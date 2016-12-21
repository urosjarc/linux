VIRTUAL_ENV = virtualenv
PATH := $(VIRTUAL_ENV)/bin:$(PATH)
export CODACY_PROJECT_TOKEN=%Project_Token%

.PHONY: clean clean-test clean-pyc clean-build docs help test
.DEFAULT_GOAL := help


define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url
webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"


define PRINT_HELP_PYSCRIPT
import re, sys
for line in sys.stdin:
	match = re.match(r'^### (.*) #', line)
	if match:
		target = match.groups()[0]
		print("\n%s" % (target))
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("  %-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)
