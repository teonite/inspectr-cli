import subprocess

from inspectr.parsers import parse_pytest_output
from .parsers import parse_flake8_output, parse_eslint_output, parse_unittest_output, parse_coverage_output, parse_karma_output, parse_karma_coverage_output


def flake8_reporter(config, previous_reports):
    """
    Generates flake8 report object (dictionary) for python files in given directories.
    Requires flake8 in path.
    """
    process = subprocess.Popen(['flake8'] + config['lint_paths'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # FIXME: error handling
    flake8_result = parse_flake8_output(out.decode('utf-8'))
    return flake8_result


def django_test_reporter(config, previous_reports):
    """
    Generates unittest report object (dictionary) for given modules.
    """
    process = subprocess.Popen([config['manage_path'], 'test', '--noinput'] + config['test_modules'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # FIXME: error handling
    unittest_result = parse_unittest_output(err.decode('utf-8'))  # unittest pushes output to stderr
    return unittest_result


def coverage_django_test_reporter(config, previous_reports):
    """
    Generates unittest report object (dictionary). Runs through coverage.py so that
    subsequent coverage reporter can gather data. Requires coverage in path (coverage.py).
    """
    process = subprocess.Popen([
        'coverage', 'run',
        config['manage_path'], 'test', '--noinput'] + config['test_modules'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = process.communicate()
    # FIXME: error handling
    unittest_result = parse_unittest_output(err.decode('utf-8'))  # unittest pushes output to stderr

    return unittest_result


def pytest_reporter(config, previous_reports):
    """
    Generates unittest report object (dictionary) for given modules.
    """
    process = subprocess.Popen(['py.test'] + config['test_paths'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # FIXME: error handling
    pytest_result = parse_pytest_output(out.decode('utf-8'))
    return pytest_result


def coverage_pytest_reporter(config, previous_reports):
    """
    Generates unittest report object (dictionary). Runs through coverage.py so that
    subsequent coverage reporter can gather data. Requires coverage in path (coverage.py).
    """
    process = subprocess.Popen([
        'coverage', 'run',
        '-m', 'py.test'] + config['test_paths'],  # FIXME: coverage can't see py.test for some reason...
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = process.communicate()
    # FIXME: error handling
    pytest_result = parse_pytest_output(out.decode('utf-8'))
    return pytest_result


def coverage_py_reporter(config, previous_reports):
    """
    Generates test coverage report object (dictionary). Requires coverage in path (coverage.py).
    Must be invoked after one of coverage-report-generating reporters (like coverage_django_test_reporter).
    """
    process = subprocess.Popen(['coverage', 'report'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # FIXME: error handling
    coverage_result = parse_coverage_output(out.decode('utf-8'))

    return coverage_result


def eslint_reporter(config, previous_reports):
    """
    Generates eslint report object (dictionary) for javascript files in given directories.
    Requires eslint in path.
    """
    process = subprocess.Popen(['eslint'] + config['lint_paths'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # FIXME: error handling
    eslint_result = parse_eslint_output(out.decode('utf-8'))

    return eslint_result


def karma_reporter(config, previous_reports):
    """
    Generates karma report object (dictionary).
    Requires karma in path.
    """
    process = subprocess.Popen(['karma', 'start'] + [config['karma_config']] + ['--single-run'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # FIXME: error handling
    karma_result = parse_karma_output(out.decode('utf-8'))

    return karma_result


def karma_coverage_reporter(config, previous_reports):
    """
    Generates karma test coverage report object (dictionary). Depends on karma output and so
    has to be invoked after karma_reporter.
    """
    karma_result = [report for report in previous_reports if report['type'] == 'karma']
    if not karma_result:
        raise ValueError('karma-coverage reporter depends on karma reporter output, but no karma reports found.')

    return parse_karma_coverage_output('\n'.join(karma_result[0]['output']))
