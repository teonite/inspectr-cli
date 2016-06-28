from .fixtures import (flake8_output, unittest_output, coverage_output, eslint_output, karma_output, karma_summary_fail_line,
                       karma_summary_success_line, karma_coverage_summary_line, coverage_output_small, pytest_output_success, pytest_output_fail)
from inspectr.parsers import (parse_flake8_output, parse_unittest_output, parse_coverage_output, parse_eslint_output, parse_karma_output,
                              extract_karma_coverage_summary, extract_karma_summary, parse_karma_coverage_output, parse_pytest_output)


def test_parse_flake8_output():
    parsed = parse_flake8_output(flake8_output, '')

    assert len(parsed['stdout'].split('\n')) == 8
    assert len(parsed['stderr'].split('\n')) == 1
    assert parsed['summary'] == {
        'total_errors': 6
    }


def test_parse_unittest_output():
    parsed = parse_unittest_output('', unittest_output)  # unittest pushes output to stderr
    assert len(parsed['stdout'].split('\n')) == 1
    assert len(parsed['stderr'].split('\n')) == 14
    assert parsed['summary'] == {
        'total_tests': 2,
        'failed_tests': 1
    }


def test_parse_unittest_output_unparsable():
    parsed = parse_unittest_output('', 'Unparsable string. Seriously, dont even try.')  # unittest pushes output to stderr
    assert len(parsed['stdout'].split('\n')) == 1
    assert len(parsed['stderr'].split('\n')) == 1
    assert parsed['summary'] is None


def test_parse_coverage_output():
    parsed = parse_coverage_output(coverage_output, '')
    assert len(parsed['stdout'].split('\n')) == 7
    assert len(parsed['stderr'].split('\n')) == 1
    assert parsed['summary'] == {
        'total_statements': 4572,
        'total_missing': 1673,
        'coverage_percent': 63
    }


def test_parse_coverage_output_unparsable():
    parsed = parse_coverage_output('Unparsable string. Seriously, dont even try.', '')
    assert len(parsed['stdout'].split('\n')) == 1
    assert len(parsed['stderr'].split('\n')) == 1
    assert parsed['summary'] is None


def test_parse_coverage_output_small():
    parsed = parse_coverage_output(coverage_output_small, '')
    assert len(parsed['stdout'].split('\n')) == 10
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'total_statements': 140,
        'total_missing': 97,
        'coverage_percent': 31
    }


def test_parse_pytest_output_success():
    parsed = parse_pytest_output(pytest_output_success, '')
    assert len(parsed['stdout'].split('\n')) == 10
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'passed_tests': 21,
        'failed_tests': 0,
    }


def test_parse_pytest_output_fail():
    parsed = parse_pytest_output(pytest_output_fail, '')
    assert len(parsed['stdout'].split('\n')) == 13
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'passed_tests': 38,
        'failed_tests': 4,
    }


def test_parse_pytest_ouput_unparsable():
    parsed = parse_pytest_output('Unparsable string. Seriously, dont even try.', '')
    assert len(parsed['stdout'].split('\n')) == 1
    assert len(parsed['stderr'].split('\n')) == 1
    assert parsed['summary'] is None


def test_parse_eslint_output():
    parsed = parse_eslint_output(eslint_output, '')
    assert len(parsed['stdout'].split('\n')) == 7
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'total_problems': 47,
        'total_errors': 5,
        'total_warnings': 42
    }


def test_parse_eslint_ouput_unparsable():
    parsed = parse_eslint_output('Unparsable string. Seriously, dont even try.', '')
    assert len(parsed['stdout'].split('\n')) == 1
    assert len(parsed['stderr'].split('\n')) == 1
    assert parsed['summary'] is None


def test_parse_karma_output():
    parsed = parse_karma_output(karma_output, '')
    assert len(parsed['stdout'].split('\n')) == 22
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'total_tests': 1,
        'executed_tests': 1,
        'failed_tests': 0
    }


def test_parse_karma_ouput_unparsable():
    parsed = parse_karma_output('Unparsable string. Seriously, dont even try.', '')
    assert len(parsed['stdout'].split('\n')) == 1
    assert len(parsed['stderr'].split('\n')) == 1
    assert parsed['summary'] is None


def test_parse_karma_coverage_output():
    parsed = parse_karma_coverage_output(karma_output, '')
    assert len(parsed['stdout'].split('\n')) == 22
    assert len(parsed['stderr'].split('\n')) == 1

    assert parsed['summary'] == {
        'statements_percent': 4.82,
        'branches_percent': 0.43,
        'functions_percent': 0.78,
        'lines_percent': 4.91
    }


def test_parse_karma_coverage_ouput_unparsable():
    parsed = parse_karma_coverage_output('Unparsable string. Seriously, dont even try.', '')
    assert len(parsed['stdout'].split('\n')) == 1
    assert len(parsed['stderr'].split('\n')) == 1
    assert parsed['summary'] is None


def test_extract_karma_summary_fail():
    parsed = extract_karma_summary(karma_summary_fail_line)
    assert parsed == {
        'total_tests': 1,
        'executed_tests': 1,
        'failed_tests': 1
    }


def test_extract_karma_summary_success():
    parsed = extract_karma_summary(karma_summary_success_line)
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
