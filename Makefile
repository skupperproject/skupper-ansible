VERSION := 2.0.0
TARBALL := skupper-v2-$(VERSION).tar.gz

IMAGES = default fedora40 ubuntu2404
PYTHON ?= `python -c 'import platform; print(".".join(platform.python_version_tuple()[0:2]))'`
PYTHON_DOCKER = 3.12

INTEGRATION_TARGETS = resource system

OPTIONS ?=

all: clean lint sanity unit coverage

lint:
	ansible-galaxy collection install -r tests/integration/requirements.yml
	ANSIBLE_ROLES_PATH=./tests/integration/targets ANSIBLE_LIBRARY=./plugins/modules ANSIBLE_MODULE_UTILS=./plugins/module_utils ansible-lint -v --offline

release-changelog:
	pip install --user -U antsibull-changelog
	antsibull-changelog release -v

build-docs: build install
	pip install --user -U virtualenv
	rm -rf docs/* && mkdir docs/docsite
	antsibull-docs sphinx-init --use-current --dest-dir ./docs/docsite skupper.v2
	pip install -U -r docs/docsite/requirements.txt
	./docs/docsite/build.sh
	mv ./docs/docsite/build/html/* ./docs
	touch ./docs/.nojekyll
	rm -rf ./docs/docsite

build: clean
	ansible-galaxy collection build

clean:
	@[ -f "$(TARBALL)" ] && rm $(TARBALL) || true
	rm -rf tests/output

install:
	@[ -f "$(TARBALL)" ] && true || (echo "Collection has not been built" && false)
	@ansible-galaxy collection install -f "$(TARBALL)"

publish: build
	@[ -f "$(TARBALL)" ] && true || (echo "Collection has not been built" && false)
	@ansible-galaxy collection publish "$(TARBALL)"

sanity:
	ansible-test sanity --color --docker -v --python $(PYTHON) --requirements plugins/

.PHONY: unit
unit:
	pip install -r ./tests/unit/requirements.txt -U
	ansible-test units --color --coverage --python $(PYTHON) -v

.PHONY: unit-docker
unit-docker: $(foreach img,$(IMAGES),unit-docker-$(img))
unit-docker-%: clean
	ansible-test units --coverage --docker "$*" --python $(PYTHON_DOCKER) -v

integration:
	ansible-test integration --allow-destructive --local -v $(OPTIONS)

integration-ssh:
	ansible-test integration --allow-destructive --target "ssh:`id -un`@localhost,python=$(PYTHON)" -v $(OPTIONS)

coverage:
	ansible-test coverage html || true
