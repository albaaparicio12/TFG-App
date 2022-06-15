from src.base.Executor import Executor
from src.base.Validator import Validator
from custom_inherit import doc_inherit
from qiskit import BasicAer
from qiskit.utils import QuantumInstance


class LocalExecutor(Executor):
    def __init__(self, device, n_executions) -> None:
        super(LocalExecutor, self).__init__(device, n_executions)

    @doc_inherit(Executor.create_backend, style="google")
    def create_backend(self):
        Validator.check_local_device(self.device)
        Validator.check_n_executions(int(self.n_executions))

        seed = 0
        backend = BasicAer.get_backend(self.device)
        quantum_instance = QuantumInstance(backend, shots=1024, seed_simulator=seed, seed_transpiler=seed)
        return backend, quantum_instance
