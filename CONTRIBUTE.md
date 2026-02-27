# Contributing to Skupper v2 Ansible Collection

## Getting Started

Thank you for your interest in contributing to the Skupper v2 Ansible collection! This guide will help you set up your development environment and understand our contribution process.

## Prerequisites

- Python 3.9 or higher
- Ansible 2.15 or later
- Git
- pip

## Local Development Setup

1. **Clone the repository**
  ```bash
  mkdir -p ansible_collections/skupper
  cd ansible_collections/skupper
  git clone https://github.com/skupperproject/skupper-ansible.git v2
  cd v2
  ```
  > **Note:** The repository must be cloned into the `ansible_collections/skupper/v2` directory structure as shown above. This directory layout is required for proper Ansible collection discovery and functionality.

2. **Create a virtual environment**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

3. **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```

4. **Run the setup command**
  ```bash
  make all
  ```
  > **Note:** This command ensures your environment is properly configured and all necessary dependencies are installed.

## Development Workflow

- Create a feature branch: `git checkout -b your-feature`
- Make your changes and write tests
- Run linting and tests locally
- Commit with clear messages
- Submit a pull request

## Running Tests

```bash
make all integration
```

## Prerequisites for Integration Tests

> **Note:** To run integration tests, ensure you have access to a valid Kubernetes cluster. Additionally, verify that the following tools are available on your system:
> - Podman 4.0 or higher
> - Docker
> - `skrouterd` (skupper-router binary)
>
> These prerequisites are required for testing Skupper v2 functionality within your development environment.

## Code Standards

- Follow PEP 8 style guidelines
- Include docstrings for modules and roles
- Write tests for new functionality
- Update documentation as needed

## Reporting Issues

Found a bug? Please create an issue with:
- Description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Environment details

## License

By contributing, you agree that your contributions will be licensed under the project's license.
