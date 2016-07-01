from pyrsistent import freeze, thaw
import rethinkdb as r
import pytest
from inspectr.utils import init_db, save_report, validate_and_parse_config, validate_connector_config


minimal_valid_config = freeze({
    "project_name": "Project",
    "reporters": []
})

minimal_valid_connector_config = freeze({
    "rethinkdb_host": "localhost",
    "rethinkdb_port": 28015,
    "rethinkdb_db": "inspectr",

    # https://github.com/rethinkdb/horizon/issues/498
    "reports_table": "reports_1234",
    "reports_history_table": "reports_history_4321"
})

valid_reporter_config = freeze({
    'type': 'flake8',
    'command': ['flake8 app/']
})


def test_validate_minimal_config():
    parsed = validate_and_parse_config(minimal_valid_config)
    assert bool(parsed)
    assert parsed == minimal_valid_config


def test_validate_minimal_config_fail():
    for key in ['project_name', 'reporters']:
        config = minimal_valid_config.remove(key)
        with pytest.raises(SystemExit):
            validate_and_parse_config(thaw(config))


def test_validate_minimal_connector_config():
    parsed = validate_connector_config(minimal_valid_connector_config)
    assert bool(parsed)
    assert parsed == minimal_valid_connector_config


def test_validate_minimal_connector_config_fail():
    for key in ['rethinkdb_host', 'rethinkdb_port', 'rethinkdb_db', "reports_table", "reports_history_table"]:
        config = minimal_valid_connector_config.remove(key)
        with pytest.raises(SystemExit):
            validate_connector_config(thaw(config))


def test_config_with_reporters_success():
    config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(valid_reporter_config))

    parsed = validate_and_parse_config(thaw(config))
    assert bool(parsed)
    assert parsed == config


def test_config_with_reporters_fail():
    for key in ['type', 'command']:
        invalid_reporter = valid_reporter_config.remove(key)
        config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(invalid_reporter))
        with pytest.raises(SystemExit):
            validate_and_parse_config(thaw(config))


def test_init_db(monkeypatch, mocker):
    db_create_stub = mocker.stub('db_create')
    errors_stub = mocker.stub('errors')
    db_stub = mocker.stub('db')

    monkeypatch.setattr(r, 'db_create', db_create_stub)
    monkeypatch.setattr(r, 'errors', errors_stub)
    monkeypatch.setattr(r, 'db', db_stub)
    init_db('fake_connection', minimal_valid_connector_config)

    db_create_stub.assert_called_once_with(minimal_valid_connector_config['rethinkdb_db'])
    db_stub.assert_called_with(minimal_valid_connector_config['rethinkdb_db'])


def test_save_report(monkeypatch, mocker):
    db_create_stub = mocker.stub('db_create')
    errors_stub = mocker.stub('errors')
    db_stub = mocker.stub('db')
    connect_stub = mocker.stub('connect')

    monkeypatch.setattr(r, 'db_create', db_create_stub)
    monkeypatch.setattr(r, 'errors', errors_stub)
    monkeypatch.setattr(r, 'db', db_stub)
    monkeypatch.setattr(r, 'connect', connect_stub)
    save_report({'project_name': 'fake_name'}, minimal_valid_connector_config)

    db_create_stub.assert_called_once_with(minimal_valid_connector_config['rethinkdb_db'])
    db_stub.assert_called_with(minimal_valid_connector_config['rethinkdb_db'])
    connect_stub.assert_called_with(
        minimal_valid_connector_config['rethinkdb_host'],
        minimal_valid_connector_config['rethinkdb_port']
    )
