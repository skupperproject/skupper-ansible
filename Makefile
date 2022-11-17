all: ansible-lint build

ansible-lint:
	cd skupper/network && ansible-lint

build:
	cd skupper/network && ansible-galaxy collection build
