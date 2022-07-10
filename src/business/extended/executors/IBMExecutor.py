from qiskit.utils import QuantumInstance

from business.base.Executor import Executor
from business.base.Validator import Validator
from custom_inherit import doc_inherit
from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy
from business.base.Validator import InvalidTokenException


class IBMExecutor(Executor):
    def __init__(self, token, n_executions) -> None:
        super(IBMExecutor, self).__init__(None, n_executions)
        self._authenticated = True if len(IBMQ.stored_account()) > 0 else False
        self._valid_token = self.validate_token(token)

    @property
    def valid_token(self):
        return self._valid_token

    @property
    def authenticated(self):
        return self._authenticated

    @doc_inherit(Executor.create_backend, style="google")
    def create_backend(self):
        Validator.check_n_executions(int(self.n_executions))

        provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')

        num_qubits = 2
        seed = 0
        available_devices = provider.backends(filters=lambda x: x.configuration().n_qubits >= num_qubits
                                                                and not x.configuration().simulator
                                                                and x.status().operational == True)

        backend = least_busy(available_devices)
        quantum_instance = QuantumInstance(backend, shots=int(self.n_executions), seed_simulator=seed,
                                           seed_transpiler=seed)

        return backend, quantum_instance

    def log_in_IBMQ(self, token: str):
        if self._authenticated:
            return IBMQ.load_account()
        else:
            IBMQ.save_account(token, overwrite=True)
            IBMQ.load_account()
            self._authenticated = True

    def validate_token(self, token: str) -> bool:
        if self._authenticated or Validator.check_token(token):
            self.log_in_IBMQ(token)
            return True
        else:
            raise InvalidTokenException("Invalid token.", 1000)
            return False
