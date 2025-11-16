SHELL := /bin/bash

TEST_PYTHON_VERSION ?= 3.11
VENV ?= .venv
PYTHON ?= python$(TEST_PYTHON_VERSION)
REQUIREMENTS ?= requirements.txt
VENV_STAMP := $(VENV)/.deps-installed
ANSIBLE_TEST := $(VENV)/bin/ansible-test
UNIT_PYTHON ?= $(TEST_PYTHON_VERSION)
#DOCKER_TARGET ?= default
#DOCKER_FLAG := --docker $(DOCKER_TARGET)
VM_TARGET_FILE ?= .vm_target
VM_TARGET := $(strip $(shell test -f $(VM_TARGET_FILE) && cat $(VM_TARGET_FILE)))
VM_TARGET_PYTHON ?= $(TEST_PYTHON_VERSION)

# Support "make integration <target_name>"
ifeq ($(firstword $(MAKECMDGOALS)),integration)
  INTEGRATION_NAME := $(word 2,$(MAKECMDGOALS))
  ifneq ($(INTEGRATION_NAME),)
    $(INTEGRATION_NAME):
    	@:
  endif
endif

.PHONY: venv sanity unit integration units integrations docs all clean-venv

venv: $(VENV_STAMP)

$(VENV_STAMP): $(REQUIREMENTS)
	@echo "Setting up virtualenv in $(VENV)..."
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@$(VENV)/bin/pip install --upgrade pip
	@$(VENV)/bin/pip install -r $<
	@touch $@

sanity: venv
	$(ANSIBLE_TEST) sanity --python $(UNIT_PYTHON)

unit: venv
	$(ANSIBLE_TEST) units --python $(UNIT_PYTHON) -v

units: unit

integration: venv
ifeq ($(VM_TARGET),)
	@echo "Missing $(VM_TARGET_FILE); create it with user@host to run live integration tests."
	@exit 1
else
	$(ANSIBLE_TEST) integration $(if $(INTEGRATION_NAME),$(INTEGRATION_NAME)) --allow-unsupported --target "ssh:$(VM_TARGET),python=$(VM_TARGET_PYTHON)" $(INTEGRATION_DEBUG)
endif

integrations: integration

all: sanity unit integration

docs: venv
	$(VENV)/bin/antsibull-docs collection \
	  --use-current \
	  --dest-dir docs \
	  --squash-hierarchy \
	  --output-format simplified-rst \
	  mareckii.truenas_scale

clean-venv:
	rm -rf $(VENV)
# Allow "make integration DEBUG=1" to append -vvv
ifdef DEBUG
  INTEGRATION_DEBUG := -vvv
endif
