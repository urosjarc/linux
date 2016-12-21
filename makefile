include config/makefile

#============================
### START DEVELOPING ########
#============================

init: clean ## start virtual environment and install dev. requirements
	rm -fr $(VIRTUAL_ENV)
	virtualenv -p python3 $(VIRTUAL_ENV) --distribute
	pip install -r requirements_dev.txt

#============================
### TESTING #################
#============================

test-CI: ## run CI tests
	tox

test: test-spec lint ## run test, lint

test-spec: ## run spec tests
	coverage run --source mylinux -m py.test test/spec
	coverage report -m
	coverage xml
	coverage html

test-e2e: ## run e2e tests
	py.test test/e2e

lint: ## check style with pylint
	pylint --reports=n --output-format=colorized mylinux tests

test-dep: ## test dependencies
	pip list --outdated

#============================
### DOCS ####################
#============================

docs: pdoc ## generate documentation
	$(BROWSER) build/docs/mylinux/index.html

codacy: test-spec ## upload codacy coverage report
	python-codacy-coverage -r coverage.xml

serve: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.md' -c '$(MAKE) docs' -R -D .

pdoc: ## generate pdoc html
	pdoc --html --overwrite --html-dir build/docs ./mylinux

#============================
### BUILD ###################
#============================

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

#============================
### CLEANING ################
#============================

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage coverage.xml
	rm -fr htmlcov/
