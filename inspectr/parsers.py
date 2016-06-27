# -*- coding: utf-8 -*-
import re


def parse_flake8_output(output):
    """Returns summary and list of errors from flake8 stdout"""
    lines = output.split('\n')
    return {
        'output': lines,
        'summary': {
            'total_errors': len(lines) - 2
        }
    }


def parse_unittest_output(output):
    """Returns summary and detailed testing results from unittest stdout"""
    lines = output.split('\n')
    total_line, status_line = lines[-4:-1:2]

    # example total_line: u'Ran 2 tests in 0.396s'
    total_tests = int(total_line.split()[1])

    # example fail status line: u'FAILED (failures=17)'
    failed_tests = 0 if status_line.startswith('OK') else int(status_line.split('=')[1][:-1])

    return {
        'output': lines,
        'summary': {
            'total_tests': total_tests,
            'failed_tests': failed_tests
        }
    }


def parse_coverage_output(output):
    """Returns summary and detailed test coverage results from coverage stdout"""
    lines = output.split('\n')
    summary_line = ' '.join(lines[-2].split())  # remove duplicate spaces
    total_statements, total_missing, coverage_percent = summary_line.split()[1:]

    return {
        'output': lines,
        'summary': {
            'total_statements': int(total_statements),
            'total_missing': int(total_missing),
            'coverage_percent': int(coverage_percent[:-1])
        }
    }


def parse_eslint_output(output):
    """Returns summary and list of errors from eslint stdout"""
    lines = output.split('\n')
    summary_line = lines[-3].split()

    # example summary line: u'✖ 1767 problems (120 errors, 1647 warnings)'
    total_problems, total_errors, total_warnings = int(summary_line[1]), int(summary_line[3][1:]), int(summary_line[5])

    return {
        'output': lines,
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


def parse_karma_output(output):
    """Returns summary and list of errors from karma stdout"""
    lines = output.split('\n')

    karma_summary_regex = r'\(.+\): Executed \d+ of \d+ (SUCCESS|\(\d+ FAILED\)( ERROR)?) \(.+ secs / .+ secs\)'

    karma_summary = {}
    summary_lines = [line for line in lines if re.search(karma_summary_regex, line)]
    for line in summary_lines:
        karma_summary = extract_karma_summary(line)

    return {
        'output': lines,
        'summary': karma_summary
    }


def parse_karma_coverage_output(output):
    """Returns test coverage summary and list of errors from karma stdout"""
    lines = output.split('\n')

    coverage_summary_regex = r'All files\s*\|\s*\d+\.\d+\s*\|\s*\d+\.\d+\s*\|\s*\d+\.\d+\s*\|\s*\d+\.\d+\s*\|\s*\|'

    coverage_summary = {}
    summary_lines = [line for line in lines if re.search(coverage_summary_regex, line)]
    for line in summary_lines:
        coverage_summary = extract_karma_coverage_summary(line)

    return {
        'output': lines,
        'summary': coverage_summary
    }
