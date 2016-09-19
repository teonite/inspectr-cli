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

1. Place <b>inspectr.json</b> in your project directory. Example below shows all available reporters - use only the ones that are relevant to your project:

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

2. Map .inspectr_connector.json in your backend container configuration at Rancher, f.e. /s/inspectr/.inspectr_connector.json:/root/.inspectr_connector.json

<pre>
{
    "rethinkdb_host": "localhost",
    "rethinkdb_port": 28015,
    "rethinkdb_db": "inspectr",
    "reports_table": "reports",
    "reports_history_table": "reports_history"
}
</pre>

3. Add command that runs inspectr during backend container startup. For example you can add it to tools/run_backend.sh:

<pre>
if [[ -n "$INSPECTR" ]] && [ "$INSPECTR" == "inspect" ]; then
    echo "Env set - running inspectr"
    cd /backend
    inspectr &
else
    echo "Not running inspectr - env not set"
fi
</pre>

4. Add variable INSPECTR = 'inspect' to backend container configuration at Rancher.
