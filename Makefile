TARBALL := $(shell echo "skupper-v2-`grep -E '^version:' galaxy.yml | awk '{print $$NF}'`.tar.gz")

IMAGES = default fedora40 ubuntu2404
PYTHON = 3.12

all: clean lint sanity unit coverage

dep:
	pip install -r ./tests/unit/requirements.txt -U

lint:
	ansible-lint -v

release-changelog:
	pip install --user -U antsibull-changelog
	antsibull-changelog release

build-docs: build install
	pip install --user -U virtualenv
	rm -rf docs/* && mkdir docs/docsite
	antsibull-docs sphinx-init --use-current --dest-dir ./docs/docsite skupper.v2
	pip install -U -r docs/docsite/requirements.txt
	./docs/docsite/build.sh
	mv ./docs/docsite/build/html ./docs
	touch ./docs/.nojekyll
	rm -rf ./docs/docsite

build: clean
	ansible-galaxy collection build

clean:
	@[[ -f "$(TARBALL)" ]] && rm $(TARBALL) || true
	rm -rf tests/output

install:
	@[[ -f "$(TARBALL)" ]] && true || (echo "Collection has not been built" && false)
	@ansible-galaxy collection install -f "$(TARBALL)"

sanity:
	ansible-test sanity --color --docker -v --python $(PYTHON) --requirements plugins/

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
