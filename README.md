# InspectR CLI

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

1. Place **inspectr.json** in your project directory. Example below shows all available reporters - use only the ones that are relevant to your project:

```
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
```

2. Add .inspectr_connector.json into Your home directory. In it, You need to specify Your [RethinkDB][rethink] instance details

An example inspectr_connector.json file:

```
{
    "rethinkdb_host": "localhost",
    "rethinkdb_port": 28015,
    "rethinkdb_db": "inspectr", //do not change this value
    "reports_table": "reports", //do not change this value
    "reports_history_table": "reports_history" // do not change this value
}
```

If you have problems setting up Your RethinkDB instance, simply run it as Docker container: 

```
docker run -d -p 8080:8080 -p 28015:28015 -p 29015:29015 rethinkdb
```

3. Install Python virtual environment using, e.x. this code : 

```
pip install virtualenv
virtualenv ENV
source ENV/bin/activate
```

4. Install InspectR CLI to your venv 
```
python setup.py
```

#Running
Simply go to your project and InspectR it! (remember that it must contain **inspectr.json**!)

```
cd /path/to/my/project
inspectr
```

Results should be visible in [InspectR Dashboard][dashboard]



[rethink]:https://www.rethinkdb.com/
[dashboard]:https://git.teonite.net/inspectr/inspectr-dashboard