from qiskit import IBMQ


class Validator:

    @staticmethod
    def check_local_device(device: str):
        if device not in ["qasm_simulator", "statevector_simulator", "unitary_simulator"]:
            raise ValueError("The specified local device does not exist.")

    @staticmethod
    def check_token(token: str):
        try:
            IBMQ.save_account(token, overwrite=True)
            IBMQ.load_account()
        except:
            raise ValueError("The specified token is invalid.")

    @staticmethod
    def check_n_executions(n_executions: int):
        if n_executions <= 0 or n_executions >= 10000:
            raise ValueError("The specified number of executions is invalid.")
