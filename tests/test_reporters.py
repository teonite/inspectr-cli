from .mocks import flake8_output, unittest_output, coverage_output, eslint_output, karma_output
from inspectr.reporters import django_unittest_reporter, django_unittest_coverage_reporter, flake8_reporter, eslint_reporter, karma_reporter, karma_coverage_reporter
import subprocess


class Process(object):
    """
    Mock process returning appropriate outputs for each command invoked by reporters.
    """
    def __init__(self, command, *args):
        self.command = command

    def communicate(self):
        if self.command[0] == 'flake8':
            return bytes(flake8_output, 'utf-8'), ''
        if self.command[:2] == ['coverage', 'run']:
            return '', bytes(unittest_output, 'utf-8')
        if self.command[0] == 'manage.py':
            return '', bytes(unittest_output, 'utf-8')
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


def test_django_unittest_reporter(monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', mockpopen)

    report = django_unittest_reporter({
        'manage_path': 'manage.py',
        'test_modules': []
    }, [])

    assert bool(report)  # detailed testing in test_parsers.py


def test_django_unittest_coverage_reporter(monkeypatch):
    monkeypatch.setattr(subprocess, 'Popen', mockpopen)

    report = django_unittest_coverage_reporter({
        'manage_path': 'manage.py',
        'test_modules': []
    }, [])

    assert bool(report)  # detailed testing in test_parsers.py


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
