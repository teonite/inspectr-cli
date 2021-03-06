from copy import deepcopy
import sys
import rethinkdb as r
from colorama import Style, Fore
import os


common_required_settings = ['project_name', 'reporters', 'rethinkdb_host', 'rethinkdb_port']
env_config_matches = (
    ('project_name', 'INSPECTR_PROJECT_NAME'),
    ('rethinkdb_host', 'INSPECTR_RETHINKDB_HOST'),
    ('rethinkdb_port', 'INSPECTR_RETHINKDB_PORT'),
)
default_settings = {
    'rethinkdb_db': 'inspectr'
}

required_reporter_settings = ['type', 'command']


def add_env_to_config(config):
    new_config = config
    for env_config_match in env_config_matches:
        config_field, env_field = env_config_match
        new_config[config_field] = os.getenv(env_field, config[config_field])

    return new_config


def validate_and_parse_config(config_in):
    config = deepcopy(config_in)

    # add env specified variables for config
    config = add_env_to_config(config)

    # check if all required configuration options are present in config file
    if None in [config.get(key) for key in common_required_settings]:
        print('Error: Incomplete configuration (required settings: %s)' % common_required_settings)
        sys.exit(1)

    # check if all required configuration options are present in all reporters
    for reporter in config['reporters']:
        if False in [key in reporter for key in required_reporter_settings]:
            print('Error: Invalid reporter configuration:\n%s\n\nRequired settings: %s' % (reporter, required_reporter_settings))
            sys.exit(1)

    # add default settings if not present in config file
    for key, value in default_settings.items():
        config[key] = config_in.get(key, value)

    return config


def init_db(connection, config):
    """Creates database, tables and indices"""
    try:
        r.db_create(config['rethinkdb_db']).run(connection)
    except r.errors.ReqlOpFailedError:
        # database already exists
        pass

    for table in ['reports', 'reports_history']:
        try:
            r.db(config['rethinkdb_db']).table_create(table).run(connection)
        except r.errors.ReqlOpFailedError:
            # table already exists
            pass

    try:
        r.db(config['rethinkdb_db']).table('reports').index_create('time_created').run(connection)
    except r.errors.ReqlOpFailedError:
        # index already exists
        pass


def save_report(report, config):
    """Saves report to rethinkdb"""
    connection = r.connect(config['rethinkdb_host'], config['rethinkdb_port'])
    init_db(connection, config)

    # Generate uuid from project_name
    uuid = r.uuid(report['project_name']).run(connection)
    report['id'] = uuid

    r.db(config['rethinkdb_db']).table('reports').get(uuid).delete().run(connection)
    # Insert report
    r.db(config['rethinkdb_db']).table('reports').insert(report).run(connection)

    # Report in history should have unique id, but also should have project_id to be able to reference to current report
    report['project_id'] = report['id']
    report['id'] = r.uuid().run(connection)

    # Save report to report_history
    r.db(config['rethinkdb_db']).table('reports_history').insert(report).run(connection)


def colored(message, color=Style.RESET_ALL):
    return "{}{}{}".format(color, message, Style.RESET_ALL)


def print_command(reporter):
    sys.stdout.write(
        '[....] %s (%s)\r' % (reporter['command'] or '', colored(reporter['type'], Fore.BLUE))
    )
    sys.stdout.flush()


def print_command_ok(reporter):
    sys.stdout.write(
        colored('%s[ %sOK %s]%s\n' % (Fore.WHITE, Fore.GREEN, Fore.WHITE, Fore.RESET))
    )
    sys.stdout.flush()


def print_command_fail(reporter):
    sys.stdout.write(
        colored('%s[%sFAIL%s]%s\n' % (Fore.WHITE, Fore.RED, Fore.WHITE, Fore.RESET))
    )
    sys.stdout.flush()
