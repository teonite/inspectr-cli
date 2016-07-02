import pytest

from tests.fixtures import eslint_output_custom
from .fixtures import (flake8_output, unittest_output, coverage_output, eslint_output, eslint_output_noerrors, karma_output, karma_summary_fail_line,
                       karma_summary_success_line, karma_coverage_summary_line, coverage_output_small, pytest_output_success, pytest_output_fail)
from inspectr.parsers import (flake8_parser, unittest_parser, coverage_py_parser, eslint_parser, jasmine_parser,
                              extract_karma_coverage_summary, extract_jasmine_summary, karma_coverage_parser, pytest_parser)


def test_parse_flake8_output():
    parsed = flake8_parser(flake8_output, '')

    assert len(parsed['stdout'].split('\n')) == 8
    assert len(parsed['stderr'].split('\n')) == 1
    assert parsed['summary'] == {
        'total_errors': 6
    }


def test_parse_unittest_output():
    parsed = unittest_parser('', unittest_output)  # unittest pushes output to stderr
    assert len(parsed['stdout'].split('\n')) == 1
    assert len(parsed['stderr'].split('\n')) == 14
    assert parsed['summary'] == {
        'total_tests': 2,
        'failed_tests': 1
    }


def test_parse_unittest_output_unparsable():
    with pytest.raises(Exception):
        unittest_parser('', 'Unparsable string. Seriously, dont even try.')  # unittest pushes output to stderr


def test_parse_coverage_output():
    parsed = coverage_py_parser(coverage_output, '')
    assert len(parsed['stdout'].split('\n')) == 7
    assert len(parsed['stderr'].split('\n')) == 1
    assert parsed['summary'] == {
        'total_statements': 4572,
        'total_missing': 1673,
        'coverage_percent': 63
    }


def test_parse_coverage_output_unparsable():
    with pytest.raises(Exception):
        coverage_py_parser('Unparsable string. Seriously, dont even try.', '')


def test_parse_coverage_output_small():
    parsed = coverage_py_parser(coverage_output_small, '')
    assert len(parsed['stdout'].split('\n')) == 10
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'total_statements': 140,
        'total_missing': 97,
        'coverage_percent': 31
    }


def test_parse_pytest_output_success():
    parsed = pytest_parser(pytest_output_success, '')
    assert len(parsed['stdout'].split('\n')) == 10
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'passed_tests': 21,
        'failed_tests': 0,
    }


def test_parse_pytest_output_fail():
    parsed = pytest_parser(pytest_output_fail, '')
    assert len(parsed['stdout'].split('\n')) == 13
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'passed_tests': 38,
        'failed_tests': 4,
    }


def test_parse_pytest_ouput_unparsable():
    with pytest.raises(Exception):
        pytest_parser('Unparsable string. Seriously, dont even try.', '')


def test_parse_eslint_output():
    parsed = eslint_parser(eslint_output, '')
    assert len(parsed['stdout'].split('\n')) == 7
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'total_problems': 47,
        'total_errors': 5,
        'total_warnings': 42
    }


def test_parse_eslint_output_noerrors():
    parsed = eslint_parser(eslint_output_noerrors, '')
    assert len(parsed['stdout'].split('\n')) == 1
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'total_problems': 0,
        'total_errors': 0,
        'total_warnings': 0
    }


def test_parse_eslint_output_custom():
    parsed = eslint_parser(eslint_output_custom, '')
    assert len(parsed['stdout'].split('\n')) == 5
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'total_problems': 0,
        'total_errors': 0,
        'total_warnings': 0
    }


def test_parse_eslint_ouput_unparsable():
    with pytest.raises(Exception):
        eslint_parser('✖ Unparsable string.\nSeriously, dont even try.', '')


def test_parse_karma_output():
    parsed = jasmine_parser(karma_output, '')
    assert len(parsed['stdout'].split('\n')) == 22
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'total_tests': 1,
        'executed_tests': 1,
        'failed_tests': 0
    }


def test_parse_jasmine_ouput_unparsable():
    with pytest.raises(Exception):
        jasmine_parser('Unparsable string. Seriously, dont even try.', '')


def test_parse_karma_coverage_output():
    parsed = karma_coverage_parser('', '', [{'type': 'jasmine', 'stdout': karma_output}])
    assert len(parsed['stdout'].split('\n')) == 1
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'statements_percent': 4.82,
        'branches_percent': 0.43,
        'functions_percent': 0.78,
        'lines_percent': 4.91
    }


def test_parse_karma_coverage_ouput_unparsable():
    with pytest.raises(Exception):
        karma_coverage_parser('Unparsable string. Seriously, dont even try.', '')


def test_extract_karma_summary_fail():
    parsed = extract_jasmine_summary(karma_summary_fail_line)
    assert parsed == {
        'total_tests': 1,
        'executed_tests': 1,
        'failed_tests': 1
    }


def test_extract_karma_summary_success():
    parsed = extract_jasmine_summary(karma_summary_success_line)
    assert parsed == {
        'total_tests': 1,
        'executed_tests': 1,
        'failed_tests': 0
    }


def test_extract_coverage_summary():
    parsed = extract_karma_coverage_summary(karma_coverage_summary_line)

    assert parsed == {
        'statements_percent': 4.82,
        'branches_percent': 0.43,
        'functions_percent': 0.78,
        'lines_percent': 4.91
    }
