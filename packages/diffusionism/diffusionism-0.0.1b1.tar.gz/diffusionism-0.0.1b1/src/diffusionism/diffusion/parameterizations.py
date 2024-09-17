from typing import Optional
from abc import ABC, abstractmethod
import torch
from torch import Tensor
from .buffers.diffusion_buffer import DiffusionBuffer


class Parameterization(ABC):
    def __init__(self, simple_weight = 1., elbo_weight = 0.):
        super().__init__()
        self.simple_weight = simple_weight
        self.elbo_weight = elbo_weight
    
    @property
    def is_loss_complex(self) -> bool:
        return self.simple_weight != 1. or self.elbo_weight != 0.
    
    @abstractmethod
    def optimization_target(
        self,
        diffusion_buffer: DiffusionBuffer,
        x_start: Tensor,
        timestep: Tensor,
        *args,
        degradation: Optional[Tensor] = None,
        **kwargs
    ) -> Tensor:
        pass
    
    @abstractmethod
    def variational_weights(
        self,
        diffusion_buffer: DiffusionBuffer,
        x_t: Tensor,
        timestep: Tensor,
        *args,
        **kwargs
    ) -> Tensor:
        pass
    
    @abstractmethod
    def predict_current_and_start(
        self,
        backbone_prediction: Tensor,
        diffusion_buffer: DiffusionBuffer,
        x_t: Tensor,
        timestep: Tensor,
        *args,
        retention_total_var: Optional[Tensor] = None,
        **kwargs
    ) -> Tensor:
        pass
    
    @abstractmethod
    def reconstruct_step(
        self,
        diffusion_buffer: DiffusionBuffer,
        x_t: Tensor,
        timestep: Tensor,
        *args,
        degradation: Optional[Tensor] = None,
        **kwargs
    ) -> Tensor:
        pass


class NoiseParameterization(Parameterization):
    def optimization_target(
        self,
        diffusion_buffer: DiffusionBuffer,
        x_start: Tensor,
        timestep: Tensor,
        *args,
        degradation: Optional[Tensor] = None,
        **kwargs
    ) -> Tensor:
        return degradation
    
    def variational_weights(
        self,
        diffusion_buffer: DiffusionBuffer,
        x_t: Tensor,
        timestep: Tensor,
        *args,
        **kwargs
    ) -> Tensor:
        timestep = timestep.clone()
        timestep[timestep == 0] = 1
        return (
            torch.square(diffusion_buffer.degradation_var(x_t, timestep, *args, **kwargs)) / 
            (
                2 * diffusion_buffer.posterior_var(x_t, timestep, *args, **kwargs) *
                diffusion_buffer.retention_var(x_t, timestep, *args, **kwargs) *
                (1 - diffusion_buffer.retention_total_var(x_t, timestep, *args, **kwargs))
            )
        )
    
    def predict_current_and_start(
        self,
        backbone_prediction: Tensor,
        diffusion_buffer: DiffusionBuffer,
        x_t: Tensor,
        timestep: Tensor,
        *args,
        retention_total_var: Optional[Tensor] = None,
        **kwargs
    ) -> Tensor:
        if retention_total_var is None:
            retention_total_var = diffusion_buffer.retention_total_var(x_t, timestep, *args, **kwargs)
        
        e_t = backbone_prediction
        pred_x0 = (x_t - torch.sqrt(1. - retention_total_var) * e_t) / torch.sqrt(retention_total_var)
        return e_t, pred_x0
    
    def reconstruct_step(
        self,
        diffusion_buffer: DiffusionBuffer,
        x_t: Tensor,
        timestep: Tensor,
        *args,
        degradation: Optional[Tensor] = None,
        **kwargs
    ) -> Tensor:
        mean = diffusion_buffer.reciprocal_retention_total_std(x_t, timestep, *args, **kwargs) * x_t
        std = diffusion_buffer.complementary_reciprocal_retention_total_std(x_t, timestep, *args, **kwargs)
        return mean - std * degradation


class InputParameterization(NoiseParameterization):
    def optimization_target(
        self,
        diffusion_buffer: DiffusionBuffer,
        x_start: Tensor,
        timestep: Tensor,
        *args,
        degradation: Optional[Tensor] = None,
        **kwargs
    ) -> Tensor:
        return x_start

    def variational_weights(
        self,
        diffusion_buffer: DiffusionBuffer,
        x_t: Tensor,
        timestep: Tensor,
        *args,
        **kwargs
    ) -> Tensor:
        timestep = timestep.clone()
        timestep[timestep == 0] = 1
        return 0.5 * torch.sqrt(diffusion_buffer.retention_total_var(x_t, timestep, *args, **kwargs)) / (2. * 1 - diffusion_buffer.retention_total_var(x_t, timestep, *args, **kwargs))
    
    def reconstruct_step(
        self,
        diffusion_buffer: DiffusionBuffer,
        x_t: Tensor,
        timestep: Tensor,
        *args,
        degradation: Tensor,
        **kwargs
    ) -> Tensor:
        return degradation

class VParameterization(Parameterization):
    def optimization_target(
        self,
        diffusion_buffer: DiffusionBuffer,
        x_start: Tensor,
        timestep: Tensor,
        *args,
        degradation: Tensor,
        **kwargs
    ) -> Tensor:
        return (
            diffusion_buffer.retention_total_std(x_start, timestep, *args, **kwargs) * degradation -
            diffusion_buffer.degradation_total_std(x_start, timestep, *args, **kwargs) * x_start
        )
    
    def predict_current_and_start(
        self,
        backbone_prediction: Tensor,
        diffusion_buffer: DiffusionBuffer,
        x_t: Tensor,
        timestep: Tensor,
        *args,
        retention_total_var: Optional[Tensor] = None,
        **kwargs
    ) -> Tensor:
        retention_total_std = diffusion_buffer.retention_total_std(x_t, timestep, *args, **kwargs)
        degradation_total_std = diffusion_buffer.degradation_total_std(x_t, timestep, *args, **kwargs)
        
        e_t = retention_total_std * backbone_prediction + degradation_total_std * x_t
        pred_x0 = retention_total_std * x_t - degradation_total_std * backbone_prediction
        return e_t, pred_x0
    
    def variational_weights(
        self,
        diffusion_buffer: DiffusionBuffer,
        x_t: Tensor,
        timestep: Tensor,
        *args,
        **kwargs
    ) -> Tensor:
        timestep = timestep.clone()
        timestep[timestep == 0] = 1
        return torch.ones_like(
            torch.square(diffusion_buffer.degradation_var(x_t, timestep, *args, **kwargs)) / 
            (
                2 * diffusion_buffer.posterior_var(x_t, timestep, *args, **kwargs) *
                diffusion_buffer.retention_var(x_t, timestep, *args, **kwargs) *
                (1 - diffusion_buffer.retention_total_var(x_t, timestep, *args, **kwargs))
            )
        )
    
    def reconstruct_step(
        self,
        diffusion_buffer: DiffusionBuffer,
        x_t: Tensor,
        timestep: Tensor,
        *args,
        degradation: Optional[Tensor] = None,
        **kwargs
    ) -> Tensor:
        raise TypeError(f"{type(self).__name__} is only suitbale for DDIM samplers, and the current sampling process might not be DDIM.")