PYTHON_INTERPRETER = python3

create_metadata:
	$(PYTHON_INTERPRETER) setup.py develop

requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	$(PYTHON_INTERPRETER) -m pip install -e .

requirements_devel:
	$(PYTHON_INTERPRETER) -m pip install -r requirements_devel.txt

styling:
	black MultiAgentAlg
	isort MultiAgentAlg
	flake8 MultiAgentAlg

typing:
	mypy MultiAgentAlg

create_requirements:
	pipreqs --force --savepath requirements.txt MultiAgentAlg

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
