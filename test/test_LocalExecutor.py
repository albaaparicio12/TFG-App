from extended.LocalExecutor import LocalExecutor


def test_create_backend_not_exist():
    simulator = LocalExecutor('no existe', 10)
    try:
        simulator.create_backend()
        assert False
    except:
        assert True


def test_create_backend_is_aer_simulator():
    simulator = LocalExecutor('automatic', 10)
    backend, quantum_instance = simulator.create_backend()

    assert backend.options.method == 'automatic'
    assert quantum_instance.run_config.shots == 10


def test_create_backend_is_not_aer_simulator():
    simulator = LocalExecutor('statevector', 10)
    backend, quantum_instance = simulator.create_backend()

    assert backend.options.method == 'statevector'
    assert quantum_instance.run_config.shots == 10
