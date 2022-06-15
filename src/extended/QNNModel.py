from sklearn import metrics
import matplotlib.pyplot as plt
from qiskit_machine_learning.algorithms import NeuralNetworkClassifier
from qiskit_machine_learning.neural_networks import TwoLayerQNN
# Import the optimizer for training the quantum kernel
from qiskit.algorithms.optimizers import COBYLA
from IPython.display import clear_output
from src.base.QuantumModel import QuantumModel
from custom_inherit import doc_inherit


class QNNModel(QuantumModel):

    def __init__(self, dataset, quantum_instance, n_executions, backend) -> None:
        super(QNNModel, self).__init__(dataset, quantum_instance, n_executions, backend)

    @doc_inherit(QuantumModel.run, style="google")
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
        return accuracy_test
    
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


