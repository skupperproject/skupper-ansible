TARBALL := $(shell echo "skupper/core/skupper-core-`grep -E '^version:' skupper/core/galaxy.yml | awk '{print $$NF}'`.tar.gz")

all: ansible-lint build build-docs

dep:
	pip install -r ./requirements.txt
	pip install -r ./skupper/core/tests/unit/requirements.txt
	pip install -r ./skupper/core/docs/requirements.txt

ansible-lint:
	cd skupper/core && ansible-lint -v

release-changelog:
	pip install --user -U antsibull-changelog
	cd skupper/core && antsibull-changelog release

build-docs: build install
	rm -rf ./skupper/core/docs/*
	antsibull-docs sphinx-init --use-current --dest-dir ./skupper/core/docs skupper.core
	(cd skupper/core/docs && pip install --user -U -r requirements.txt && ./build.sh) && \
	rm -rf ./docs && mv skupper/core/docs/build/html/ ./docs && touch ./docs/.nojekyll

build: clean 
	cd skupper/core && ansible-galaxy collection build

clean:
	@[[ -f "$(TARBALL)" ]] && rm $(TARBALL) || true

install:
	@[[ -f "$(TARBALL)" ]] && true || (echo "Collection has not been built" && false)
	@ansible-galaxy collection install -f "$(TARBALL)"

sanity-tests:
	cd skupper/core && ansible-test sanity -v --color

unit-tests:
	cd skupper/core && ansible-test units -vvv --color

e2e-setup:
	cd examples/hello-world && ansible-playbook -i inventory.yml setup.yml

e2e-validate:
	cd examples/hello-world && ansible-playbook -i inventory.yml test.yml

e2e-teardown:
	cd examples/hello-world && ansible-playbook -i inventory.yml teardown.yml

e2e-test: e2e-setup e2e-validate e2e-teardown
