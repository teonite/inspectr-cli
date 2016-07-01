# -*- coding: utf-8 -*-
import re


def parse_flake8_output(stdout, stderr):
    """Returns summary and list of errors from flake8 stdout"""
    lines = stdout.split('\n')
    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': {
            'total_errors': max(0, len(lines) - 2)
        }
    }


def parse_unittest_output(stdout, stderr):
    """Returns summary and detailed testing results from unittest stdout"""
    lines = stderr.split('\n')  # unittest pushes output to stderr
    try:
        total_line, status_line = lines[-4:-1:2]

        # example total_line: u'Ran 2 tests in 0.396s'
        total_tests = int(total_line.split()[1])

        # example fail status line: u'FAILED (failures=17)'
        failed_tests = 0 if status_line.startswith('OK') else int(status_line.split('=')[1][:-1])
    except:
        print('Warning: Parsing unittest output failed: %s' % '\n'.join([stdout, stderr]))
        return {
            'stdout': stdout,
            'stderr': stderr,
            'summary': None
        }

    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': {
            'total_tests': total_tests,
            'failed_tests': failed_tests
        }
    }


def parse_coverage_output(stdout, stderr):
    """Returns summary and detailed test coverage results from coverage stdout"""
    lines = stdout.split('\n')
    try:
        summary_line = ' '.join(lines[-2].split())  # remove duplicate spaces
        total_statements, total_missing, coverage_percent = summary_line.split()[1:]
    except:
        print('Warning: Parsing coverage.py output failed: %s' % '\n'.join([stdout, stderr]))
        return {
            'stdout': stdout,
            'stderr': stderr,
            'summary': None
        }

    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': {
            'total_statements': int(total_statements),
            'total_missing': int(total_missing),
            'coverage_percent': int(coverage_percent[:-1])
        }
    }


def parse_pytest_output(stdout, stderr):
    """Retruns summary and detailed test report from pytest stdout"""
    lines = stdout.split('\n')
    try:
        summary_line = lines[-2].split()
        # example fail summary_line: =========== 4 failed, 38 passed in 0.10 seconds =============
        # example success summary_line: ========= 21 passed in 0.05 seconds =========
        if summary_line[2].lower() == 'passed':
            passed_tests = int(summary_line[1])
            failed_tests = 0
        else:
            passed_tests = int(summary_line[3])
            failed_tests = int(summary_line[1])
    except:
        print('Warning: Parsing py.test output failed: %s' % '\n'.join([stdout, stderr]))
        return {
            'stdout': stdout,
            'stderr': stderr,
            'summary': None
        }

    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': {
            'passed_tests': passed_tests,
            'failed_tests': failed_tests
        }
    }


def parse_eslint_output(stdout, stderr):
    """Returns summary and list of errors from eslint stdout"""
    lines = stdout.split('\n')
    if len(lines) == 1:
        # no output, no errors
        return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': {
            'total_problems': 0,
            'total_errors': 0,
            'total_warnings': 0
        }
    }
    try:
        summary_line = lines[-3].split()

        # example summary line: u'✖ 1767 problems (120 errors, 1647 warnings)'
        total_problems, total_errors, total_warnings = int(summary_line[1]), int(summary_line[3][1:]), int(summary_line[5])
    except:
        print('Warning: Parsing ESLint output failed: %s' % '\n'.join([stdout, stderr]))
        return {
            'stdout': stdout,
            'stderr': stderr,
            'summary': None
        }

    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': {
            'total_problems': total_problems,
            'total_errors': total_errors,
            'total_warnings': total_warnings
        }
    }


def extract_karma_summary(line):
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


def parse_karma_output(stdout, stderr):
    """Returns summary and list of errors from karma stdout"""
    lines = stdout.split('\n')
    try:
        karma_summary_regex = r'\(.+\): Executed \d+ of \d+ (SUCCESS|\(\d+ FAILED\)( ERROR)?) \(.+ secs / .+ secs\)'

        karma_summary = None
        summary_lines = [line for line in lines if re.search(karma_summary_regex, line)]
        for line in summary_lines:
            karma_summary = extract_karma_summary(line)
    except:
        print('Warning: Parsing karma output failed: %s' % '\n'.join([stdout, stderr]))
        return {
            'stdout': stdout,
            'stderr': stderr,
            'summary': None
        }

    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': karma_summary
    }


def parse_karma_coverage_output(stdout, stderr):
    """Returns test coverage summary and list of errors from karma stdout"""
    lines = stdout.split('\n')
    try:
        coverage_summary_regex = r'All files\s*\|\s*\d+\.\d+\s*\|\s*\d+\.\d+\s*\|\s*\d+\.\d+\s*\|\s*\d+\.\d+\s*\|\s*\|'

        coverage_summary = None
        summary_lines = [line for line in lines if re.search(coverage_summary_regex, line)]
        for line in summary_lines:
            coverage_summary = extract_karma_coverage_summary(line)
    except:
        print('Warning: Parsing karma-coverage output failed: %s' % '\n'.join([stdout, stderr]))
        return {
            'stdout': stdout,
            'stderr': stderr,
            'summary': None
        }

    return {
        'stdout': stdout,
        'stderr': stderr,
        'summary': coverage_summary
    }
