from src.base.Executor import Executor
from src.base.Validator import Validator
from custom_inherit import doc_inherit
from qiskit import Aer
from qiskit.utils import QuantumInstance


class LocalExecutor(Executor):
    def __init__(self, device, n_executions) -> None:
        super(LocalExecutor, self).__init__(device, n_executions)

    @doc_inherit(Executor.create_backend, style="google")
    def create_backend(self):
        Validator.check_local_device(self.device)
        simulator = 'aer_simulator' if self.device == 'automatic' else "aer_simulator_" + self._device
        Validator.check_n_executions(int(self.n_executions))

        seed = 100224
        backend = Aer.get_backend(simulator, shots=self.n_executions)
        quantum_instance = QuantumInstance(backend, shots=self.n_executions, seed_simulator=seed, seed_transpiler=seed)
        return backend, quantum_instance
