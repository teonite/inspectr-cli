from copy import deepcopy
import sys
import rethinkdb as r
from colorama import Style


common_required_settings = ['project_name', 'reporters']
required_connector_settings = ['rethinkdb_host', 'rethinkdb_port', 'rethinkdb_db', 'reports_table', 'reports_history_table']

required_reporter_settings = ['type', 'command']


def validate_and_parse_config(config_in):
    config = deepcopy(config_in)
    # check if all required configuration options are present in config file
    if None in [config.get(key) for key in common_required_settings]:
        print('Error: Incomplete configuration (required settings: %s)' % common_required_settings)
        sys.exit(1)

    for reporter in config['reporters']:
        if False in [key in reporter for key in required_reporter_settings]:
            print('Error: Invalid reporter configuration:\n%s\n\nRequired settings: %s' % (reporter, required_reporter_settings))
            sys.exit(1)

    return config


def validate_connector_config(config_in):
    config = deepcopy(config_in)
    # check if all required configuration options are present in config file
    if None in [config.get(key) for key in required_connector_settings]:
        print('Error: Incomplete connector configuration (required settings: %s)' % required_connector_settings)
        sys.exit(1)

    return config


def init_db(connection, config):
    """Creates database, tables and indices"""
    try:
        r.db_create(config['rethinkdb_db']).run(connection)
    except r.errors.ReqlOpFailedError:
        # database already exists
        pass

    for table in [config['reports_table'], config['reports_history_table']]:
        try:
            r.db(config['rethinkdb_db']).table_create(table).run(connection)
        except r.errors.ReqlOpFailedError:
            # table already exists
            pass

    try:
        r.db(config['rethinkdb_db']).table(config['reports_table']).index_create('time_created').run(connection)
    except r.errors.ReqlOpFailedError:
        # index already exists
        pass


def save_report(report, config):
    """Saves report to rethinkdb"""
    connection = r.connect(config['rethinkdb_host'], config['rethinkdb_port'])
    init_db(connection, config)

    # delete old reports from reports table and insert new report
    r.db(config['rethinkdb_db']).table(config['reports_table']).filter({'project_name': report['project_name']}).delete().run(connection)
    r.db(config['rethinkdb_db']).table(config['reports_table']).insert(report).run(connection)

    # insert report to reports_history table
    r.db(config['rethinkdb_db']).table(config['reports_history_table']).insert(report).run(connection)


def cprint(message, color=Style.RESET_ALL):
    print("{}{}{}".format(color, message, Style.RESET_ALL))
