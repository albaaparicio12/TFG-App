from qiskit.circuit import ParameterVector
from qiskit.visualization import circuit_drawer
from custom_inherit import doc_inherit
import numpy as np
from src.base.QuantumModel import QuantumModel

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


class QSVCModel(QuantumModel):

    def __init__(self, dataset, quantum_instance, backend) -> None:
        super(QSVCModel, self).__init__(dataset, quantum_instance, backend)

    @doc_inherit(QuantumModel.run, style="google")
    def run(self):
        output = {}
        # Get dataset
        X_train, y_train, X_test, y_test = self.dataset.get_data()

        # n_qubits will be the number of classes to clasify in the selected dataset
        n_qubits = 2

        # Define the Quantum Feature Map
        # Create a rotational layer to train. We will rotate each qubit the same amount.
        user_params = ParameterVector("θ", 1)
        fm0 = QuantumCircuit(n_qubits)
        for qubit in range(n_qubits):
            fm0.ry(user_params[0], qubit)

        # Use ZZFeatureMap to represent input data
        fm1 = ZZFeatureMap(n_qubits, reps=2)

        # Create the feature map, composed of our two circuits
        fm = fm0.compose(fm1)

        output['circuit'] = circuit_drawer(fm, style='mpl')
        output['parameters'] = f"Trainable parameters: {user_params}"
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
        output['qka_results'] = qka_results
        # Use QSVC for classification
        qsvc = QSVC(quantum_kernel=optimized_kernel)

        # Fit the QSVC
        qsvc.fit(X_train, y_train)

        # Predict the labels
        labels_test = qsvc.predict(X_test)

        # Evalaute the test accuracy
        accuracy_test = metrics.balanced_accuracy_score(y_true=y_test, y_pred=labels_test)
        print(f"accuracy test: {accuracy_test}")
        output['accuracy'] = f"accuracy test: {accuracy_test}"
        output['y_test'] = f"y expected: {y_test}"
        output['labels_test'] = f"y predicted: {labels_test}"
        print(y_test)
        print(labels_test)
        return output
