import rethinkdb as r
from inspectr.utils import init_db, save_report, validate_and_parse_config


def test_init_db(monkeypatch, mocker):
    db_create_stub = mocker.stub('db_create')
    errors_stub = mocker.stub('errors')
    db_stub = mocker.stub('db')

    monkeypatch.setattr(r, 'db_create', db_create_stub)
    monkeypatch.setattr(r, 'errors', errors_stub)
    monkeypatch.setattr(r, 'db', db_stub)
    init_db('fake_connection', 'fake_db')

    db_create_stub.assert_called_once_with('fake_db')
    db_stub.assert_called_with('fake_db')


def test_validate_and_parse_config():
    config_dict = {
        "project_name": "test_project",

        "rethinkdb_host": "localhost",
        "rethinkdb_port": 28015,
        "rethinkdb_db": "inspectr",

        "reporters": []
    }

    config = validate_and_parse_config(config_dict)
    assert config


def test_save_report(monkeypatch, mocker):
    db_create_stub = mocker.stub('db_create')
    errors_stub = mocker.stub('errors')
    db_stub = mocker.stub('db')
    connect_stub = mocker.stub('connect')

    monkeypatch.setattr(r, 'db_create', db_create_stub)
    monkeypatch.setattr(r, 'errors', errors_stub)
    monkeypatch.setattr(r, 'db', db_stub)
    monkeypatch.setattr(r, 'connect', connect_stub)
    save_report({'project_name': 'fake_name'}, host='fake_host', port='fake_port', db='fake_db')

    db_create_stub.assert_called_once_with('fake_db')
    db_stub.assert_called_with('fake_db')
    connect_stub.assert_called_with('fake_host', 'fake_port')
