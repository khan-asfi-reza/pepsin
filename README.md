<div align="center">
    <h1>pepsin</h1>
    <div style="gap:10px;display: flex; justify-content: center" align="center">
        <img src="https://github.com/khan-asfi-reza/pepsin/actions/workflows/development.yaml/badge.svg" alt="">
        <img src="https://codecov.io/gh/khan-asfi-reza/pepsin/branch/master/graph/badge.svg?token=BS5ZJN8ZRI" alt="">
        <img src="https://img.shields.io/badge/code%20style-pep8-orange.svg" alt="">
        <img src="https://img.shields.io/badge/linting-pylint-green" alt="">
</div>
</div>

#### Python Project Initializer CLI Tool, uses pip
To install packages

`Discarded previous version for not maintaining and complexity of code`

### In Development

Currently the goal is to create a simple tool to manage dependencies,
Initialize projects (django, fastapi, flask) with production ready features.
Initialize pytest, tox, github actions etc. Managing scripts to run,
(Inspired by `npm run`)

So primary goal is to -

1. Create a toolchain to manage dependencies
2. Project initialization
3. Managing scripts
4. File generation based on templates (tox, pytest)
5. Dockerizing and customization hook

pepsin's code structure is heavily inspired by `django.core.management`
pepsin implements almost the similar strategy of code writing and work process.
pepsin cli library is written using builtin libraries like `argparse` `importlib` `pkgutil` `sys` `os` etc.
For storing libraries and managing dependencies, `yaml` file has been selected
as it has a very basic and minimalistic syntax.


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

Uninstall a library that is installed in your envrionment

```shell
$ pepsin uninstall
```
