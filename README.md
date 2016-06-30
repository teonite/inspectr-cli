# Dafuq is this

Inspectr gives you insight into quality of your code at a glance. It supports variety of
code quality tools. Those are the ones supported now, more under way:

* flake8 python linter
* django unittests
* py.test tests
* coverage.py reports
* eslint javascript linter
* karma tests
* karma-coverage reports

# Configuration

Place <b>inspectr.json</b> in your project directory. Example below shows all available reporters
use only the ones that are relevant to your project:

<pre>
{
  "project_name": "My Project",

  "reporters": [
    {
      "type": "flake8",
      "lint_paths": ["apps/"]
    },
    {
      "type": "django-test",
      "manage_path": "manage.py",
      "test_modules": ["apps.core"]
    },
    {
      "type": "coverage-django-test",
      "manage_path": "manage.py",
      "test_modules": ["myapp"]
    },
    {
      "type": "coverage-py"
    },
    {
      "type": "coverage-pytest",
      "test_paths": ["apps/"]
    },
    {
      "type": "pytest",
      "test_paths": ["apps/"]
    },
    {
      "type": "eslint",
      "lint_paths": [
        "src/"
      ]
    },
    {
      "type": "karma"
    },
    {
      "type": "karma-coverage"
    }
  ]
}
</pre>

Place <b>.inspectr_connector.json</b> in your home directory. This file describes where to store
inspection results to be displayed by inspectr-dashboard. Example:

<pre>
{
    "rethinkdb_host": "localhost",
    "rethinkdb_port": 28015,
    "rethinkdb_db": "inspectr",
    "reports_table": "reports",
    "reports_history_table": "reports_history"
}
</pre>

# Development - Adding reporters

1. Add reporter_required_settings and default_settings for your reporter in utils.py
2. Implement validation logic for your reporter in utils.parse_and_validate_config
3. Implement reporter in reporters.py - should invoke command, gather output and parse it with appropriate parser
4. Implement parser for command invoked by your reporter. Parser should return dictionary with keys:
output: should contain command output split into lines (['output line 1', 'output line 2', ...])
summary: contains relevant summary statistics from your reporter ({tests_executed: 10, tests_failed: 3})
5. Don't forget to test reporter, parser and validation (test_reporters, test_parsers, test_utils)

6. Add react component for your reporter
7. Add ranking function for your reporter (ranking.js). Ranking function should return value in range <0, 1> - the higher the better.
