PYTHON=`which python`
NAME=`python setup.py --name`
VERSION=`python setup.py --version`

init:
	pip install -r requirements.txt --use-mirrors