# pipcx

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

The way of writing code is heavily inspired by `django.core.management`
This project implements almost the similar strategy in terms of process and code writing.
The main target is not to use any external tools to create a cli program

[![GitHub Actions (Tests)](https://github.com/khan-asfi-reza/pipcx/workflows/Build/badge.svg)](https://github.com/khan-asfi-reza/pipcx)
[![codecov](https://codecov.io/gh/khan-asfi-reza/pipcx/branch/master/graph/badge.svg?token=BS5ZJN8ZRI)](https://codecov.io/gh/khan-asfi-reza/pipcx)


### Requirements
`python 3.6>`

## Installation
### 1. Create a virtual environment and activate

`windows`
```cmd
 pip install virtualenv
 python3 -m virtualenv venv
 <YOUR WORKING DIRECTORY>/venv/scripts/activate
```
>Your Current Working Directory

`MacOS`
```commandline
pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```

`Ubuntu [Debian]`
```commandline
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
virtualenv venv 
source venv/bin/activate
```
>you can use any name instead of **venv**
### 2. Install pipcx
```cmd
pip3 install pipcx
```

## Usages

### 1. `init`

Starts A Python Project

```commandline
pipcx init
```

```commandline
Project Name[Project]: YOUR_PROJECT_NAME
Project Author[ubuntu]: PETER_PARKER
Project Description[]: A Web Slinger Project
```

`No Input Option`: `--no-input`, `--ninp`

This will automatically generate project without taking input
```commandline
pipcx init My_PROJECT --no-input
```

`Changing Source Directory Option`: `--src`, `source`

Change Source Directory Option
```commandline
pipcx init My_PROJECT --no-input --src=newSrc
```

### 2. `run`

Runs Python File

```commandline
pipcx run
```
Will run src/main.py by default

```
picx run src/test.py
```
Will Run test.py

### 3. `createtest`

Runs Python File

```commandline
pipcx createtest
```
Will generate `tests` folder for pytest

### 4. `install`

```
pipcx install django
```
Will install libraries and add to config file

### 5. `uninstall`
```
pipcx uninstall flask
```
Will uninstall library and remove from config file
