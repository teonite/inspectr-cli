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
    "rethinkdb_db": "inspectr"
})

# valid reporter configs
flake8_cfg = freeze({
    'type': 'flake8',
    'lint_paths': ['/dev/null']
})

django_test_cfg = freeze({
    "type": "django-test",
    "manage_path": "tools/manage.py",
    "test_modules": ["apps.core"]
})

coverage_django_test_cfg = freeze({
    "type": "coverage-django-test",
    "manage_path": "tools/manage.py",
    "test_modules": ["apps.core"]
})

coverage_py_cfg = freeze({
    'type': 'coverage-py'
})

eslint_cfg = freeze({
    "type": "eslint",
    "lint_paths": [
        "src/ng-app/project-app"
    ]
})

karma_cfg = freeze({
    "type": "karma",
    'karma_config': 'karma.conf.js'
})

karma_coverage_cfg = freeze({
    "type": "karma-coverage"
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
    for key in ['rethinkdb_host', 'rethinkdb_port', 'rethinkdb_db']:
        config = minimal_valid_connector_config.remove(key)
        with pytest.raises(SystemExit):
            validate_connector_config(thaw(config))


def test_flake8_config_success():
    config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(flake8_cfg))

    parsed = validate_and_parse_config(thaw(config))
    assert bool(parsed)
    assert parsed == config


def test_flake8_config_fail():
    for key in ['type', 'lint_paths']:
        invalid_reporter = flake8_cfg.remove(key)
        config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(invalid_reporter))
        with pytest.raises(SystemExit):
            validate_and_parse_config(thaw(config))


def test_django_test_config_success():
    config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(django_test_cfg))

    parsed = validate_and_parse_config(thaw(config))
    assert bool(parsed)
    assert parsed == config


def test_django_test_config_fail():
    for key in ['type']:
        invalid_reporter = django_test_cfg.remove(key)
        config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(invalid_reporter))
        with pytest.raises(SystemExit):
            validate_and_parse_config(thaw(config))


def test_django_test_config_defaults():
    tested_cfg = django_test_cfg
    for key in ['manage_path', 'test_modules']:
        missing_key_reporter = tested_cfg.remove(key)
        config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(missing_key_reporter))
        parsed = validate_and_parse_config(thaw(config))

        assert parsed['reporters'][0].get(key) is not None


def test_coverage_django_test_config_success():
    config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(coverage_django_test_cfg))

    parsed = validate_and_parse_config(thaw(config))
    assert bool(parsed)
    assert parsed == config


def test_coverage_django_test_config_fail():
    for key in ['type']:
        invalid_reporter = coverage_django_test_cfg.remove(key)
        config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(invalid_reporter))
        with pytest.raises(SystemExit):
            validate_and_parse_config(thaw(config))


def test_coverage_django_test_config_defaults():
    tested_cfg = coverage_django_test_cfg
    for key in ['manage_path', 'test_modules']:
        missing_key_reporter = tested_cfg.remove(key)
        config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(missing_key_reporter))
        parsed = validate_and_parse_config(thaw(config))

        assert parsed['reporters'][0].get(key) is not None


def test_coverage_py_config_success():
    config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(coverage_py_cfg))

    parsed = validate_and_parse_config(thaw(config))
    assert bool(parsed)
    assert parsed == config


def test_coverage_py_config_fail():
    for key in ['type']:
        invalid_reporter = coverage_py_cfg.remove(key)
        config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(invalid_reporter))
        with pytest.raises(SystemExit):
            validate_and_parse_config(thaw(config))


def test_eslint_config_success():
    config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(eslint_cfg))

    parsed = validate_and_parse_config(thaw(config))
    assert bool(parsed)
    assert parsed == config


def test_eslint_config_fail():
    for key in ['type', 'lint_paths']:
        invalid_reporter = eslint_cfg.remove(key)
        config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(invalid_reporter))
        with pytest.raises(SystemExit):
            validate_and_parse_config(thaw(config))


def test_karma_config_success():
    config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(karma_cfg))

    parsed = validate_and_parse_config(thaw(config))
    assert bool(parsed)
    assert parsed == config


def test_karma_config_fail():
    for key in ['type']:
        invalid_reporter = karma_cfg.remove(key)
        config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(invalid_reporter))
        with pytest.raises(SystemExit):
            validate_and_parse_config(thaw(config))


def test_karma_config_defaults():
    tested_cfg = karma_cfg
    for key in ['karma_config']:
        missing_key_reporter = tested_cfg.remove(key)
        config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(missing_key_reporter))
        parsed = validate_and_parse_config(thaw(config))

        assert parsed['reporters'][0].get(key) is not None


def test_karma_coverage_config_success():
    config = minimal_valid_config.transform(['reporters'], lambda reporters: reporters.append(karma_coverage_cfg))

    parsed = validate_and_parse_config(thaw(config))
    assert bool(parsed)
    assert parsed == config


def test_karma_coverage_config_fail():
    for key in ['type']:
        invalid_reporter = karma_coverage_cfg.remove(key)
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
    init_db('fake_connection', 'fake_db')

    db_create_stub.assert_called_once_with('fake_db')
    db_stub.assert_called_with('fake_db')


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
