from src.base.QuantumModel import QuantumModel
from src.base.Dataset import Dataset
from src.extended.LocalExecutor import LocalExecutor
from src.extended.IBMExecutor import IBMExecutor
from src.extended.QSVCModel import QSVCModel
from src.extended.QNNModel import QNNModel


class QMLAlgorithm:

    def __init__(self, dataset, execution_type, ml_model, n_executions, device=None, token=None) -> None:
        self._dataset = dataset
        self._execution_type = execution_type
        self._device = device
        self._n_executions = n_executions
        self._token = token
        self._ml_model = ml_model

    @property
    def dataset(self):
        return self._dataset

    @property
    def execution_type(self):
        return self._execution_type

    @property
    def device(self):
        return self._device

    @property
    def n_executions(self):
        return self._n_executions

    @property
    def token(self):
        return self._token

    @property
    def ml_model(self):
        return self._ml_model

    def run(self):
        quantum_model = self.create_quantum_model()
        salida = quantum_model.run()
        return salida

    def create_quantum_instance(self):
        if self.execution_type == 'local':
            backend, quantum_instance = LocalExecutor(self.device + "_simulator", self.n_executions).createBackend()
        elif self.execution_type == 'ibm':
            backend, quantum_instance = IBMExecutor(self.token, self.n_executions).createBackend()
        else:
            raise ValueError("The execution type is invalid.")
        return backend, quantum_instance

    def create_quantum_model(self):
        dataset = Dataset(self.dataset)
        backend, quantum_instance = self.create_quantum_instance()
        if self.ml_model == 'qsvm':
            return QSVCModel(dataset, quantum_instance, self.n_executions, backend)
        elif self.ml_model == 'qnn':
            return QNNModel(dataset, quantum_instance, self.n_executions, backend)
        else:
            raise ValueError("The model selected is invalid.")
