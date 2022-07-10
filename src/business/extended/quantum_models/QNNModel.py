from sklearn import metrics
import matplotlib.pyplot as plt
from qiskit_machine_learning.algorithms import NeuralNetworkClassifier
from qiskit_machine_learning.neural_networks import TwoLayerQNN
# Import the optimizer for training the quantum kernel
from IPython.display import clear_output
from business.base.QuantumModel import QuantumModel
from custom_inherit import doc_inherit
# Import a quantum feature map
from qiskit.circuit.library import ZZFeatureMap
from qiskit.algorithms.optimizers import SPSA, GradientDescent


class QNNModel(QuantumModel):

    def __init__(self, dataset, quantum_instance, backend) -> None:
        super(QNNModel, self).__init__(dataset, quantum_instance, backend)
        # create empty array for callback to store evaluations of the objective function
        self._objective_func_vals = []

    @property
    def objective_func_vals(self):
        return self._objective_func_vals

    @doc_inherit(QuantumModel.run, style="google")
    def run(self):
        output = {}
        # Get dataset
        X_train, y_train, X_test, y_test = self.dataset.get_data()

        n_qubits = 2

        fm = ZZFeatureMap(n_qubits, reps=2)
        opflow_qnn = TwoLayerQNN(n_qubits, feature_map=fm, quantum_instance=self._quantum_instance)
        fm.decompose().draw(output="mpl", filename='./static/files/circuit.png')

        # construct neural network classifier
        opflow_classifier = NeuralNetworkClassifier(opflow_qnn, optimizer=SPSA(maxiter=30),
                                                    callback=self.callback_graph)

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
        output['accuracy'] = f"Porcentaje de exactitud: {accuracy_test * 100}%"
        output['y_test'] = f"Valores reales: {y_test}"
        output['labels_test'] = f"Valores predecidos: {self.print_predicted(labels_test)}"
        return output

    @staticmethod
    def print_predicted(labels) -> list:
        result = ""
        for item in labels:
            if item[0] < 0:
                result += "0 "
            else:
                result += "1 "
        return [result]

    def callback_graph(self, _, obj_func_eval):
        """
        Callback function that draws a live plot when the .fit() method is called
        """

        clear_output(wait=True)
        self.objective_func_vals.append(obj_func_eval)
        plt.title("Objective function value against iteration")
        plt.xlabel("Iteration")
        plt.ylabel("Objective function value")
        plt.plot(range(len(self.objective_func_vals)), self.objective_func_vals)
        plt.savefig('./static/files/grafo.png')
        plt.show()
