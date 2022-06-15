from pylab import cm
from sklearn import metrics
from abc import ABC
from custom_inherit import  doc_inherit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import QuantumModel

# Package to evaluate model performance
from sklearn import metrics

from qiskit import QuantumCircuit

# Import a quantum feature map 
from qiskit.circuit.library import ZZFeatureMap

# Import the quantum kernel and the trainer
from qiskit_machine_learning.kernels import QuantumKernel
from qiskit_machine_learning.kernels.algorithms import QuantumKernelTrainer

# Import the optimizer for training the quantum kernel
from qiskit.algorithms.optimizers import SPSA

from qiskit_machine_learning.algorithms import QSVC, PegasosQSVC



seed = 10599
algorithm_globals.random_seed = seed

class QSVCModel(QuantumModel, ABC):

    def __init__(self, dataset, quantum_instance, n_executions, backend) -> None:
        
        super(QSVCModel, self).__init__(dataset, quantum_instance, n_executions, backend)
    
    
    @doc_inherit(QuantumModel.createModel, style="google")
    def run(self):
        # Get dataset
        X_train, y_train, X_test, y_test = self.dataset.get_data()

        # Define the Quantum Feature Map
        # Create a rotational layer to train. We will rotate each qubit the same amount.
        user_params = ParameterVector("θ", 1)
        fm0 = QuantumCircuit(2)
        fm0.ry(user_params[0], 0)
        fm0.ry(user_params[0], 1)

        # Use ZZFeatureMap to represent input data
        fm1 = ZZFeatureMap(2)

        # Create the feature map, composed of our two circuits
        fm = fm0.compose(fm1)

        print(circuit_drawer(fm))
        print(f"Trainable parameters: {user_params}")
        
        # Instantiate quantum kernel
        quantum_kernel = QuantumKernel(fm, user_parameters=user_params, quantum_instance=self._backend)

        """
        Since no analytical gradient is defined for kernel loss functions, gradient-based optimizers are not recommended for training kernels.
        """
        # Instantiate a quantum kernel trainer.
        qkt = QuantumKernelTrainer(
            quantum_kernel=quantum_kernel, loss="svc_loss", optimizer=SPSA(), initial_point=[np.pi / 2]
        )

        # Train the kernel using QKT directly
        qka_results = qkt.fit(X_train, y_train)
        optimized_kernel = qka_results.quantum_kernel
        print(qka_results)

        # Use QSVC for classification
        qsvc = QSVC(quantum_kernel=optimized_kernel)

        # Fit the QSVC
        qsvc.fit(X_train, y_train)

        # Predict the labels
        labels_test = qsvc.predict(X_test)

        # Evalaute the test accuracy
        accuracy_test = metrics.balanced_accuracy_score(y_true=y_test, y_pred=labels_test)
        print(f"accuracy test: {accuracy_test}")

        print(y_test)
        print(labels_test)
