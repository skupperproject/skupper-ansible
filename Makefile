TARBALL := $(shell echo "skupper-v2-`grep -E '^version:' galaxy.yml | awk '{print $$NF}'`.tar.gz")

IMAGES = default fedora40 ubuntu2404
PYTHON = 3.12

all: clean unit coverage

dep:
	pip install -r ./requirements.txt
	pip install -r ./skupper/skupper/tests/unit/requirements.txt
	pip install -r ./skupper/skupper/docs/requirements.txt

ansible-lint:
	ansible-lint -v

release-changelog:
	pip install --user -U antsibull-changelog
	antsibull-changelog release

build-docs: build install
#    rm -rf docs/*
#    antsibull-docs sphinx-init --use-current --dest-dir ./docs/docsite skupper.v2
#    (cd docs && pip install --user -U -r requirements.txt && ./build.sh) && \
#    rm -rf ./docs && mv ./docs/build/html/ ./docs && touch ./docs/.nojekyll
#    rm -rf ./skupper/skupper/docs/*

build: clean
    ansible-galaxy collection build

clean:
	@[[ -f "$(TARBALL)" ]] && rm $(TARBALL) || true
	rm -rf tests/output

install:
	@[[ -f "$(TARBALL)" ]] && true || (echo "Collection has not been built" && false)
	@ansible-galaxy collection install -f "$(TARBALL)"

sanity-tests:
	ansible-test sanity -v --color

.PHONY: unit
unit:
	ansible-test units --color --coverage --python $(PYTHON) -v

.PHONY: unit-docker
unit-docker: $(foreach img,$(IMAGES),unit-docker-$(img))
unit-docker-%: clean
	ansible-test units --coverage --docker "$*" --python $(PYTHON) -v

integration:
	@echo ansible-test integration --docker default -v

coverage:
	ansible-test coverage html
