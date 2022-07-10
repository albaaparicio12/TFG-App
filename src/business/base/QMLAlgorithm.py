from business.base.Dataset import Dataset
from src.business.extended.executors.LocalExecutor import LocalExecutor
from src.business.extended.executors.IBMExecutor import IBMExecutor
from src.business.extended.quantum_models.QSVCModel import QSVCModel
from src.business.extended.quantum_models.QNNModel import QNNModel
from business.base.Validator import InvalidValueException


class QMLAlgorithm:

    def __init__(self, dataset, execution_type, ml_model, n_executions, device=None) -> None:
        self._dataset = dataset
        self._execution_type = execution_type
        self._device = device
        self._n_executions = n_executions
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
    def ml_model(self):
        return self._ml_model

    def run(self, token: str):
        quantum_model = self.create_quantum_model(token)
        salida = quantum_model.run()
        return salida

    def create_quantum_instance(self, token: str):
        if self.execution_type == 'local':
            backend, quantum_instance = LocalExecutor(self.device, self.n_executions).create_backend()
        elif self.execution_type == 'ibm':
            backend, quantum_instance = IBMExecutor(token, self.n_executions).create_backend()
        else:
            raise InvalidValueException("The execution type is invalid.", 2000)
        return backend, quantum_instance

    def create_quantum_model(self, token: str):
        dataset = Dataset(self.dataset)
        backend, quantum_instance = self.create_quantum_instance(token)
        if self.ml_model == 'qsvm':
            return QSVCModel(dataset, quantum_instance, backend)
        elif self.ml_model == 'qnn':
            return QNNModel(dataset, quantum_instance, backend)
        else:
            raise InvalidValueException("The model selected is invalid.", 2000)
