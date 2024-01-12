# Grafana Container

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
4. [Generate SSL Certificate](#generate-ssl-certificate)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

## Introduction

This project provides a containerized version of Grafana, an open-source platform for monitoring and observability. It's designed to be easy to deploy and manage, making it ideal for environments that benefit from containerization. The Grafana Container offers a scalable way to visualize and analyze metrics, logs, and traces from your environment.

## Features

- Easy to deploy Grafana in a containerized environment.
- Configurable settings for different monitoring needs.
- Integration with various data sources.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system.
- Basic understanding of containerization and Grafana.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/benjisho/grafana-container.git
```

2. Navigate to the cloned directory:

```bash
cd grafana-container
```

## Generate SSL certyificate into `certs/` directory

> **Note:** This section is relevant if you haven't generated a well-known SSL certificate from a certified authority.
> These will guide you on creating a self-signed certificate, useful for testing or development purposes.

1. Run the following command to generate a 2048-bit RSA private key, which is used to decrypt traffic:

```bash
openssl genrsa -out certs/server.key 2048
```

2. Run the following command to generate a certificate, using the private key from the previous step.

```bash
openssl req -new -key certs/server.key -out certs/server.csr
```

3. Run the following command to self-sign the certificate with the private key, for a period of validity of 365 days:

```bash
openssl x509 -req -days 365 -in certs/server.csr -signkey certs/server.key -out certs/server.crt
```

## Usage

To use the Grafana Container:

1. Start the container:

```bash
docker-compose up -d
```

2. Access Grafana by navigating to `https://localhost` in your web browser.
3. Default login user is usually `admin` for both username and password (unless configured otherwise).
4. Configure data sources and dashboards as per your requirements.

> For example, to add a Prometheus data source:
>
> - Navigate to `Configuration > Data Sources` in the Grafana UI.
> - Click `Add data source`, and select `Prometheus`.
> - Enter the URL of your Prometheus server, and click `Save & Test`.

5. Explore and create dashboards to visualize your data.
   For more detailed usage instructions, refer to the [Grafana documentation](https://grafana.com/docs/).

## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
