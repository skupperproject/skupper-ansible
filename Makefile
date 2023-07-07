TARBALL := $(shell echo "skupper/network/skupper-network-`grep -E '^version:' skupper/network/galaxy.yml | awk '{print $$NF}'`.tar.gz")

all: ansible-lint build

ansible-lint:
	cd skupper/network && ansible-lint --skip-list 'var-naming[pattern],var-naming[no-role-prefix]'

release-changelog:
	pip install --user -U antsibull-changelog
	cd skupper/network && antsibull-changelog release

build-docs:
	rm -rf skupper/network/docs/build skupper/network/docs/temp-rst
	(cd skupper/network/docs && pip install --user -U -r requirements.txt && ./build.sh) && \
	rm -rf ./docs && mv skupper/network/docs/build/html/ ./docs

build: clean build-docs
	cd skupper/network && ansible-galaxy collection build

clean:
	@[[ -f "$(TARBALL)" ]] && rm $(TARBALL) || true

install:
	@[[ -f "$(TARBALL)" ]] && true || (echo "Collection has not been built" && false)
	@ansible-galaxy collection install -f "$(TARBALL)"
