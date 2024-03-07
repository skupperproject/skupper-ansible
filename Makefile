TARBALL := $(shell echo "skupper/skupper/skupper-skupper-`grep -E '^version:' skupper/skupper/galaxy.yml | awk '{print $$NF}'`.tar.gz")

all: ansible-lint build-docs

dep:
	pip install -r ./requirements.txt
	pip install -r ./skupper/skupper/tests/unit/requirements.txt
	pip install -r ./skupper/skupper/docs/requirements.txt

ansible-lint:
	cd skupper/skupper && ansible-lint -v

release-changelog:
	pip install --user -U antsibull-changelog
	cd skupper/skupper && antsibull-changelog release

build-docs: build install
	rm -rf ./skupper/skupper/docs/*
	antsibull-docs sphinx-init --use-current --dest-dir ./skupper/skupper/docs skupper.skupper
	(cd skupper/skupper/docs && pip install --user -U -r requirements.txt && ./build.sh) && \
	rm -rf ./docs && mv skupper/skupper/docs/build/html/ ./docs && touch ./docs/.nojekyll
	rm -rf ./skupper/skupper/docs/*

build: clean 
	cd skupper/skupper && ansible-galaxy collection build

clean:
	@[[ -f "$(TARBALL)" ]] && rm $(TARBALL) || true

install:
	@[[ -f "$(TARBALL)" ]] && true || (echo "Collection has not been built" && false)
	@ansible-galaxy collection install -f "$(TARBALL)"

sanity-tests:
	cd skupper/skupper && ansible-test sanity -v --color

unit-tests:
	cd skupper/skupper && ansible-test units -vvv --color

e2e-setup:
	cd examples/hello-world && ansible-playbook -i inventory.yml setup.yml

e2e-validate:
	cd examples/hello-world && ansible-playbook -i inventory.yml test.yml

e2e-teardown:
	cd examples/hello-world && ansible-playbook -i inventory.yml teardown.yml

e2e-test: e2e-setup e2e-validate e2e-teardown
