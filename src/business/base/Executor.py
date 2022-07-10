from abc import ABC, abstractmethod


class Executor(ABC):
    """Interfaz Executor.

    Sirve para dar una estructura al backedn donde se vaya a ejecutar el modelo de aprendizaje auntomático.
    """

    def __init__(self, device, n_executions) -> None:
        self._device = device
        self._n_executions = n_executions

    @property
    def device(self):
        """Nombre del dispositivo en el que se ejecuta el algoritmo

        :return: string con el nombre del dispositivo
        """
        return self._device

    @property
    def n_executions(self):
        """Número de veces que se ejecutará el algoritmo en el dispositivo

        :return: int con nº de ejecuciones
        """
        return self._n_executions

    @abstractmethod
    def create_backend(self):
        """Método que crea el backend y el circuito cuántico

        :return: backend y quantum instance
        """
