Command Broker
_________________

[![PyPI version](https://badge.fury.io/py/command_broker.svg)](http://badge.fury.io/py/command_broker)
[![Test Status](https://github.com/brad/command_broker/workflows/Test/badge.svg?branch=develop)](https://github.com/brad/command_broker/actions?query=workflow%3ATest)
[![Lint Status](https://github.com/brad/command_broker/workflows/Lint/badge.svg?branch=develop)](https://github.com/brad/command_broker/actions?query=workflow%3ALint)
[![codecov](https://codecov.io/gh/brad/command_broker/branch/main/graph/badge.svg)](https://codecov.io/gh/brad/command_broker)
[![Join the chat at https://gitter.im/brad/command_broker](https://badges.gitter.im/brad/command_broker.svg)](https://gitter.im/brad/command_broker?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/command_broker/)
[![Downloads](https://pepy.tech/badge/command_broker)](https://pepy.tech/project/command_broker)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)
_________________

[Read Latest Documentation](https://brad.github.io/command_broker/) - [Browse GitHub Code Repository](https://github.com/brad/command_broker/)
_________________

**cmdbroker** Broker commands to a server

## Overview

Command Broker (cmdbroker) is a tool that allows a client to send commands to a server and get the results back. While for most use cases you can simply run commands over SSH, cmdbroker is designed for scenarios where you need to run commands with access to the server's UI. This can be particularly useful for commands that require graphical interfaces or other UI elements that are not accessible through standard SSH sessions.

## Features

- **Client-Server Architecture**: cmdbroker uses a client-server model to facilitate command execution and result retrieval.
- **SSL Encryption**: All communications between the client and server are secured using SSL, ensuring that data is encrypted and protected from eavesdropping.
- **UI Access**: Enables running commands that require access to the server's UI, which is not possible with standard SSH.
- **Easy Integration**: Simple to integrate into existing workflows and systems.

## Installation

You can install cmdbroker using pip:

```bash
pip install cmdbroker
