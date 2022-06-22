from qiskit_machine_learning.datasets import ad_hoc_data, breast_cancer, gaussian
import matplotlib.pyplot as plt
from src.base.Validator import InvalidValueException


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
        if self.selected_dataset == 'ad_hoc_data':
            X_train, y_train, X_test, y_test = ad_hoc_data(
                training_size=20,
                test_size=5,
                n=2,
                gap=0.1,
                plot_data=True,
                one_hot=False)
        else:
            X_train, y_train, X_test, y_test = self.select_dataset()(
                training_size=20,
                test_size=5,
                n=2,
                plot_data=True,
                one_hot=False)

        self._X_train = X_train
        self._y_train = y_train
        self._X_test = X_test
        self._y_test = y_test

        plt.savefig('my_plot.png')

    def select_dataset(self):
        if self._selected_dataset == 'breast_cancer':
            return breast_cancer
        elif self._selected_dataset == 'gaussian':
            return gaussian
        else:
            raise InvalidValueException("Wrong dataset", 2000)

    def get_data(self):
        return self.X_train, self.y_train, self.X_test, self.y_test
