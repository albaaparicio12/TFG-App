from abc import ABC, abstractmethod
from src.base.Dataset import Dataset


class QuantumModel(ABC):

    def __init__(self, dataset: Dataset, quantum_instance, backend) -> None:
        self._dataset = dataset
        self._quantum_instance = quantum_instance
        self._backend = backend

    @property
    def dataset(self):
        return self._dataset

    @property
    def quantum_instance(self):
        return self._quantum_instance

    @abstractmethod
    def run(self):
        """
        """
