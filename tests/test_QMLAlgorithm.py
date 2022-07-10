from business.base.QMLAlgorithm import QMLAlgorithm
from extended.QNNModel import QNNModel
from extended.QSVCModel import QSVCModel

TOKEN = "5fdc8febffc863044dd6a9595abbc9b49a87a1bc36a3869f2fe970493c17173b2eb591d52cf85f0e658084ffb4bfec9daf779f886f7042f23e819069b2957d64"


def test_create_quantum_instance_local():
    qml = QMLAlgorithm(None, 'local', None, 1, 'statevector')
    backend, quantum_instance = qml.create_quantum_instance(None)
    assert backend.options.method == 'statevector'
    assert quantum_instance.run_config.shots == 1


def test_create_quantum_instance_ibm():
    qml = QMLAlgorithm(None, 'ibm', None, 1, None)
    backend, quantum_instance = qml.create_quantum_instance(TOKEN)
    assert backend.configuration().n_qubits >= 2
    assert backend.configuration().simulator == False
    assert backend.status().operational == True
    assert quantum_instance.run_config.shots == 1


def test_create_quantum_instance_other():
    qml = QMLAlgorithm(None, 'other', None, 1, 'statevector')
    try:
        qml.create_quantum_instance(TOKEN)
        assert False
    except:
        assert True


def create_quantum_model_qsvm():
    qml = QMLAlgorithm('ad_hoc_data', 'local', 'qsvm', 1, 'statevector')
    QModel = qml.create_quantum_model(None)
    assert QModel is QSVCModel


def create_quantum_model_qnn():
    qml = QMLAlgorithm('ad_hoc_data', 'local', 'qnn', 1, 'statevector')
    QModel = qml.create_quantum_model(None)
    assert QModel is QNNModel


def create_quantum_model_other():
    qml = QMLAlgorithm('ad_hoc_data', 'local', 'otro', 1, 'statevector')
    try:
        qml.create_quantum_model(None)
        assert False
    except:
        assert True


def test_run_local():
    qml = QMLAlgorithm('ad_hoc_data', 'local', 'qnn', 1, 'statevector')
    try:
        qml.run(None)
        assert True
    except:
        assert False


def test_run_ibm():
    qml = QMLAlgorithm('ad_hoc_data', 'ibm', 'qnn', 1, 'statevector')
    try:
        qml.run(TOKEN)
        assert True
    except:
        assert False
