# Dafuq is this

Inspectr gives you insight into quality of your code at a glance. It supports variety of
code quality tools. Those are the ones supported now, more under way:

* flake8 python linter
* python unittests
* py.test tests
* coverage.py reports
* eslint javascript linter
* jasmine tests
* mocha tests
* karma-coverage reports

# Configuration

Place <b>inspectr.json</b> in your project directory. Example below shows all available reporters - use only the ones that are relevant to your project:

<pre>
{
  "project_name": "My Project",

  "reporters": [
    {
      "type": "flake8",
      "command": "flake8 apps/"
    },
    {
      "type": "unittest",
      "command": "manage.py test"
    },
    {
      "type": "coverage-py",
      "command": "coverage report"
    },
    {
	"type": "pytest",
	"command": "coverage run -m py.test"
    },
    {
      "type": "eslint",
	  "command": "eslint src/"
    },
    {
    	"type": "jasmine",
	    "command": "karma start karma.conf.js --single-run"
    },
    {
    	"type": "mocha",
	    "command": "karma start karma.conf.js --single-run"
    },
    {
	    "type": "karma-coverage",
	    "command": null
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
