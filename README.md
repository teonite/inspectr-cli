# InspectR CLI Overview

Inspectr gives you insight into quality of your code at a glance. It supports variety of code quality tools. 
When you add `inspectr.json` file to your project directory and use command `inspectr` reports will be created and save in RethinkDB (so to use this command you need running RethinkDB). 
The reports will be able in [inspectr-dashboard](https://git.teonite.net/inspectr/inspectr-dashboard). 

Those are the ones supported now, more under way:

* flake8 python linter
* python unittests
* py.test tests
* coverage.py reports
* eslint javascript linter
* jasmine tests
* mocha tests
* karma-coverage reports

List of reporters:
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

# Quick start docker (recommended)

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
- Build docker image for example: `docker build -t inspectr_cli .` in `inspectr-cli` directory
- Run your docker image (for example: `docker run -v $PWD/project:/code inspectr_cli`). Give your `inspectr.json` path instead of `$PWD/project`. If everything went ok report will be sent to rethinkDB and will be available in inspectr-dashboard. 

# Quick start local docker (recommended)

If you are using local RethinkDB docker container you have to add your docker RethinkDB IP Address as `rethink_db_host` parameter in `inspectr.json` type `docker inspect --format='{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' REHINKDB_NAME_CONTAINER` put your RethinkDB container name in `REHINKDB_NAME_CONTAINER`, if you're using RethinkDB from `inspectr-dashboard` docker-compose it'll be `inspectrdashboard_rethinkdb_1`.
    
# Quick start local

1. Run RethinkDB
2. Install Python virtual environment using, e.x. this code :
```
pip3 install virtualenv
virtualenv env
source env/bin/activate
```
3. Install InspectR CLI to your venv
`python setup.py install`
4. Place inspectr.json in your project directory (example above) and use command `inspectr`.
5. If you're inspecting JS app install (global) dependencies from docker/package.json.
6. If you're inspecting python app install pip requirements from `requirements.pip` and `docker/reporter-requirements.pip`


# Running

Simply go to your project and InspectR it! (remember that it must contain `inspectr.json`!)

```
cd /path/to/my/project
inspectr
```

Results should be visible in [InspectR Dashboard][dashboard]

# FAQ
 
1. If you have problems setting up Your RethinkDB instance, simply run
 it as Docker container:
`docker run -d -p 8080:8080 -p 28015:28015 -p 29015:29015 rethinkdb`

2. You have to run inspectr at your app first to create Collections in RethinkDB, otherwise you'll see error "Collection *reports* does not exist" 

3. If one of your reporters will fail check if it is installed.
For example if you have error
	```
	[FAIL] eslint jsapp/src/ (eslint) FileNotFoundError: [Errno 2] No such file or directory: 'eslint'
	```
	Install eslint `npm install -g eslint`

4. If you're inspecting django app local, install django in your virtualenv.

[rethink]:(https://www.rethinkdb.com/)
[dashboard]:(https://git.teonite.net/inspectr/inspectr-dashboard)
