from json import loads
import sys

from .reporters import django_unittest_reporter, django_unittest_coverage_reporter, flake8_reporter, eslint_reporter, karma_reporter, karma_coverage_reporter
from .utils import save_report, validate_and_parse_config
import time
from datetime import datetime

from pytz import timezone

reporters = {
    'flake8': flake8_reporter,
    'django-unittest': django_unittest_reporter,
    'django-unittest-coverage': django_unittest_coverage_reporter,
    'eslint': eslint_reporter,
    'karma': karma_reporter,
    'karma-coverage': karma_coverage_reporter
}


def get_datetime():
    tz = timezone(time.tzname[0])
    return datetime.now(tz=tz)


def run():
    # FIXME: config location as command line param
    config_path = 'inspectr.json'
    with open(config_path, 'r') as config_file:
        try:
            # load config file
            config_dict = loads(config_file.read())
        except:
            print('Error: parsing configuration file %s failed' % config_path)
            sys.exit(1)

    config = validate_and_parse_config(config_dict)

    # generate report for each reporter in config['reporters'] list
    reports = []
    for reporter in config['reporters']:
        print('Executing %s reporter' % reporter['type'])
        try:
            report = reporters[reporter['type']](reporter, reports)
        except:
            print('Warning: Reporter for type %s failed.' % reporter['type'])
            continue
        report['type'] = reporter['type']
        reports.append(report)

    project_report = {
        'project_name': config['project_name'],
        'time_created': get_datetime(),
        'reports': reports
    }
    save_report(project_report, config['rethinkdb_host'], config['rethinkdb_port'], config['rethinkdb_db'])
