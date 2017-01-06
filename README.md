# Quick start

- Add `inspectr.json` to your project root directory. Example:

    ```
    {
      "project_name": "My Project",
      "rethinkdb_host": "localhost",
      "rethinkdb_port": 28015,
    
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
      "rethinkdb_host": "localhost",
      "rethinkdb_port": 28015,
    
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

    **NOTE**
    If you have problems setting up Your RethinkDB instance, simply run it as Docker container: 

    ```
    docker run -d -p 8080:8080 -p 28015:28015 -p 29015:29015 rethinkdb
    ```

2. Install Python virtual environment : 

    ```
    pip install virtualenv
    virtualenv ENV
    source ENV/bin/activate
    ```

3. Install InspectR CLI to your venv 
    ```
    pip install inspectr
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