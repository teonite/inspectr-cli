import pytest

from .fixtures import (flake8_output, unittest_output, eslint_output_custom, mocha_success_output, mocha_fail_output, coverage_output,
                       eslint_output, eslint_output_noerrors, jasmine_output, jasmine_summary_fail_line, jasmine_summary_success_line,
                       karma_coverage_summary_line, coverage_output_small, pytest_output_success, pytest_output_fail, radon_maintainability_output,
                       coffeelint_output, jasmine_output_integers, radon_cyclomatic_complexity_output, tslint_output)
from inspectr.parsers import (flake8_parser, unittest_parser, coverage_py_parser, eslint_parser, jasmine_parser, radon_maintainability_parser,
                              extract_karma_coverage_summary, extract_jasmine_summary, karma_coverage_parser, pytest_parser, mocha_parser,
                              coffeelint_parser, radon_cyclomatic_complexity_parser, tslint_parser)


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
        'failed_tests': 1,
        'passed_tests': 1
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
        'total_tests': 21
    }


def test_parse_pytest_output_fail():
    parsed = pytest_parser(pytest_output_fail, '')
    assert len(parsed['stdout'].split('\n')) == 13
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'passed_tests': 38,
        'failed_tests': 4,
        'total_tests': 42
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
    parsed = jasmine_parser(jasmine_output, '')
    assert len(parsed['stdout'].split('\n')) == 22
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'total_tests': 1,
        'executed_tests': 1,
        'failed_tests': 0,
        'passed_tests': 1
    }


def test_parse_jasmine_ouput_unparsable():
    with pytest.raises(Exception):
        jasmine_parser('Unparsable string. Seriously, dont even try.', '')


def test_parse_karma_coverage_output():
    parsed = karma_coverage_parser('', '', [{'type': 'jasmine', 'stdout': jasmine_output}])
    assert len(parsed['stdout'].split('\n')) == 1
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'statements_percent': 4.82,
        'branches_percent': 0.43,
        'functions_percent': 0.78,
        'lines_percent': 4.91
    }


def test_parse_karma_coverage_output_integers():
    parsed = karma_coverage_parser('', '', [{'type': 'jasmine', 'stdout': jasmine_output_integers}])
    assert len(parsed['stdout'].split('\n')) == 1
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'statements_percent': 100,
        'branches_percent': 100,
        'functions_percent': 100,
        'lines_percent': 100
    }


def test_parse_karma_coverage_ouput_unparsable():
    with pytest.raises(Exception):
        karma_coverage_parser('Unparsable string. Seriously, dont even try.', '')


def test_extract_karma_summary_fail():
    parsed = extract_jasmine_summary(jasmine_summary_fail_line)
    assert parsed == {
        'total_tests': 1,
        'executed_tests': 1,
        'failed_tests': 1,
        'passed_tests': 0
    }


def test_extract_karma_summary_success():
    parsed = extract_jasmine_summary(jasmine_summary_success_line)
    assert parsed == {
        'total_tests': 1,
        'executed_tests': 1,
        'failed_tests': 0,
        'passed_tests': 1
    }


def test_extract_coverage_summary():
    parsed = extract_karma_coverage_summary(karma_coverage_summary_line)

    assert parsed == {
        'statements_percent': 4.82,
        'branches_percent': 0.43,
        'functions_percent': 0.78,
        'lines_percent': 4.91
    }


def test_parse_mocha_output_success():
    parsed = mocha_parser(mocha_success_output, '')
    assert len(parsed['stdout'].split('\n')) == 25
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'total_tests': 4,
        'passed_tests': 4,
        'failed_tests': 0,
    }


def test_parse_mocha_output_fail():
    parsed = mocha_parser(mocha_fail_output, '')
    assert len(parsed['stdout'].split('\n')) == 7
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'total_tests': 4,
        'passed_tests': 3,
        'failed_tests': 1
    }


def test_parse_mocha_ouput_unparsable():
    with pytest.raises(Exception):
        mocha_parser('Unparsable string. Seriously, dont even try.', '')


def test_radon_maintainability_output():
    parsed = radon_maintainability_parser(radon_maintainability_output, '')
    assert len(parsed['stdout'].split('\n')) == 11
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'A': 6,
        'B': 2,
        'C': 2,
        'total': 10
    }


def test_radon_maintainability_output_unparsable():
    with pytest.raises(Exception):
        radon_maintainability_parser('Unparsable string.\nSeriously, dont even try.', '')


def test_radon_cyclomatic_complexity():
    parsed = radon_cyclomatic_complexity_parser(radon_cyclomatic_complexity_output, '')

    assert len(parsed['stdout'].split('\n')) == 17
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'A': 11,
        'B': 2,
        'C': 0,
        'D': 0,
        'E': 0,
        'F': 0,
        'total': 13,
    }


def test_radon_cyclomatic_complexity_output_unparsable():
    with pytest.raises(Exception):
        radon_maintainability_parser('Unparsable string.\nSeriously, dont even try.', '')


def test_coffeelint_output():
    parsed = coffeelint_parser(coffeelint_output, '')
    assert len(parsed['stdout'].split('\n')) == 10
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'total_problems': 98,
        'total_errors': 98,
        'total_warnings': 0
    }


def test_coffeelint_output_output_unparsable():
    with pytest.raises(Exception):
        coffeelint_parser('Unparsable string. Seriously, dont even try.', '')


def test_parse_tslint_output():
    parsed = tslint_parser(tslint_output, '')

    assert len(parsed['stdout'].split('\n')) == 7
    assert parsed['summary'] == {
        'total_errors': 6
    }
