from _pytest.fixtures import fixture

from base.Dataset import Dataset
from extended.IBMExecutor import IBMExecutor
from extended.LocalExecutor import LocalExecutor
from extended.QNNModel import QNNModel
from extended.QSVCModel import QSVCModel


@fixture
def simulator():
    return LocalExecutor('statevector', 1)


@fixture
def ibm():
    return IBMExecutor(
        '5fdc8febffc863044dd6a9595abbc9b49a87a1bc36a3869f2fe970493c17173b2eb591d52cf85f0e658084ffb4bfec9daf779f886f7042f23e819069b2957d64',
        1)


@fixture()
def dataset():
    return Dataset('ad_hoc_data')


def test_run_QNN_local(simulator, dataset):
    backend, quantum_instance = simulator.create_backend()
    qnn = QNNModel(dataset, quantum_instance, backend)
    try:
        output = qnn.run()
        assert True
    except:
        assert False


def test_run_QSVM_local(simulator, dataset):
    backend, quantum_instance = simulator.create_backend()
    qsvc = QSVCModel(dataset, quantum_instance, backend)
    try:
        output = qsvc.run()
        assert True
    except:
        assert False


def test_run_QNN_ibm(ibm, dataset):
    backend, quantum_instance = ibm.create_backend()
    qnn = QNNModel(dataset, quantum_instance, backend)
    try:
        output = qnn.run()
        assert True
    except:
        assert False


def test_run_QSVM_ibm(ibm, dataset):
    backend, quantum_instance = ibm.create_backend()
    qsvc = QSVCModel(dataset, quantum_instance, backend)
    try:
        output = qsvc.run()
        assert True
    except:
        assert False
