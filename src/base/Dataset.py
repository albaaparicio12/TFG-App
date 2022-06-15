import matplotlib.pyplot as plt
import numpy as np

from qiskit_machine_learning.datasets import ad_hoc_data, breast_cancer, gaussian, iris, wine

import QuantumModel

class Dataset():

    def __init__(self, selected_dataset:str) -> None:
        
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
        X_train, y_train, X_test, y_test = self.select_dataset(
        training_size=20,
        test_size=10,
        n=2,
        plot_data=True)

        self._X_train = X_train
        self._y_train = y_train
        self._X_test = X_test
        self._y_test = y_test


    def select_dataset(self):
        #TODO arreglar ad_hoc, necesita atributo gap
        if(self._selected_dataset == 'ad_hoc_data'):
            return ad_hoc_data
        else if(self._selected_dataset == 'breast_cancer'):
            return breast_cancer
        else if(self._selected_dataset == 'gaussian'):
            return gaussian
        else if(self._selected_dataset == 'iris'):
            return iris
        else if(self._selected_dataset == 'wine'):
            return wine
        else 
            raise ValueError("Wrong dataset")


    def get_data(self):
        return self.X_train, self.y_train, self.X_test, self.y_test
