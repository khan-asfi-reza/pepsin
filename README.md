<div align="center">
    <h1>Pipcx</h1>
    <div style="gap:10px;display: flex; justify-content: center" align="center">
        <img src="https://github.com/khan-asfi-reza/pipcx/actions/workflows/development.yaml/badge.svg" alt="">
        <img src="https://codecov.io/gh/khan-asfi-reza/pipcx/branch/master/graph/badge.svg?token=BS5ZJN8ZRI" alt="">
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

Pipcx's code structure is heavily inspired by `django.core.management`
pipcx implements almost the similar strategy of code writing and work process.
Pipcx cli library is written using builtin libraries like `argparse` `importlib` `pkgutil` `sys` `os` etc.
For storing libraries and managing dependencies, `yaml` file has been selected 
as it has a very basic and minimalistic syntax. 


### Requirements
`python 3.6+`

## Installation

```shell
$ pip3 install pipcx
```

## Usage

### 1. `init` - Initializes a python project and virtualenv

```shell
$ pipcx init
```

This will create a virtualenv and activate it along with project config yaml file in the project directory
```
Project  Directory
|____ venv
|____ pipcx.yaml
|____ project
      |___ main.py
      |___ __init__.py
```

#### Options:
`name` Project Name

`--venv`  Virtualenv Directory name

```shell
$ pipcx project_name --venv=my_venv 
```
The above command will create a virtualenv under the name `my_venv`
and create project with `project_name`

---