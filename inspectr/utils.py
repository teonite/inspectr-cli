from collections import defaultdict
from copy import deepcopy
import sys
import rethinkdb as r

reports_table = 'reports'
reports_history_table = 'reports_history'

common_required_settings = ['project_name', 'reporters', 'rethinkdb_host', 'rethinkdb_port', 'rethinkdb_db']

reporter_required_settings = defaultdict(list)
reporter_required_settings.update({
    'flake8': ['lint_paths'],
    'eslint': ['lint_paths'],
})

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
    },
    'pytest': {
        'test_paths': []
    },
    'coverage-pytest': {
        'test_paths': []
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
