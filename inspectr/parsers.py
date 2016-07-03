# -*- coding: utf-8 -*-
import re


def flake8_parser(stdout, stderr, previous_reports=None):
    lines = stdout.split('\n')
    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': {
            'total_errors': max(0, len(lines) - 2)
        }
    }


def unittest_parser(stdout, stderr, previous_reports=None):
    """
    Example total_line: u'Ran 2 tests in 0.396s'
    Example fail status line: u'FAILED (failures=17)'
    """
    lines = stderr.split('\n')  # unittest pushes output to stderr
    total_line, status_line = lines[-4:-1:2]

    total_tests = int(total_line.split()[1])
    failed_tests = 0 if status_line.startswith('OK') else int(status_line.split('=')[1][:-1])
    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': {
            'total_tests': total_tests,
            'failed_tests': failed_tests
        }
    }


def coverage_py_parser(stdout, stderr, previous_reports=None):
    lines = stdout.split('\n')
    summary_line = ' '.join(lines[-2].split())  # remove duplicate spaces
    total_statements, total_missing, coverage_percent = summary_line.split()[1:]

    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': {
            'total_statements': int(total_statements),
            'total_missing': int(total_missing),
            'coverage_percent': int(coverage_percent[:-1])
        }
    }


def pytest_parser(stdout, stderr, previous_reports=None):
    """
    Example fail summary_line: =========== 4 failed, 38 passed in 0.10 seconds =============
    Example success summary_line: ========= 21 passed in 0.05 seconds =========
    """
    lines = stdout.split('\n')
    summary_line = lines[-2].split()

    if summary_line[2].lower() == 'passed':
        passed_tests = int(summary_line[1])
        failed_tests = 0
    else:
        passed_tests = int(summary_line[3])
        failed_tests = int(summary_line[1])

    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': {
            'passed_tests': passed_tests,
            'failed_tests': failed_tests
        }
    }


def eslint_parser(stdout, stderr, previous_reports=None):
    lines = stdout.split('\n')
    eslint_summary_regex = r'^✖.*'
    summary_lines = [line for line in lines if re.search(eslint_summary_regex, line)]
    if not summary_lines:
        # no summary, no errors
        return {
            'stdout': stdout,
            'stderr': stderr,
            'summary': {
                'total_problems': 0,
                'total_errors': 0,
                'total_warnings': 0
            }
        }
    summary_line = summary_lines[-1].split()

    # example summary line: u'✖ 1767 problems (120 errors, 1647 warnings)'
    total_problems, total_errors, total_warnings = int(summary_line[1]), int(summary_line[3][1:]), int(summary_line[5])

    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': {
            'total_problems': total_problems,
            'total_errors': total_errors,
            'total_warnings': total_warnings
        }
    }


def extract_jasmine_summary(line):
    """
    Example SUCCESS karma summary line:
    PhantomJS 2.1.1 (Linux 0.0.0): Executed 1 of 1 SUCCESS (0.205 secs / 0.001 secs)
    Exmaple FAIL karma summary line:
    PhantomJS 2.1.1 (Linux 0.0.0): Executed 1 of 1 (1 FAILED) ERROR (0.21 secs / 0.001 secs)
    """
    # get totals
    totals = line.split(' Executed ')[1].split(' ')
    executed_tests, total_tests = int(totals[0]), int(totals[2])

    # get failed
    if 'SUCCESS' in line:
        failed_tests = 0
    else:
        failed_tests = int(totals[3][1:])

    return {
        'total_tests': total_tests,
        'executed_tests': executed_tests,
        'failed_tests': failed_tests
    }


def extract_karma_coverage_summary(line):
    """
    Example coverage summary line (table row):
    All files          |     4.82 |     0.43 |     0.78 |     4.91 |                |
    """
    totals = line.replace(' ', '').split('|')
    statements_percent, branches_percent, functions_percent, lines_percent = [float(t) for t in totals[1:5]]
    return {
        'statements_percent': statements_percent,
        'branches_percent': branches_percent,
        'functions_percent': functions_percent,
        'lines_percent': lines_percent
    }


def jasmine_parser(stdout, stderr, previous_reports=None):
    lines = stdout.split('\n')
    jasmine_summary_regex = r'\(.+\): Executed \d+ of \d+ (SUCCESS|\(\d+ FAILED\)( ERROR)?) \(.+ secs / .+ secs\)'

    jasmine_summary = None
    summary_lines = [line for line in lines if re.search(jasmine_summary_regex, line)]
    for line in summary_lines:
        jasmine_summary = extract_jasmine_summary(line)

    if jasmine_summary is None:
        raise ValueError('Karma summary line not found in input: %s' % stdout)

    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': jasmine_summary
    }


def karma_coverage_parser(stdout, stderr, previous_reports=None):
    reports = [report for report in previous_reports if report['type'] in ['jasmine', 'mocha']]
    for report in reports:
        lines = report['stdout'].split('\n')

        coverage_summary_regex = r'All files\s*\|\s*\d+\.\d+\s*\|\s*\d+\.\d+\s*\|\s*\d+\.\d+\s*\|\s*\d+\.\d+\s*\|\s*\|'

        coverage_summary = None
        summary_lines = [line for line in lines if re.search(coverage_summary_regex, line)]
        for line in summary_lines:
            coverage_summary = extract_karma_coverage_summary(line)

    if coverage_summary is None:
        raise ValueError('Did not find karma coverage summary line in previous reports')

    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': coverage_summary
    }


def extract_mocha_summary(lines):
    """
    Example mocha summary lines (both lines can be missing if no tests passed/failed):
    ✔ 3 tests completed
    ✖ 1 test failed
    """
    passes, fails = 0, 0
    for line in lines:
        if line and line[0] == '✔':
            passes = int(line.split()[1])
        elif line and line[0] == '✖':
            fails = int(line.split()[1])

    return {
        'total_tests': passes + fails,
        'passed_tests': passes,
        'failed_tests': fails
    }


def mocha_parser(stdout, stderr, previous_reports=None):
    lines = stdout.split('\n')
    mocha_summary_start_regex = r'^SUMMARY:$'

    mocha_summary = None
    summary_lines = [index for index, line in enumerate(lines) if re.search(mocha_summary_start_regex, line)]
    for line_index in summary_lines:
        mocha_summary = extract_mocha_summary(lines[line_index + 1:line_index + 3])

    if mocha_summary is None:
        raise ValueError('Karma summary line not found in input: %s' % stdout)

    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': mocha_summary
    }


def radon_maintainability_parser(stdout, stderr, previous_reports=None):
    """
    Example line: apps/api/urls.py - A
    """
    lines = stdout.split('\n')[:-1]
    summary = {'A': 0, 'B': 0, 'C': 0}
    for line in lines:
        maintainability = line.split(' ')[2]
        assert maintainability in ['A', 'B', 'C']
        summary[maintainability] += 1

    summary['total'] = sum(summary.values())
    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': summary,
    }


def coffeelint_parser(stdout, stderr, previous_reports=None):
    """
    Example summary line:
    ✗ Lint! » 98 errors and 0 warnings in 41 files
    """
    lines = stdout.split('\n')
    summary_line = lines[-3].split(' ')
    total_errors = int(summary_line[3])
    total_warnings = int(summary_line[6])
    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': {
            'total_problems': total_errors + total_warnings,
            'total_errors': total_errors,
            'total_warnings': total_warnings
        }
    }
