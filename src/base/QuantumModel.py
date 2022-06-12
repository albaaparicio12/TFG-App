from abc import abstractmethod
from qiskit_machine_learning.algorithms import VQC
from qiskit.providers.basicaer import QasmSimulatorPy
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
# import the optimizer for the training
from qiskit.algorithms.optimizers import GradientDescent


class QuantumModel(ABC):
    
    def __init__(self, dataset: Dataset, quantum_instance, n_executions, backend) -> None:
        
        self._dataset = dataset
        self._quantum_instance = quantum_instance
        self._n_executions = n_executions
        self._backend = backend
    
    @property
    def dataset(self):
        return self._dataset

    @property
    def quantum_instance(self):
        return self._quantum_instance
    
    @property
    def n_executions(self):
        return self._n_executions

    @abstractmethod
    def run(self):
        """
        """

    @abstractmethod
    def createModel(self) -> QuantumModel:
        """
        """