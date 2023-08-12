.PHONY: update clean quality release

update:
	pip install --upgrade pip
	pip install --upgrade --upgrade-strategy eager -e ".[dev]"

clean:
	rm -rf dist
	rm -rf .pytest_cache

quality:
	black --check .
	flake8

release:
	fullrelease
	pip install -e ".[dev]"

# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = documentation/source
BUILDDIR      = documentation/build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
