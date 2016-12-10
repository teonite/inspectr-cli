# Quick start

- Add `inspectr.json` to your project root directory. Example:

    ```
    {
      "project_name": "My Project",
    
      "reporters": [
        {
          "type": "jasmine",
          "command": "karma start karma.conf.js --single-run"
        },
        {
          "type": "mocha",
          "command": "karma start karma.conf.js --single-run"
        }
      ]
    }
    ```

- Add Dashboard connector file - `.inspectr_connector.json` in your home directory. Example:

    ```
    {
        "rethinkdb_host": "localhost",
        "rethinkdb_port": 28015,
        "rethinkdb_db": "inspectr", //do not change this value
        "reports_table": "reports", //do not change this value
        "reports_history_table": "reports_history" // do not change this value
    }
    ```

- Install inspectr to Your Venv

    `pip install inspectr`
    
- Test your project! Run `inspectr` command in your project root directory

# InspectR CLI Overview

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

1. Place `inspectr.json` in your project directory. Example below shows all available reporters - use only the ones that are relevant to your project:

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

2. Add `.inspectr_connector.json` into Your home directory. In it, You need to specify Your [RethinkDB][rethink] instance details

    An example `.inspectr_connector.json` file:

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

# Running

Simply go to your project and InspectR it! (remember that it must contain `inspectr.json`!)

```
cd /path/to/my/project
inspectr
```

Results should be visible in [InspectR Dashboard][dashboard]

# Dockerizing InspectR CLI

1. Add Your `inspectr.json` to project

2. Add necessary config files specific to your reporters in Dockerfile for backend container:
    ```
    ADD inspectr.json /backend/inspectr.json
    ADD .coveragerc /backend/.coveragerc
    ADD .flake8 /backend/.flake8
    ```

3. Map `.inspectr_connector.json` in your backend container configuration in `docker-compose.yml` file, for example:
    ```
    backend:
      image: ${BACKEND_IMAGE}
      volumes:
       - /s/inspectr/.inspectr_connector.json:/root/.inspectr_connector.json
    ```

4. Add command that runs inspectr during backend container startup. For example you can add it to tools/run_backend.sh:
    ```
    if [[ -n "$INSPECTR" ]] && [ "$INSPECTR" == "inspect" ]; then
        echo "Env set - running inspectr"
        cd /backend
        inspectr &
    else
        echo "Not running inspectr - env not set"
    fi
    ```
5. Add environment variable `INSPECTR = 'inspect'` to backend container configuration in `docker-compose.yml` file.

6. Add necessary requirements to backend container:
    ```
    inspectr==0.1.0
    flake8==2.5.4
    radon==1.4.0
    coverage==4.1
    pytest==2.9.2
    pytest-django==2.9.1
    ```


[rethink]:https://www.rethinkdb.com/
[dashboard]:https://git.teonite.net/inspectr/inspectr-dashboard