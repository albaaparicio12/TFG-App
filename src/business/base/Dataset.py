from qiskit_machine_learning.datasets import ad_hoc_data, breast_cancer, gaussian
import matplotlib.pyplot as plt
import numpy as np
from business.base.Validator import InvalidValueException


class Dataset:

    def __init__(self, selected_dataset: str) -> None:

        self._X_test = None
        self._y_test = None
        self._X_train = None
        self._y_train = None
        self._selected_dataset = selected_dataset
        self.define_data()

    @property
    def selected_dataset(self):
        return self._selected_dataset

    @property
    def X_train(self):
        return self._X_train

    @property
    def y_train(self):
        return self._y_train

    @property
    def X_test(self):
        return self._X_test

    @property
    def y_test(self):
        return self._y_test

    def define_data(self):
        """Crea los subconjuntos de entrenamiento y test dado un conjunto de datos seleccionado por el usuario."""
        if self.selected_dataset == 'ad_hoc_data':
            X_train, y_train, X_test, y_test = ad_hoc_data(
                training_size=20,
                test_size=5,
                n=2,
                gap=0.1,
                one_hot=False)
        else:
            X_train, y_train, X_test, y_test = self.select_dataset()(
                training_size=20,
                test_size=5,
                n=2,
                one_hot=False)

        self._X_train = X_train
        self._y_train = y_train
        self._X_test = X_test
        self._y_test = y_test
        self.show_plot()

    def show_plot(self):
        """ Crea el gráfico del conjunto de datos seleccionado por el usuario"""
        x_total = np.concatenate((self.X_train, self.X_test), axis=0)
        y_total = np.concatenate((self.y_train, self.y_test), axis=0)
        if self.selected_dataset == 'ad_hoc_data':
            self.plot_ad_hoc_data(x_total, y_total)
        elif self.selected_dataset == 'gaussian':
            self.plot_gaussian(x_total, y_total)
        elif self.selected_dataset == 'breast_cancer':
            self.plot_breast_cancer(x_total, y_total)

    def plot_ad_hoc_data(self, x_total, y_total):
        """ Crea el gráfico del conjunto de datos ad_hoc_data"""
        plt.show()
        n = x_total.shape[1]
        fig = plt.figure()
        projection = "3d" if n == 3 else None
        ax1 = fig.add_subplot(1, 1, 1, projection=projection)
        for k in range(0, 2):
            ax1.scatter(*x_total[y_total == k][:20].T)
        ax1.set_title("Ad-hoc Data")
        plt.savefig('./static/files/grafo.png')

    def plot_gaussian(self, sample_train, label_train):
        """ Crea el gráfico del conjunto de datos gaussian"""
        plt.show()
        for k in range(0, 3):
            plt.scatter(
                sample_train[label_train == k, 0][:20],
                sample_train[label_train == k, 1][:20],
            )

        plt.title("Gaussians")
        plt.savefig('./static/files/grafo.png')

    def plot_breast_cancer(self, sample_train, label_train):
        """ Crea el gráfico del conjunto de datos breast_cancer"""
        plt.show()
        for k in range(0, 2):
            plt.scatter(
                sample_train[label_train == k, 0][:20],
                sample_train[label_train == k, 1][:20],
            )

        plt.title("PCA dim. reduced Breast cancer dataset")
        plt.savefig('./static/files/grafo.png')

    def select_dataset(self):
        """
        Devuelve la instancia del conjunto de datos seleccionado por el usuario.
        Lanza una excepción en el caso de que introduzca un nombre que no existe.

        :return: Qiskit dataset instance
        """
        if self._selected_dataset == 'breast_cancer':
            return breast_cancer
        elif self._selected_dataset == 'gaussian':
            return gaussian
        else:
            raise InvalidValueException("Wrong dataset", 2000)

    def get_data(self):
        """Devuelve los subconjuntos de entrenamiento y test.

        :return: Subconjuntos X_train e y_train de entrenamiento y X_test e y_test de test.
        """
        return self.X_train, self.y_train, self.X_test, self.y_test
