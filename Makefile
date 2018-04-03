.PHONY: default
default: run

.PHONY: run
run: virtualenv_run
	./virtualenv_run/bin/python main.py

virtualenv: virtualenv_run

virtualenv_run:
	virtualenv --python python3 virtualenv_run
	./virtualenv_run/bin/pip install -r ./requirements.txt
