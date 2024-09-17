from typing import overload, Optional, Iterable, Tuple
from abc import abstractmethod
from tqdm import tqdm
import torch
from torch import Tensor
from torch import nn
from ..buffers.diffusion_buffer import DiffusionBuffer
from ..diffusion import MetaDiffusion, Diffusion
from ..parameterizations import Parameterization, NoiseParameterization
from ..diffusers.diffuser import Diffuser


class Sampler(Diffusion, diffusion_buffer=DiffusionBuffer, diffuser=Diffuser):
    diffusion_buffer: DiffusionBuffer
    diffuser: Diffuser
    
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
        **kwargs
    ):
        super(Diffusion, self).__init__()
        self.backbone = backbone
        self.parameterization = parameterization
        self.diffusion_buffer = MetaDiffusion.get_diffusion_buffer(
            type(self).diffusion_buffer, f"{type(self).__name__}.{type(self).__init__.__code__.co_name}()", *args, **kwargs
        )
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @classmethod
    def extract_main_timestep(cls, timesteps: Iterable[Tensor]):
        return timesteps[0]

    @torch.no_grad()
    @classmethod
    def sample(
        cls,
        backbone: nn.Module,
        diffusion_buffer: DiffusionBuffer,
        parameterization: Parameterization,
        x_end: Tensor,
        *args,
        additional_residuals: Optional[Iterable[Tensor]] = None,
        x_inpaint: Optional[Tensor] = None,
        mask: Optional[Tensor] = None,
        initial_state: Optional[Tensor] = None,
        strength: float = 0.8,
        **kwargs
    ):
        # p_sample_loop
        """
        Algorithm 2.
        """
        x_t, timestep_iters, length = cls.initialize_state(diffusion_buffer, x_end, initial_state, strength, *args, **kwargs)
        
        for timesteps in tqdm(zip(*timestep_iters), leave=False, total=length):
            timesteps = [torch.full((x_end.size(0),), timestep, device=x_end.device, dtype=torch.long) for timestep in timesteps]
            if mask is not None:
                assert x_inpaint is not None
                diffused_inpainting_x = cls.diffuser.diffuse(
                    diffusion_buffer,
                    x_inpaint,
                    cls.extract_main_timestep(timesteps),
                )  # TODO: deterministic forward pass?
                x_t = diffused_inpainting_x * mask + (1. - mask) * x_t
            x_t = cls.sample_step(
                backbone,
                diffusion_buffer,
                parameterization,
                x_t,
                timesteps,
                *args,
                additional_residuals=additional_residuals,
                **kwargs
            )
        
        return x_t
    
    @torch.no_grad()
    def forward(
        self,
        x_end: Tensor,
        *args,
        additional_residuals: Optional[Iterable[Tensor]] = None,
        x_inpaint: Optional[Tensor] = None,
        mask: Optional[Tensor] = None,
        initial_state: Optional[Tensor] = None,
        strength: float = 0.8,
        **kwargs
    ):
        return self.sample(
            self.backbone,
            self.diffusion_buffer,
            self.parameterization,
            x_end,
            *args,
            additional_residuals=additional_residuals,
            x_inpaint=x_inpaint,
            mask=mask,
            initial_state=initial_state,
            strength=strength,
            **kwargs
        )