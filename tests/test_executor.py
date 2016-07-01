import subprocess

from inspectr.executor import execute


class Process(object):
    """
    Mock process returning fixture defined in constructor. Used as return value of monkeypatched
    subprocess.Popen to prevent real subprocess creation during tests.
    """
    def __init__(self, stdout_fixture, stderr_fixture):
        self.stdout_fixture = stdout_fixture
        self.stderr_fixture = stderr_fixture

    def communicate(self):
        return self.stdout_fixture.encode('utf-8'), self.stderr_fixture.encode('utf-8')


def get_mock_popen(stdout_fixture, stderr_fixture):
    return lambda *args, **kwargs: Process(stdout_fixture, stderr_fixture)


def test_execute(monkeypatch, mocker):
    mock_popen = get_mock_popen('stdout', 'stderr')
    monkeypatch.setattr(subprocess, 'Popen', mock_popen)
    mocker.spy(subprocess, 'Popen')

    stdout, stderr = execute('commmand')
    assert (stdout, stderr) == ('stdout', 'stderr')
    assert subprocess.Popen.call_count == 1


def test_execute_none(monkeypatch, mocker):
    mock_popen = get_mock_popen('stdout', 'stderr')
    monkeypatch.setattr(subprocess, 'Popen', mock_popen)
    mocker.spy(subprocess, 'Popen')

    stdout, stderr = execute(None)
    assert (stdout, stderr) == ('', '')
    assert subprocess.Popen.call_count == 0
