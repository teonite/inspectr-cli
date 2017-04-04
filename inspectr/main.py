from json import loads
import sys

from inspectr.utils import print_command, print_command_fail, print_command_ok
from .executor import execute
from .parsers import (flake8_parser, coverage_py_parser, eslint_parser, jasmine_parser, karma_coverage_parser,
                      pytest_parser, unittest_parser, mocha_parser, radon_maintainability_parser, coffeelint_parser,
                      radon_cyclomatic_complexity_parser, tslint_parser)
from .utils import save_report, validate_and_parse_config, colored
import time
from datetime import datetime
from colorama import init, Fore

from pytz import timezone


parsers = {
    'flake8': flake8_parser,
    'unittest': unittest_parser,
    'coverage-py': coverage_py_parser,
    'eslint': eslint_parser,
    'coffeelint': coffeelint_parser,
    'jasmine': jasmine_parser,
    'mocha': mocha_parser,
    'karma-coverage': karma_coverage_parser,
    'pytest': pytest_parser,
    'radon-maintainability': radon_maintainability_parser,
    'radon-cyclomatic-complexity': radon_cyclomatic_complexity_parser,
    'tslint': tslint_parser,
}


def get_datetime():
    tz = timezone(time.tzname[0])
    return datetime.now(tz=tz)


def run():
    init()
    # TODO: config locations as command line param?
    config_path = 'inspectr.json'
    try:
        with open(config_path, 'r') as config_file:
            # load config file
            config_dict = loads(config_file.read())
    except:
        print(colored('Error: parsing configuration file %s failed' % config_path, Fore.RED))
        sys.exit(1)

    config = validate_and_parse_config(config_dict)

    # generate report for each reporter in config['reporters'] list
    reports = []
    for reporter in config['reporters']:
        print_command(reporter)
        try:
            stdout, stderr = execute(reporter['command'])
            parsed_report = parsers[reporter['type']](stdout, stderr, reports)
        except:
            print_command_fail(reporter)
            print(colored('Error: Reporter %s failed. \nSTDOUT:\n%s\nSTDERR:\n%s\n' % (reporter['type'], stdout, stderr), Fore.RED))
            parsed_report = {
                'stdout': stdout,
                'stderr': stderr,
                'summary': None
            }
        else:
            print_command_ok(reporter)

        parsed_report['type'] = reporter['type']
        reports.append(parsed_report)

    project_report = {
        'project_name': config['project_name'],
        'time_created': get_datetime(),
        'reports': reports
    }
    save_report(project_report, config)
