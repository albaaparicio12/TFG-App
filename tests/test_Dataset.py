from joblib.testing import fixture

from business.base.Dataset import Dataset
from qiskit_machine_learning.datasets import gaussian


@fixture
def datasets(mocker):
    mocker.patch('base.Dataset.Dataset.define_data', return_value=lambda x: None)
    wrong_dataset = Dataset('wrong')
    correct_dataset = Dataset('gaussian')
    ad_hoc_data_dataset = Dataset('ad_hoc_data')
    datasets = {'wrong': wrong_dataset, 'correct': correct_dataset, 'ad_hoc_data': ad_hoc_data_dataset}
    mocker.resetall()
    return datasets


def test_select_dataset_when_wrong_dataset(datasets):
    dataset = datasets['wrong']
    try:
        dataset.select_dataset()
        assert False
    except:
        assert True


def test_select_dataset_when_correct_dataset(datasets):
    dataset = datasets['correct']
    selected_dataset = dataset.select_dataset()

    assert selected_dataset is not None
    assert selected_dataset is gaussian


def test_define_data_when_wrong_dataset(datasets):
    dataset = datasets['wrong']
    try:
        dataset.define_data()
        assert False
    except:
        assert True


"""
def test_define_data_when_correct_dataset(datasets):
    dataset = datasets['correct']
    dataset.define_data()

    assert dataset.X_test is not None
    assert dataset.y_test is not None
    assert dataset.X_train is not None
    assert dataset.y_train is not None


def test_define_data_when_dataset_is_ad_hoc_data(datasets):
    dataset = datasets['ad_hoc_data']
    dataset.define_data()

    assert dataset.selected_dataset == 'ad_hoc_data'
    assert dataset.X_test is not None
    assert dataset.y_test is not None
    assert dataset.X_train is not None
    assert dataset.y_train is not None
"""
