from qiskit.utils import QuantumInstance

from src.base.Executor import Executor
from src.base.Validator import Validator
from custom_inherit import doc_inherit
from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy


class IBMExecutor(Executor):
    def __init__(self, token, n_executions) -> None:
        super(IBMExecutor, self).__init__(None, n_executions)
        self._token = token

    @property
    def token(self):
        return self._token

    @doc_inherit(Executor.create_backend, style="google")
    def create_backend(self):
        Validator.check_token(self.token)
        Validator.check_n_executions(int(self.n_executions))

        IBMQ.save_account(self.token, overwrite=True)
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub='ibm-q')

        num_qubits = 2
        seed = 0
        available_devices = provider.backends(filters=lambda x: x.configuration().n_qubits >= num_qubits
                                                                and not x.configuration().simulator
                                                                and x.status().operational == True)

        backend = least_busy(available_devices)
        quantum_instance = QuantumInstance(backend, shots=self.n_executions, seed_simulator=seed, seed_transpiler=seed)

        return backend, quantum_instance
