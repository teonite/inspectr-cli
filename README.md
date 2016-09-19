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

2. Add necessary config files specific to your reporters. This is an example for Dockerfile for backend container:

<pre>
ADD inspectr.json /backend/inspectr.json
ADD .coveragerc /backend/.coveragerc
ADD .flake8 /backend/.flake8
</pre>

3. Map .inspectr_connector.json in your backend container configuration at Rancher, for example:

<pre>
backend:
  image: ${BACKEND_IMAGE}
  volumes:
   - /s/inspectr/.inspectr_connector.json:/root/.inspectr_connector.json
</pre>

An example inspectr_connector.json file:

<pre>
{
    "rethinkdb_host": "localhost",
    "rethinkdb_port": 28015,
    "rethinkdb_db": "inspectr",
    "reports_table": "reports",
    "reports_history_table": "reports_history"
}
</pre>

4. Add command that runs inspectr during backend container startup. For example you can add it to tools/run_backend.sh:

<pre>
if [[ -n "$INSPECTR" ]] && [ "$INSPECTR" == "inspect" ]; then
    echo "Env set - running inspectr"
    cd /backend
    inspectr &
else
    echo "Not running inspectr - env not set"
fi
</pre>

5. Add variable INSPECTR = 'inspect' to backend container configuration at Rancher.

6. Add necessary requirements to backend container:

<pre>
inspectr==0.1.0
flake8==2.5.4
radon==1.4.0
coverage==4.1
pytest==2.9.2
pytest-django==2.9.1
</pre>