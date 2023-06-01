all: ansible-lint build

ansible-lint:
	cd skupper/network && ansible-lint --skip-list 'var-naming[pattern],var-naming[no-role-prefix]'

release-changelog:
	pip install --user -U antsibull-changelog
	cd skupper/network && antsibull-changelog release

build-docs:
	cd skupper/network/docs && pip install --user -U -r requirements.txt && ./build.sh && \
		rm -rf html && cp -r build/html/ ./

build: build-docs
	cd skupper/network && ansible-galaxy collection build
