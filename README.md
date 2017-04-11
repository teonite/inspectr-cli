 ![eagle-R]


# What is InspectR?

InspectR gives you insight into quality of your code at a glance. It supports variety of code quality tools. 
When you add `inspectr.json` file to your project directory and use command `inspectr` reports from your test tools will be created and save in RethinkDB. 

The reports will be able in [inspectr-dashboard][dashboard] and it looks like this

![example]

Those are the ones supported now, more under way:

* flake8 python linter
* python unittests
* py.test tests
* coverage.py reports
* eslint javascript linter
* jasmine tests
* mocha tests
* karma-coverage reports


# Quick start (for developers)

1. Install Inspectr globally from pip `pip3 install inspectr`.
2. Run inspectr-dashboard with RethinkDB (go [here][dashboard]).
3. Add inspectr.json to your project root directory. Example:
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
4. Use command `inspectr` in this directory.
5. If everything went ok you should see results in browser.


# Using inspectr with docker

1. Run RethinkDB, we recommend to use docker-compose in [inspectr-dashboard][dashboard] which is creating RethinkDB container.
2. Add `inspectr.json` to your project root directory (example above).
3. Change `rethinkdb_host` and `rethinkdb_port` if you have to.
4. Clone this repo using `git clone git@git.teonite.net:inspectr/inspectr.git.`
5. Build docker image for example: `docker build -t inspectr_cli .` in inspectr directory
6. Run your docker image (for example: `docker run -t -v $PWD/project:/code inspectr_cli`). 
Give your `inspectr.json` path instead of `$PWD/project`. If everything went ok report will be sent to rethinkDB and will be available in inspectr-dashboard.
7. If you're using RethinkDB docker container local, and you'll see error `ConnectionRefusedError: [Errno 111] Connection refused` you have to link RethinkDB container to alias which will be use in `inspectr.json` as rethinkdb_host parameter.
Example: `docker run -t --link inspectrdashboard_rethinkdb_1:db_link -v $PWD:/code inspectr_cli` where `inspectrdashboard_rethinkdb_1` is name of your RethinkDB container and `db_link` is parameter of `rethinkdb_host` in `inspectr.json`.
8. Your reports should be saved in RethinkDB. Use [inspectr-dashboard][dashboard] to see results in browser.

For more informations check FAQ at the end of README.


# Using inspectr locally

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

### Running

Simply go to your project and InspectR it! (remember that it must contain `inspectr.json`!)

```
cd /path/to/my/project
inspectr
```

Results should be visible in [InspectR Dashboard][dashboard]


# List of reporters

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




# FAQ
 
1. If you have problems setting up Your RethinkDB instance, simply run
 it as Docker container:
`docker run -d -p 8080:8080 -p 28015:28015 -p 29015:29015 rethinkdb`

2. You have to run inspectr at your app first to create Collections in RethinkDB, otherwise you'll see error "Collection *reports* does not exist" 

3. If one of your reporters will fail check if it is installed.
For example if you have error
	```
	[FAIL] eslint src/ (eslint) FileNotFoundError: [Errno 2] No such file or directory: 'eslint'
	```
	Install eslint `npm install -g eslint`

4. If you're inspecting django app local, install django in your virtualenv.
5. If you're using Inspectr in docker and you want to connect with RethinkDB on localhost run `docker run -t --net="host" -v $PWD/project:/code inspectr_cli`

[rethink]:(https://www.rethinkdb.com/)
[dashboard]:(https://git.teonite.net/inspectr/inspectr-dashboard)
[eagle-L]: md_imgs/eagle-L.png "Eagle"
[eagle-R]: md_imgs/eagle-R.png "Eagle"
[star]: md_imgs/star.png "Star"
[example]: md_imgs/example.png "Example"
