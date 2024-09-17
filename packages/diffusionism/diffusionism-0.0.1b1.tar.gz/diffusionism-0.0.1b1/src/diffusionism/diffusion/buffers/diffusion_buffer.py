from abc import ABC, abstractmethod
import numpy as np
from torch import Tensor
import torchflint as te


class DiffusionBuffer(te.nn.BufferObject, ABC):
    def __init__(self, num_timesteps: int = 1000):
        super().__init__()
        self.num_timesteps = num_timesteps
        self.timesteps = np.arange(self.num_timesteps)
        self.prev_timesteps = np.concatenate([[0], self.timesteps[:-1]])
        
        self.eta = 0.
    
    @abstractmethod
    def degradation_var(self, x_t: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        # beta_t
        pass

    @abstractmethod
    def retention_var(self, x_t: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        # alpha_t = 1 - beta_t
        pass
    
    @abstractmethod
    def degradation_std(self, x_t: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        # beta_t
        pass

    @abstractmethod
    def retention_std(self, x_t: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        # alpha_t = 1 - beta_t
        pass
    
    @abstractmethod
    def degradation_total_var(self, x_start: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        # \hat{beta_t}
        pass

    @abstractmethod
    def retention_total_var(self, x_start: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        # \hat{alpha_t}
        pass
    
    @abstractmethod
    def degradation_total_std(self, x_start: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        # \sqrt{\hat{beta_t}}
        pass

    @abstractmethod
    def retention_total_std(self, x_start: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        # \sqrt{\hat{alpha_t}}
        pass

    @abstractmethod
    def reciprocal_retention_total_std(self, x_start: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        # \sqrt{1 / \hat{alpha_t}}
        pass
    
    @abstractmethod
    def complementary_reciprocal_retention_total_std(self, x_start: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        # \sqrt{1 / \hat{alpha_t} - 1}
        pass

    @abstractmethod
    def posterior_var(self, x: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        pass
    
    @abstractmethod
    def posterior_log_var(self, x: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        pass
    
    @abstractmethod
    def posterior_mean_start_coefficient(self, x_start: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        # (\sqrt{\bar{\alpha}_{t-1}} \beta_t) / (1 - \bar{\alpha}_t)
        pass
    
    @abstractmethod
    def posterior_mean_current_coefficient(self, x_t: Tensor, timestep: Tensor, *args, **kwargs) -> Tensor:
        # (\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})) / (1 - \bar{\alpha}_t)
        pass