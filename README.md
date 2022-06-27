<div align="center">
    <h1>pepsin</h1>
    <div style="gap:10px;display: flex; justify-content: center" align="center">
        <img src="https://github.com/khan-asfi-reza/pepsin/actions/workflows/development.yaml/badge.svg" alt="">
        <img src="https://github.com/khan-asfi-reza/pepsin/actions/workflows/publish.yaml/badge.svg" alt="">
        <img src="https://codecov.io/gh/khan-asfi-reza/pepsin/branch/master/graph/badge.svg?token=BS5ZJN8ZRI" alt="">
        <img src="https://img.shields.io/badge/linting-pylint-green" alt="">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="">
</div>
</div>


### In Development

Currently the goal is to create a simple tool to manage dependencies,
Initialize projects (django, fastapi, flask) with production ready features.
Initialize pytest, tox, github actions etc. which takes a lot of time to configure. Managing scripts to run,
(Inspired by `npm run`)


### Features

- Auto virtualenv generation
- Auto venv activation, no need to activate `venv` before running `scripts`
- Auto manage dependencies in `pepsin.yaml`
- Install and store libraries
- Run scripts stored in the configuration file


### Requirements
`python 3.6+`

## Installation

```shell
$ pip3 install pepsin
```
## Before use

pepsin generates or uses `pepsin.yaml` file to store
all your metadata, project configuration, project libraries and dependencies
`pepsin.yaml` config file
```yaml
name: GameOfChairs # Name of the project
author: Khan Asfi Reza # Author's name
email: info@khanasfireza.com # Author's email
venv: venv # Virtualenv directory name
license: MIT # Project license type
libraries:
  # Installed libraries
  - django
  - psycopg2
  - djangorestframework
  - django-channels
```

If any failure or error occurs a `failed.pepsin.log` will be created mentioning the problem

## Usage

### 1. `init`
```shell
$ pepsin init
```
Init command generates basic python project to get start with,
It will interactively ask you to fill the required fields
```shell
$ pepsin init
$ pepsin Generate Project
$ ----------------------
$ Project Name[project]:
$ Author[]:
$ Email[]:
$ License[]:
```
File structure

```
Project  Directory
|____ venv
|____ pepsin.yaml
|____ Readme.md
|____ .gitignore
|____ project
      |___ main.py
      |___ __init__.py
```

#### Optional Arguments:
`name` the name of the project and pepsin will create a project with the given project name

Example:
```shell
$ pepsin init project_name
```

#### Options

|option|description|type|required|default|
|---|---|---|---|---|
|--venv|Virtual environment directory|string|false|venv|
|--h|Help text|boolean|false|
|--no-input|Ignores input prompt|boolean(flag)|false|venv|

### 2. `install`

Command Alias: `add` `i`

Install required dependencies and libraries

```shell
$ pepsin install django
```
or
```shell
$ pepsin i django
```
or
```shell
$ pepsin add django
```
Also `text` file with list of libraries can be installed with `-r` flag
```shell
$ pepsin install -r requirements.txt
```
Note: install command will by default create a `pepsin.yaml` file and a virtualenv directory named `venv`

|option|description|type|required|default|
|---|---|---|---|---|
|-r|Install from the given requirements file|string|false|null|
|--h|Help text|boolean|false|


### 3. `uninstall`

Uninstall a library that is installed in your environment

```shell
$ pepsin uninstall <library>
```

Example:

```shell
$ pepsin uninstall flask
```

Uninstall command will remove the library from the virtual environment as well as the config

### 4. `update`

Alias: `upgrade`

Upgrades a library that is installed in your environment

```shell
$ pepsin upgrade <library>
```

Example:

```shell
$ pepsin upgrade flask
```


### 5. `run`

Runs a script from the `pepsin.yaml`

To store and run scripts you must write your scripts in the pepsin configuration

Example:

`pepsin.yaml`
```yaml
name: example # Name of the project
author: Khan Asfi Reza # Author's name
email: info@khanasfireza.com # Author's email
venv: venv # Virtualenv directory name
license: MIT # Project license type
libraries:
  # Installed libraries
  - django
  - psycopg2
scripts:
  start: example/manage.py startserver
  test: pytest examples/tests
```

To run the `start` script use pepsin run command
```shell
$ pepsin run start
```
which will fire the `start` script

### 6. `pip`

Run regular pip command

```shell
$ pepsin pip freeze
```

Pip will automatically use available virtual env (if available) otherwise
it will use global pip
