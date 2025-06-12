# Useful Scripts for Grafana Container

This directory contains scripts that are helpful for setting up the Grafana Container environment. Specifically, there are scripts for installing Docker on Debian and Ubuntu systems. These scripts automate the process of setting up Docker, which is a prerequisite for running the Grafana Container.

## Scripts

### 1. `install_docker_debian.sh`

This script automates the installation of Docker on Debian systems (specifically tested on Debian 11.8). It performs the following steps:

- Uninstalls old or conflicting Docker packages.
- Sets up Docker's apt repository.
- Installs Docker Engine.
- Verifies the installation by running a test Docker container.

To run the script, execute:

```bash
sudo bash install_docker_debian.sh
```

## Usage

To use these scripts:

1. Ensure you have `sudo` privileges on your Debian or Ubuntu system.
1. Download the script corresponding to your operating system.
1. Give execute permission to the script (if necessary) using `chmod +x script_name.sh`.
1. Run the script with `sudo`.

> **Note:** These scripts are intended for quick setup in a development environment.
> For production environments, please review and modify the scripts as needed to suit your security and configuration requirements.

## Pre-commit Hook

To ensure code quality, a pre-commit hook is configured for linting Dockerfiles using hadolint. The configuration is as follows:

```yaml
-   id: hadolint
    name: Lint Dockerfiles with hadolint
    entry: hadolint
    language: system
    types: [dockerfile]
```

## Contributing

Contributions to improve these scripts or add new ones are welcome. Please follow the standard process of forking the repository, making your changes, and submitting a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file in the main directory for details.
