from typing import overload, Optional, Iterable, Tuple
from enum import Enum, auto
from copy import copy
import numpy as np
import torch
from torch import Tensor
from torch import nn
from .sampler import Sampler
from ..parameterizations import Parameterization, NoiseParameterization
from ..buffers.diffusion_buffer import DiffusionBuffer
from ..buffers.gaussian_diffusion_buffer import GaussianDiffusionBuffer


class GaussianDDPMSampler(Sampler, diffusion_buffer=GaussianDiffusionBuffer):
    diffusion_buffer: GaussianDiffusionBuffer
    
    @classmethod
    def posteriorize(
        cls,
        diffusion_buffer: DiffusionBuffer,
        x_start: Tensor,
        x_t: Tensor,
        timestep: Tensor,
        *diffusion_args,
        **diffusion_kwargs
    ) -> Tuple[Tensor, Tensor, Tensor]:
        # q_posterior
        posterior_mean = (
            diffusion_buffer.posterior_mean_start_coefficient(x_start, timestep, *diffusion_args, **diffusion_kwargs) * x_start +
            diffusion_buffer.posterior_mean_current_coefficient(x_t, timestep, *diffusion_args, **diffusion_kwargs) * x_t
        )
        posterior_variance = diffusion_buffer.posterior_var(x_t, timestep, *diffusion_args, **diffusion_kwargs)
        posterior_log_variance_clipped = diffusion_buffer.posterior_log_var(x_t, timestep, *diffusion_args, **diffusion_kwargs)
        return posterior_mean, posterior_variance, posterior_log_variance_clipped
        
    @classmethod
    def initialize_state(
        cls,
        diffusion_buffer: DiffusionBuffer,
        x_end: Tensor,
        initial_state: Optional[Tensor] = None,
        strength: float = 0.8,
        *args,
        **kwargs
    ) -> Tuple[Tensor, Tuple[Iterable[int]], int]:
        if initial_state is None or strength >= 1.:
            t_start = diffusion_buffer.num_timesteps - 1
            x_t = x_end
        else:
            diffusion_args, diffusion_kwargs = cls.diffuser.get_diffusion_arguments(*args, **kwargs)
            
            t_start = int((diffusion_buffer.num_timesteps - 1) * strength)
            strengthened_t = torch.full((x_end.shape[0],), t_start, dtype=torch.long, device=x_end.device)
            x_t = cls.diffuser.diffuse(
                diffusion_buffer,
                initial_state,
                strengthened_t,
                *diffusion_args,
                degradation=x_end,
                **diffusion_kwargs
            )
        return x_t, (range(t_start, -1, -1),), diffusion_buffer.num_timesteps
    
    @torch.no_grad()
    @classmethod
    def sample_step(
        cls,
        backbone: nn.Module,
        diffusion_buffer: DiffusionBuffer,
        parameterization: Parameterization,
        x_t: Tensor,
        timesteps: Iterable[Tensor],
        *args,
        additional_residuals: Optional[Iterable[Tensor]] = None,
        **kwargs
    ) -> Tensor:
        # p_sample
        timestep: Tensor = timesteps[0]
        
        # p_mean_variance
        diffusion_args, diffusion_kwargs = cls.diffuser.get_diffusion_arguments(*args, **kwargs)
        backbone_args, backbone_kwargs = cls.diffuser.get_backbone_arguments(*args, **kwargs)
        
        prediction = backbone(x_t, timestep, *backbone_args, additional_residuals=additional_residuals, **backbone_kwargs)
        step_reconstruction = parameterization.reconstruct_step(
            diffusion_buffer,
            x_t,
            timestep,
            *diffusion_args,
            degradation=prediction,
            **diffusion_kwargs
        )

        model_mean, posterior_variance, posterior_log_variance = cls.posteriorize(
            diffusion_buffer,
            step_reconstruction,
            x_t,
            timestep,
            *diffusion_args,
            **diffusion_kwargs
        )
        model_mean, _, model_log_variance = model_mean, posterior_variance, posterior_log_variance
        
        degradation = cls.diffuser.degrade(
            diffusion_buffer,
            x_t,
            timestep,
            *diffusion_args,
            **diffusion_kwargs
        )
        # no noise when t == 0
        nonzero_mask = (1 - (timestep == 0).float()).reshape(x_t.size(0), *((1,) * (len(x_t.shape) - 1)))
        return model_mean + nonzero_mask * (0.5 * model_log_variance).exp() * degradation


class GaussianDDIMSampler(GaussianDDPMSampler, diffusion_buffer=GaussianDiffusionBuffer):
    diffusion_buffer: GaussianDiffusionBuffer
    
    class Method(Enum):
        uniform = auto()
        quad = auto()
    
    @overload
    def __init__(
        self,
        backbone: nn.Module,
        diffusion_buffer: DiffusionBuffer,
        *,
        parameterization: Parameterization = NoiseParameterization()
    ):
        ...
    
    @overload
    def __init__(
        self,
        backbone: nn.Module,
        *args,
        parameterization: Parameterization = NoiseParameterization(),
        **kwargs
    ):
        ...
    
    def __init__(
        self,
        backbone: nn.Module,
        *args,
        parameterization: Parameterization = NoiseParameterization(),
        expected_timesteps: int = 50,
        method: Method = Method.uniform,
        eta: float = 0.,
        **kwargs
    ):
        super().__init__(backbone, *args, parameterization=parameterization, **kwargs)
        self.diffusion_buffer = copy(self.diffusion_buffer)
        
        num_timesteps = self.diffusion_buffer.num_timesteps
        if method == GaussianDDIMSampler.Method.uniform:
            c = num_timesteps // expected_timesteps
            self.diffusion_buffer.timesteps = np.asarray(list(range(0, num_timesteps, c)))
        elif method == GaussianDDIMSampler.Method.quad:
            self.diffusion_buffer.timesteps = ((np.linspace(0, np.sqrt(num_timesteps * .8), expected_timesteps)) ** 2).astype(int)
        self.diffusion_buffer.prev_timesteps = np.concatenate([[0], self.diffusion_buffer.timesteps[:-1]])
        
        self.diffusion_buffer.eta = eta

    @classmethod
    def initialize_state(
        cls,
        diffusion_buffer: DiffusionBuffer,
        x_end: Tensor,
        initial_state: Optional[Tensor] = None,
        strength: float = 0.8,
        *args,
        **kwargs
    ) -> Tuple[Tensor, Tuple[Iterable[int]], int]:
        flip_ddim_timesteps = np.flip(diffusion_buffer.timesteps)
        flip_ddim_prev_timesteps = np.flip(diffusion_buffer.prev_timesteps)
        num_timesteps = diffusion_buffer.num_timesteps
        if initial_state is None or strength >= 1.:
            skip_steps = 0
            x_t = x_end
            ddim_timesteps = flip_ddim_timesteps
            ddim_prev_timesteps = flip_ddim_prev_timesteps
        else:
            diffusion_args, diffusion_kwargs = cls.diffuser.get_diffusion_arguments(*args, **kwargs)
            
            t_start = int((num_timesteps - 1) * strength)
            strengthened_t = torch.full((x_end.shape[0],), t_start, dtype=torch.long, device=x_end.device)
            x_t = cls.diffuser.diffuse(
                diffusion_buffer,
                initial_state,
                strengthened_t,
                *diffusion_args,
                degradation=x_end,
                **diffusion_kwargs
            )
            skip_steps = np.argmin(np.abs(flip_ddim_timesteps - t_start))
            if t_start >= flip_ddim_timesteps[skip_steps]:
                skip_steps += 1
            ddim_timesteps = flip_ddim_timesteps[skip_steps:]
            ddim_prev_timesteps = flip_ddim_prev_timesteps[skip_steps:]
        return x_t, (ddim_timesteps, ddim_prev_timesteps), len(ddim_timesteps)

    @torch.no_grad()
    @classmethod
    def sample_step(
        cls,
        backbone: nn.Module,
        diffusion_buffer: DiffusionBuffer,
        parameterization: Parameterization,
        x_t: Tensor,
        timesteps: Iterable[Tensor],
        *args,
        additional_residuals: Optional[Iterable[Tensor]] = None,
        returns_start_prediction: bool = False,
        **kwargs
    ) -> Tensor:
        # p_sample
        diffusion_args, diffusion_kwargs = cls.diffuser.get_diffusion_arguments(*args, **kwargs)
        backbone_args, backbone_kwargs = cls.diffuser.get_backbone_arguments(*args, **kwargs)
        
        t, prev_t = timesteps
        ddim_alpha = diffusion_buffer.retention_total_var(x_t, t, *diffusion_args, **diffusion_kwargs)
        ddim_alpha_prev = diffusion_buffer.retention_total_var(x_t, prev_t, *diffusion_args, **diffusion_kwargs)
        
        prediction = backbone(x_t, t, *backbone_args, additional_residuals=additional_residuals, **backbone_kwargs)
        e_t, pred_x0 = parameterization.predict_current_and_start(
            prediction,
            diffusion_buffer,
            x_t,
            t,
            *diffusion_args,
            retention_total_var=ddim_alpha,
            **diffusion_kwargs
        )
        
        if diffusion_buffer.eta == 0:
            ddim_sigma = 0
            sigma_noise = 0
        else:
            ddim_sigma = diffusion_buffer.eta * torch.sqrt((1 - ddim_alpha_prev) / (1 - ddim_alpha) * (1 - ddim_alpha / ddim_alpha_prev))
            degradation = cls.diffuser.degrade(
                diffusion_buffer,
                x_t,
                t,
                *diffusion_args,
                **diffusion_kwargs
            )
            sigma_noise = ddim_sigma * degradation
        dir_xt = torch.sqrt(1. - ddim_alpha_prev - ddim_sigma ** 2) * e_t
        x_t = torch.sqrt(ddim_alpha_prev) * pred_x0 + dir_xt + sigma_noise
        
        if returns_start_prediction:
            return x_t, pred_x0
        return x_t