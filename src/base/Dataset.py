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
    def train_features(self):
        return self._train_features
    
    @property
    def train_labels(self):
        return self._train_labels
    
    @property
    def test_features(self):
        return self._test_features
    
    @property
    def test_labels(self):
        return self._test_labels


    def define_data(self):
        train_features, train_labels, test_features, test_labels = self.get_dataset(
        training_size=20,
        test_size=10,
        n=2,
        plot_data=True)

        self._train_features = train_features
        self._train_labels = train_labels
        self._test_features = test_features
        self._test_labels = test_labels


    def get_dataset(self):
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



