include config/makefile

#============================
### START DEVELOPING ########
#============================

init: clean ## start virtual environment and install dev. requirements
	rm -fr $(VIRTUAL_ENV)
	virtualenv -p python3 $(VIRTUAL_ENV) --distribute
	pip install -r requirements_dev.txt
	pip install -e .

run: ## run package script
	python mylinux/cli/main.py ${ARGS}

#============================
### TESTING #################
#============================

test: test-spec lint ## run test, lint

test-all: ## run CI tests
	tox

test-spec: ## run spec tests
	coverage run --source $(PACKAGE) -m py.test test/spec
	coverage report -m
	coverage html

test-e2e: ## run e2e tests
	py.test test/e2e

lint: ## check style with pylint
	pylint --reports=n --output-format=colorized $(PACKAGE) tests

dep: ## test dependencies
	pip list --outdated --format=columns
	@if [ -z "$$(pip list --outdated --format=columns)" ]; then exit 0; else exit 1; fi


#============================
### DOCS ####################
#============================

docs: ## generate documentation
	cp README.md docs/index.md
	cp CONTRIBUTING.md docs/contribution.md
	github_changelog_generator  \
		--user urosjarc \
		--project $(PACKAGE) \
		--date-format %d.%m.%Y \
		--output docs/changelog.md \
		--header-label --no-verbose \
		--token ad9f253d490a97d73a55bd1992224a3bc00aecf9
	mkdocs build --strict --clean --quiet --config-file config/mkdocs.yml
	pdoc --html --overwrite --html-dir build/api-docs $(PACKAGE)
	cp build/api-docs/$(PACKAGE)/* build/docs/documentation
	$(MAKE) clean-docs

serve: docs ## compile the docs watching for changes
	$(BROWSER) build/docs/index.html
	watchmedo shell-command -p '*.md' -c \
		'$(MAKE) docs && $(BROWSER) build/docs/index.html' -R -D .

#============================
### INTEGRATIONS ############
#============================

codacy: test-spec ## upload coverage report
	coverage xml
	python-codacy-coverage -r coverage.xml

gh-deploy: docs ## upload docs to gh-pages
	mkdocs gh-deploy --message $(NOW_DATE) --config-file config/mkdocs.yml

pip: clean dist ## package and upload a release
	twine upload dist/*

#============================
### BUILD ###################
#============================

deb: dist ## create debian package
	py2dsc-deb dist/*.tar.gz

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

patch: ## bump version to patch
	bumpversion patch

minor: ## bump version to patch
	bumpversion minor

major: ## bump version to patch
	bumpversion major

#============================
### CLEANING ################
#============================

clean: clean-build clean-pyc clean-test clean-docs ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr deb_dist/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.tar.gz' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage coverage.xml
	rm -fr htmlcov/

clean-docs: ## remove docs artifacts
	rm -f docs/index.md
	rm -f docs/contribution.md
	rm -f docs/changelog.md
