import matplotlib.pyplot as plt
import numpy as np
from qiskit import BasicAer
# import the feature map and ansatz circuits
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.utils import QuantumInstance, algorithm_globals
from qiskit_machine_learning.datasets import ad_hoc_data
from qiskit_machine_learning.algorithms import NeuralNetworkClassifier
from qiskit.providers.basicaer import QasmSimulatorPy
# import the optimizer for the training
from qiskit.algorithms.optimizers import GradientDescent
# import backend
from qiskit import BasicAer

import QuantumModel
from abc import ABC
from custom_inherit import  doc_inherit

seed = 10599
algorithm_globals.random_seed = seed

class QNNModel(QuantumModel, ABC):

    def __init__(self, X_train, y_train, X_test, y_test, quantum_instance, n_executions) -> None:
        
        super(QNNModel, self).__init__(X_train, y_train, X_test, y_test, quantum_instance, n_executions)
    

    @doc_inherit(QuantumModel.createModel, style="google")
    def createModel(self):
    
    @doc_inherit(QuantumModel.createModel, style="google")
    def run(self):
        # Get dataset
        X_train, y_train, X_test, y_test = self.dataset.get_data()
        
        num_qubits = 2        
        opflow_qnn = TwoLayerQNN(num_qubits, quantum_instance=self._quantum_instance)

        # construct neural network classifier
        opflow_classifier = NeuralNetworkClassifier(opflow_qnn, optimizer=COBYLA(), callback=callback_graph)

        # create empty array for callback to store evaluations of the objective function
        objective_func_vals = []
        plt.rcParams["figure.figsize"] = (12, 6)

        # fit classifier to data
        opflow_classifier.fit(X_train, y_train)

        # return to default figsize
        plt.rcParams["figure.figsize"] = (6, 4)

        # Predict the labels
        labels_test = opflow_classifier.predict(X_test)

        # Evalaute the test accuracy
        accuracy_test = metrics.balanced_accuracy_score(y_true=y_test, y_pred=labels_test)
        print(f"accuracy test: {accuracy_test}")

    
    def callback_graph(weights, obj_func_eval):
        """
        Callback function that draws a live plot when the .fit() method is called
        """
        clear_output(wait=True)
        objective_func_vals.append(obj_func_eval)
        plt.title("Objective function value against iteration")
        plt.xlabel("Iteration")
        plt.ylabel("Objective function value")
        plt.plot(range(len(objective_func_vals)), objective_func_vals)
        plt.show()


