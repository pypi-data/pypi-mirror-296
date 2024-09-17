from typing import Type, overload, Union, Callable, Optional, Iterable
import torch
from torch import Tensor
from torch import nn
from .buffers.diffusion_buffer import DiffusionBuffer
from .diffusers.diffuser import Diffuser
from .samplers.sampler import Sampler
from .parameterizations import Parameterization, NoiseParameterization
from . import losses


class MetaDiffusion(type):
    diffusion_buffer: Type[DiffusionBuffer]
    diffuser: Type[Diffuser]
    sampler: Type[Sampler]
    
    def __new__(metacls, name, bases, attrdict, **kwargs):
        diffusion_buffer = kwargs.get('diffusion_buffer')
        if diffusion_buffer is not None:
            attrdict['diffusion_buffer'] = diffusion_buffer
        diffuser = kwargs.get('diffuser')
        if diffuser is not None:
            attrdict['diffuser'] = diffuser
        sampler = kwargs.get('sampler')
        if sampler is not None:
            attrdict['sampler'] = sampler
        cls = super().__new__(metacls, name, bases, attrdict)
        return cls
    
    @staticmethod
    def get_diffusion_buffer(diffusion_type: type, error_head: str = 'it', *args, **kwargs) -> DiffusionBuffer:
        args_length = len(args)
        kwargs_length = len(kwargs)
        diffusion_buffer = kwargs.get('diffusion_buffer')
        if args_length == 0:
            if diffusion_buffer is None:
                raise TypeError(f"missing 1 required positional argument: 'diffusion_buffer'")
            elif kwargs_length != 1:
                raise TypeError(f"{error_head} got an unexpected keyword argument '{kwargs.keys()[1]}'")
        elif args_length == 1 and isinstance(args[0], DiffusionBuffer):
            if kwargs_length != 0:
                raise TypeError(f"{error_head} got an unexpected keyword argument '{kwargs.keys()[0]}'")
            if diffusion_buffer is None:
                diffusion_buffer = args[0]
            else:
                raise TypeError(f"{error_head} got multiple values for argument 'diffusion_buffer'")
        else:
            if diffusion_buffer is None:
                diffusion_buffer = diffusion_type(*args, **kwargs)
            elif kwargs_length != 1:
                raise TypeError(f"{error_head} got an unexpected keyword argument '{kwargs.keys()[1]}'")
        return diffusion_buffer


class Diffusion(nn.Module, metaclass=MetaDiffusion, diffusion_buffer=DiffusionBuffer):
    pass


class DiffusionModel(Diffusion, metaclass=MetaDiffusion):
    diffuser: Diffuser
    sampler: Sampler
    
    @overload
    def __init__(self, diffuser: Diffuser, sampler: Sampler):
        ...
    
    @overload
    def __init__(
        self,
        diffuser: Type[Diffuser],
        sampler: Type[Sampler],
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
        diffuser: Type[Diffuser],
        sampler: Type[Sampler],
        backbone: nn.Module,
        *args,
        parameterization: Parameterization = NoiseParameterization(),
        loss_function: Callable[[Tensor, Tensor], Tensor] = losses.mse_loss,
        **kwargs
    ):
        ...
    
    def __init__(self, diffuser: Union[Type[Diffuser], Diffuser], sampler: Union[Type[Sampler], Sampler], *args, **kwargs):
        super().__init__()
        if isinstance(diffuser, Diffuser):
            self.diffuser = diffuser
            if isinstance(sampler, Sampler):
                self.sampler = sampler
            elif issubclass(sampler, Sampler):
                try:
                    self.sampler = sampler(
                        self.diffuser.backbone,
                        self.diffuser.diffusion_buffer,
                        parameterization=self.diffuser.parameterization
                    )
                except:
                    self.sampler = sampler(*args, **kwargs)
            else:
                raise TypeError(f"'sampler' should be a subclass or an instance of '{Sampler.__name__}', but got a counterpart of '{sampler.__name__ if isinstance(sampler, type) else type(sampler).__name__}'.")
        elif issubclass(diffuser, Diffuser):
            if isinstance(sampler, Sampler):
                self.sampler = sampler
                try:
                    self.diffuser = diffuser(
                        self.sampler.backbone,
                        self.sampler.diffusion_buffer,
                        parameterization=self.sampler.parameterization,
                        **kwargs
                    )
                except:
                    self.diffuser = diffuser(*args, **kwargs)
            elif issubclass(sampler, Sampler):
                from inspect import signature
                diffuser_init_parameter_keys = set(signature(diffuser).parameters.keys())
                sampler_init_parameter_keys = set(signature(sampler).parameters.keys())
                intersection_keys = diffuser_init_parameter_keys.intersection(sampler_init_parameter_keys)
                union_keys = sampler_init_parameter_keys.union(sampler_init_parameter_keys)
                complementary_keys = union_keys.difference(intersection_keys)
                sampler_kwarg_keys = set(kwargs.keys()).difference(complementary_keys)
                
                self.diffuser = diffuser(*args, **kwargs)
                self.sampler = sampler(*args, **{key : kwargs[key] for key in sampler_kwarg_keys})
            else:
                raise TypeError(f"'sampler' should be a subclass or an instance of '{Sampler.__name__}', but got a counterpart of '{sampler.__name__ if isinstance(sampler, type) else type(sampler).__name__}'.")
        else:
            raise TypeError(f"'diffuser' should be a subclass or an instance of '{Diffuser.__name__}', but got a counterpart of '{diffuser.__name__ if isinstance(diffuser, type) else type(diffuser).__name__}'.")
    
    def diffuse(
        self,
        x_start: Tensor,
        timestep: Tensor,
        *args,
        degradation: Optional[Tensor] = None,
        **kwargs
    ) -> Tensor:
        return self.diffuser.diffuse(
            self.diffuser.diffusion_buffer,
            x_start,
            timestep,
            *args,
            degradation=degradation,
            **kwargs
        )
    
    @torch.no_grad()
    def sample(
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
        return self.sampler.sample(
            self.sampler.backbone,
            self.sampler.diffusion_buffer,
            self.sampler.parameterization,
            x_end,
            *args,
            additional_residuals=additional_residuals,
            x_inpaint=x_inpaint,
            mask=mask,
            initial_state=initial_state,
            strength=strength,
            **kwargs
        )
    
    def get_losses(
        self,
        x_start: Tensor,
        *args,
        additional_residuals: Optional[Iterable[Tensor]] = None,
        **kwargs
    ) -> Tensor:
        return self.diffuser(x_start, *args, additional_residuals=additional_residuals, **kwargs)
    
    def forward(self, *args, **kwargs):
        if self.training:
            return self.diffuser(*args, **kwargs)
        else:
            return self.sampler(*args, **kwargs)