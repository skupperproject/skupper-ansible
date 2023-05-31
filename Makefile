all: ansible-lint build

ansible-lint:
	cd skupper/network && ansible-lint --skip-list 'var-naming[pattern],var-naming[no-role-prefix]'

release-changelog:
	cd skupper/network && antsibull-changelog release

build:
	cd skupper/network && ansible-galaxy collection build
