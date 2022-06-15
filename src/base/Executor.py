from abc import ABC, abstractmethod


class Executor(ABC):
    def __init__(self, device, n_executions) -> None:
        self._device = device
        self._n_executions = n_executions

    @property
    def device(self):
        return self._device

    @property
    def n_executions(self):
        return self._n_executions

    @abstractmethod
    def create_backend(self):
        """TODO complete docstring"""
