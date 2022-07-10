from http.client import HTTPException

from qiskit import IBMQ
from qiskit import Aer
from qiskit.providers.ibmq import IBMQAccountCredentialsInvalidUrl, IBMQProviderError, IBMQAccountError


class Validator:

    @staticmethod
    def check_local_device(device: str):
        if device not in [backend._options.get('method') for backend in Aer.backends()
                          if backend._options.get('method') != None] or device == 'stabilizer' \
                or device == 'extended_stabilizer':
            raise InvalidValueException("The specified local device does not exist.", 2000)

    @staticmethod
    def check_token(token: str):
        try:
            IBMQ.enable_account(token)
            return True
        except IBMQAccountCredentialsInvalidUrl or IBMQProviderError:
            return False
        except IBMQAccountError:
            return True

    @staticmethod
    def check_n_executions(n_executions: int):
        if n_executions <= 0 or n_executions >= 20000:
            raise InvalidValueException("The specified number of executions is invalid.", 2000)


class InvalidTokenException(HTTPException):
    def __init__(self, m, code):
        self.args = m
        self.message = m
        self.errors = code


class InvalidValueException(HTTPException):
    def __init__(self, m, code):
        self.args = m
        self.message = m
        self.errors = code
