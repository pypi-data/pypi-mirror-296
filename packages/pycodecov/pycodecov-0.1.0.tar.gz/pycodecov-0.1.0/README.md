# pycodecov

[![Test](https://github.com/kiraware/pycodecov/workflows/Test/badge.svg)](https://github.com/kiraware/pycodecov/actions/workflows/test.yml)
[![CodeQL](https://github.com/kiraware/pycodecov/workflows/CodeQL/badge.svg)](https://github.com/kiraware/pycodecov/actions/workflows/codeql.yml)
[![Docs](https://readthedocs.org/projects/pycodecov/badge/?version=latest)](https://pycodecov.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/kiraware/pycodecov/graph/badge.svg?token=PH6EUFT4V0)](https://codecov.io/gh/kiraware/pycodecov)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pypi](https://img.shields.io/pypi/v/pycodecov.svg)](https://pypi.org/project/pycodecov/)
[![python](https://img.shields.io/pypi/pyversions/pycodecov.svg)](https://pypi.org/project/pycodecov/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/license/MIT/)

`pycodecov` is an asynchronous API wrapper for the
[Codecov API](https://docs.codecov.com/reference/overview), designed
to streamline interaction with Codecov's services in Python. It
enables users to leverage Codecov's functionality asynchronously,
enhancing performance and usability.

## Key Features

- **Asynchronous Operations:** Utilizes `asyncio` and `aiohttp` for efficient API requests.
- **Data Schema:** Built with Python's `dataclass` for clear and structured data representation.
- **Comprehensive Documentation:** Explore detailed [documentation](https://pycodecov.readthedocs.io/en/latest/) for seamless integration and usage.

## Installation

```bash
pip install pycodecov
```

## Usage

```python
import asyncio
import os

from pycodecov import Codecov
from pycodecov.enums import Service

CODECOV_API_TOKEN = os.environ["CODECOV_API_TOKEN"]

async def main():
    async with Codecov(CODECOV_API_TOKEN) as codecov:
        service_owners = await codecov.get_service_owners(Service.GITHUB)
        print(service_owners)

asyncio.run(main())
```

## Docs

You can start reading the documentation [here](https://pycodecov.readthedocs.io/en/latest/).

## Contributing

We welcome contributions to enhance pycodecov! Please review our
[contributing guidelines](https://pycodecov.readthedocs.io/en/latest/how-to-guides/#contributing).
before getting started.

## Acknowledgements

We would like to thank [Codecov](https://about.codecov.io/)
for providing API services and also good documentation for
using the API.
