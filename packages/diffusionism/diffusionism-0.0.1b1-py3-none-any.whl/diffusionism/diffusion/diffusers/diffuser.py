from typing import overload, Callable, Optional, Iterable, Tuple
from abc import abstractmethod
import torch
from torch import Tensor
from torch import nn
from ..buffers.diffusion_buffer import DiffusionBuffer
from ..diffusion import MetaDiffusion, Diffusion
from ..parameterizations import Parameterization, NoiseParameterization
from .. import losses
from ..samplers.sampler import Sampler


class Diffuser(Diffusion, diffusion_buffer=DiffusionBuffer, sampler=Sampler):
    diffusion_buffer: DiffusionBuffer
    sampler: Sampler
    
    @overload
    def __init__(
        self,
        backbone: nn.Module,
        diffusion_buffer: DiffusionBuffer,
        *,
        parameterization: Parameterization = NoiseParameterization(),
        loss_function: Callable[[Tensor, Tensor], Tensor] = losses.mse_loss
    ):
        ...
    
    @overload
    def __init__(
        self,
        backbone: nn.Module,
        *args,
        parameterization: Parameterization = NoiseParameterization(),
        loss_function: Callable[[Tensor, Tensor], Tensor] = losses.mse_loss,
        **kwargs
    ):
        ...
    
    def __init__(
        self,
        backbone: nn.Module,
        *args,
        parameterization: Parameterization = NoiseParameterization(),
        loss_function: Callable[[Tensor, Tensor], Tensor] = losses.mse_loss,
        **kwargs
    ):
        super(Diffusion, self).__init__()
        self.backbone = backbone
        self.parameterization = parameterization
        self.loss_function = loss_function
        self.diffusion_buffer = MetaDiffusion.get_diffusion_buffer(
            type(self).diffusion_buffer, f"{type(self).__name__}.{type(self).__init__.__code__.co_name}()", *args, **kwargs
        )
    
    @abstractmethod
    @classmethod
    def get_diffusion_arguments(cls, *args, **kwargs) -> Tuple[tuple, dict]:
        pass
    
    @abstractmethod
    @classmethod
    def get_backbone_arguments(cls, *args, **kwargs) -> Tuple[tuple, dict]:
        pass
    
    @abstractmethod
    @classmethod
    def diffuse(
        cls,
        diffusion_buffer: DiffusionBuffer,
        x_start: Tensor,
        timestep: Tensor,
        *diffusion_args,
        degradation: Optional[Tensor] = None,
        **diffusion_kwargs
    ) -> Tensor:
        # q_sample
        pass
    
    @abstractmethod
    @classmethod
    def degrade(
        cls,
        diffusion_buffer: DiffusionBuffer,
        x: Tensor,
        timestep: Tensor,
        *diffusion_args,
        **diffusion_kwargs
    ) -> Tensor:
        pass
    
    def construct_optimization(
        self,
        x_start: Tensor,
        timestep: Tensor,
        *diffusion_args,
        degradation: Optional[Tensor] = None,
        **diffusion_kwargs
    ) -> Tensor:
        return self.parameterization.optimization_target(self.diffusion_buffer, x_start, timestep, *diffusion_args, degradation=degradation, **diffusion_kwargs)
    
    def forward(
        self,
        x_start: Tensor,
        *args,
        additional_residuals: Optional[Iterable[torch.Tensor]] = None,
        **kwargs
    ) -> Tensor:
        """
        Algorithm 1.
        """
        diffusion_args, diffusion_kwargs = self.get_diffusion_arguments(*args, **kwargs)
        backbone_args, backbone_kwargs = self.get_backbone_arguments(*args, **kwargs)
        
        timestep = torch.randint(self.diffusion_buffer.num_timesteps, size=x_start.shape[:1], device=x_start.device)
        degradation = self.degrade(self.diffusion_buffer, x_start, timestep, *diffusion_args, **diffusion_kwargs)
        x_t = self.diffuse(self.diffusion_buffer, x_start, timestep, *diffusion_args, degradation=degradation, **diffusion_kwargs)
        
        prediction = self.backbone(x_t, timestep, *backbone_args, additional_residuals=additional_residuals, **backbone_kwargs)
        optimization_target = self.construct_optimization(x_start, timestep, *diffusion_args, degradation=degradation, **diffusion_kwargs)
        loss = self.loss_function(prediction, optimization_target)
        
        if self.parameterization.is_loss_complex:
            loss_simple = loss * self.parameterization.simple_weight
            loss_vlb = self.parameterization.variational_weights(self.diffusion_buffer, x_t, timestep, *diffusion_args, **diffusion_kwargs) * loss
            loss = loss_simple + self.parameterization.elbo_weight * loss_vlb
        
        return loss