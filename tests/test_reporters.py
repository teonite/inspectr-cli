import subprocess

from tests.fixtures import pytest_output_success
from .fixtures import flake8_output, unittest_output, coverage_output, eslint_output, karma_output
from inspectr.reporters import (django_test_reporter, flake8_reporter, eslint_reporter, karma_reporter,
                                karma_coverage_reporter, coverage_django_test_reporter, coverage_py_reporter, pytest_reporter, coverage_pytest_reporter)


class Process(object):
    """
    Mock process returning appropriate outputs for each command invoked by reporters.
    """
    def __init__(self, command, *args):
        self.command = command

    def communicate(self):
        if self.command[0] == 'flake8':
            return bytes(flake8_output, 'utf-8'), ''
        if self.command[:3] == ['coverage', 'run', 'manage.py']:
            return '', bytes(unittest_output, 'utf-8')
        if self.command[:4] == ['coverage', 'run', '-m', 'py.test']:
            return bytes(pytest_output_success, 'utf-8'), ''
        if self.command[0] == 'manage.py':
            return '', bytes(unittest_output, 'utf-8')
        if self.command[0] == 'py.test':
            return bytes(pytest_output_success, 'utf-8'), ''
        if self.command[:2] == ['coverage', 'report']:
            return bytes(coverage_output, 'utf-8'), ''
        if self.command[0] == 'eslint':
            return bytes(eslint_output, 'utf-8'), ''
        if self.command[0] == 'karma':
            return bytes(karma_output, 'utf-8'), ''

        assert False


def mockpopen(*args, **kwargs):
    return Process(args[0], *args[1:])


def test_flake8_reporter(monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', mockpopen)

    report = flake8_reporter({
        'lint_paths': []
    }, [])

    assert bool(report)  # detailed testing in test_parsers.py


def test_django_test_reporter(monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', mockpopen)

    report = django_test_reporter({
        'manage_path': 'manage.py',
        'test_modules': []
    }, [])

    assert bool(report)  # detailed testing in test_parsers.py


def test_coverage_django_test_reporter(monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', mockpopen)

    report = coverage_django_test_reporter({
        'manage_path': 'manage.py',
        'test_modules': []
    }, [])

    assert bool(report)  # detailed testing in test_parsers.py


def test_pytest_reporter(monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', mockpopen)

    report = pytest_reporter({'test_paths': []}, [])

    assert bool(report)  # detailed testing in test_parsers.py


def test_coverage_pytest_reporter(monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', mockpopen)

    report = coverage_pytest_reporter({'test_paths': []}, [])

    assert bool(report)  # detailed testing in test_parsers.py


def test_coverage_py_reporter(monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', mockpopen)

    report = coverage_py_reporter({}, [])

    assert bool(report)


def test_eslint_reporter(monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', mockpopen)

    report = eslint_reporter({
        'lint_paths': []
    }, [])

    assert bool(report)  # detailed testing in test_parsers.py


def test_karma_reporter(monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', mockpopen)

    report = karma_reporter({
        'karma_config': ['karma.conf.js']
    }, [])

    assert bool(report)  # detailed testing in test_parsers.py


def test_karma_coverage_reporter(monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', mockpopen)

    # get karma report to extract coverage
    report = karma_reporter({
        'karma_config': ['karma.conf.js']
    }, [])
    report['type'] = 'karma'
    report = karma_coverage_reporter({}, [report])

    assert bool(report)  # detailed testing in test_parsers.py
