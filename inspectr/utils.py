from copy import deepcopy
import sys
from distutils.spawn import find_executable
import rethinkdb as r

reports_table = 'reports'
reports_history_table = 'reports_history'

common_required_settings = ['project_name', 'reporters', 'rethinkdb_host', 'rethinkdb_port', 'rethinkdb_db']

reporter_required_settings = {
    'flake8': ['lint_paths'],
    'django-test': [],
    'coverage-django-test': [],
    'coverage-py': [],
    'eslint': ['lint_paths'],
    'karma': [],
    'karma-coverage': [],
    'pytest': []
}

default_settings = {
    'django-test': {
        'manage_path': 'manage.py',
        'test_modules': []
    },
    'coverage-django-test': {
        'manage_path': 'manage.py',
        'test_modules': []
    },
    'karma': {
        'karma_config': 'karma.conf.js'
    }
}


def validate_and_parse_config(config_in):
    config = deepcopy(config_in)
    # check if all required configuration options are present in config file
    if None in [config.get(key) for key in common_required_settings]:
        print('Error: Incomplete configuration (required settings: %s)' % common_required_settings)
        sys.exit(1)

    for reporter in config['reporters']:
        if not reporter.get('type'):
            print('Error: Found reporter with undefined type.')
            sys.exit(1)

        required_settings = reporter_required_settings[reporter['type']]
        if None in [reporter.get(key) for key in required_settings]:
            print('Error: Incomplete configuration for reporter %s, required settings: %s' % (reporter['type'], required_settings))
            sys.exit(1)

        # add default config values where needed
        for key, value in default_settings.get(reporter['type'], {}).items():
            reporter[key] = reporter.get(key, value)

        # reporter-specific validation
        if reporter['type'] == 'flake8':
            # check if flake8 is installed
            if find_executable('flake8') is None:
                print('Error: flake8 not installed.')
                sys.exit(1)

        if reporter['type'] == 'coverage-django-test':
            # check if coverage.py is installed
            if find_executable('coverage') is None:
                print('Error: coverage.py not installed.')
                sys.exit(1)

        if reporter['type'] == 'coverage-py':
            # check if coverage.py is installed
            if find_executable('coverage') is None:
                print('Error: coverage.py not installed.')
                sys.exit(1)

        if reporter['type'] == 'eslint':
            # check if eslint installed
            if find_executable('eslint') is None:
                print('Error: eslint not installed.')
                sys.exit(1)

        if reporter['type'] == 'karma' or reporter['type'] == 'karma-coverage':
            # check if karma installed
            if find_executable('eslint') is None:
                print('Error: karma not installed.')
                sys.exit(1)

    return config


def init_db(connection, db):
    """Creates database, tables and indices"""
    try:
        r.db_create(db).run(connection)
    except r.errors.ReqlOpFailedError:
        # database already exists
        pass

    for table in [reports_table, reports_history_table]:
        try:
            r.db(db).table_create(table).run(connection)
        except r.errors.ReqlOpFailedError:
            # table already exists
            pass

    try:
        r.db(db).table(reports_table).index_create('time_created').run(connection)
    except r.errors.ReqlOpFailedError:
        # index already exists
        pass


def save_report(report, host='localhost', port=28015, db='inspectr'):
    """Saves report to rethinkdb"""
    connection = r.connect(host, port)
    init_db(connection, db)

    # delete old reports from reports table and insert new report
    r.db(db).table(reports_table).filter({'project_name': report['project_name']}).delete().run(connection)
    r.db(db).table(reports_table).insert(report).run(connection)

    # insert report to reports_history table
    r.db(db).table(reports_history_table).insert(report).run(connection)
