# KeyVault

## Introduction

Simple, fast, convenient! KeyVault is a lightweight solution for centralizing the management of cloud service keys, particularly in development environments. It provides a centralized point for storing and retrieving API keys and secrets, streamlining the development process and enhancing security practices.

Key features and benefits include:

- Centralized storage of API keys and secrets
- Easy integration with development workflows
- Simplified key management across multiple projects
- Improved security through centralized access control
- Configurable storage location for secrets
- Production-ready with Waitress WSGI server

## Features

- Secure storage of key-value pairs
- RESTful API for key retrieval and listing
- Python client for easy integration
- Configurable secret storage location
- Logging and improved error handling
- Waitress WSGI server for production deployment

## Prerequisites

- Python 3.7+

## Installation

You can install KeyVault using pip:

```bash
pip install keyvault-llm
```

Or directly from the GitHub repository:

```bash
pip install git+https://github.com/ltoscano/keyvault.git
```

## Quickstart

1. Create a configuration file:

   ```json
   {
     "OPENAI_API_KEY": "your-api-key-here",
     "OTHER_KEY": "another-key-value"
   }
   ```

   Save this as `config.json` in a secure location.

2. Start the KeyVault server:

   ```bash
   python -m keyvault_llm.server --config /path/to/config.json
   ```

   By default, the server will run on `http://localhost:38680`. You can change the host and port using the `--host` and `--port` options.

3. Use the client to interact with the server:

   ```python
   from keyvault_llm.client import KeyVaultClient
   import logging

   logging.basicConfig(level=logging.INFO)

   client = KeyVaultClient("http://localhost:38680")

   try:
       # Get a specific key
       api_key = client.get_key('OPENAI_API_KEY')
       print("API Key:", api_key)

       # List all keys
       keys = client.list_keys()
       print("Available keys:", keys)
   except Exception as e:
       print(f"An error occurred: {str(e)}")
   ```

## Configuration

KeyVault can be configured using command-line arguments when starting the server:

- `--config`: Path to the config.json file (default: ~/.keyvault/config.json)
- `--host`: Host to bind the server to (default: 0.0.0.0)
- `--port`: Port to run the server on (default: 38680)

Example:

```bash
python -m keyvault_llm.server --config /path/to/config.json --host 127.0.0.1 --port 8080
```

## Security Considerations

KeyVault is designed for use in development environments. While it can be used in production with proper security measures, it's essential to consider the following:

1. **Access Control**: Ensure that the KeyVault server is only accessible within your trusted network.
2. **Secure Configuration**: Store your `config.json` file in a secure location with appropriate file permissions.
3. **HTTPS**: For production use, configure KeyVault behind a reverse proxy with HTTPS enabled.
4. **Regular Updates**: Keep your KeyVault installation up to date with the latest security patches.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
