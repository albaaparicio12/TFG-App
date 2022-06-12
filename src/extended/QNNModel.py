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

    def __init__(self, train_features, train_labels, test_features, test_labels, quantum_instance, n_executions) -> None:
        
        super(QNNModel, self).__init__(train_features, train_labels, test_features, test_labels, quantum_instance, n_executions)
    

    @doc_inherit(QuantumModel.createModel, style="google")
    def createModel(self):
    
    @doc_inherit(QuantumModel.createModel, style="google")
    def run(self):


# define data (input array X, target labels y)
train_features, train_labels, test_features, test_labels, adhoc_total = ad_hoc_data(
    training_size=20,
    test_size=10,
    n=2,
    gap=0.3,
    plot_data=False,
    include_sample_total=True)

plt.figure(figsize=(5, 5))
plt.ylim(0, 2 * np.pi)
plt.xlim(0, 2 * np.pi)
plt.imshow(
    np.asmatrix(adhoc_total).T,
    interpolation="nearest",
    origin="lower",
    cmap="RdBu",
    extent=[0, 2 * np.pi, 0, 2 * np.pi],
)

plt.scatter(
    train_features[np.where(train_labels[:] == 0), 0],
    train_features[np.where(train_labels[:] == 0), 1],
    marker="s",
    facecolors="w",
    edgecolors="b",
    label="A train",
)
plt.scatter(
    train_features[np.where(train_labels[:] == 1), 0],
    train_features[np.where(train_labels[:] == 1), 1],
    marker="o",
    facecolors="w",
    edgecolors="r",
    label="B train",
)
plt.scatter(
    test_features[np.where(test_labels[:] == 0), 0],
    test_features[np.where(test_labels[:] == 0), 1],
    marker="s",
    facecolors="b",
    edgecolors="w",
    label="A test",
)
plt.scatter(
    test_features[np.where(test_labels[:] == 1), 0],
    test_features[np.where(test_labels[:] == 1), 1],
    marker="o",
    facecolors="r",
    edgecolors="w",
    label="B test",
)

plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
plt.title("Ad hoc dataset for classification")

plt.show()


# construct classifier
num_qubits = 2

backend = BasicAer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, shots=1024, seed_simulator=seed, seed_transpiler=seed)

vqc = VQC(feature_map=ZZFeatureMap(num_qubits), 
          ansatz=RealAmplitudes(num_qubits, reps=1), 
          loss='cross_entropy', 
          optimizer=GradientDescent(),
          quantum_instance=quantum_instance)

# train classifier
vqc.fit(train_features, train_labels)

# score result
vqc.score(train_features, train_labels)



from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.compiler import transpile, assemble

try:
    IBMQ.save_account('bfa0617401f012009b10cb8eedcc55e5639c63220c2f7c62920a8ed53280394c0f4025eedccfb9a5b04d52f89d7a3d42526d5f5dd90e517db7c79b5b4686e76f', overwrite=True)
    IBMQ.load_account()
except:
    return("Invalid token")

provider = IBMQ.get_provider(hub = 'ibm-q')

num_qubits = 2

available_devices = provider.backends(filters=lambda x: x.configuration().n_qubits >= n_qubits
                                    and not x.configuration().simulator
                                    and x.status().operational==True)

device = least_busy(available_devices)

quantum_instance = QuantumInstance(device, shots=1024, seed_simulator=seed, seed_transpiler=seed)

vqc = VQC(feature_map=ZZFeatureMap(num_qubits), 
          ansatz=RealAmplitudes(num_qubits, reps=1), 
          loss='cross_entropy', 
          optimizer=GradientDescent(),
          quantum_instance=quantum_instance)

# train classifier
vqc.fit(train_features, train_labels)

# score result
vqc.score(train_features, train_labels)


# In[ ]:




