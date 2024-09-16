# ALEA Data Resources

[![PyPI version](https://badge.fury.io/py/alea-data-resources.svg)](https://badge.fury.io/py/alea-data-resources)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/alea-data-resources.svg)](https://pypi.org/project/alea-data-resources/)

## Description
This library provides functionality to download, cache, and access data resources used across ALEA projects, as well
as a centralized location for proper citation and licensing information for these resources.

## Installation

```bash
pip install alea-data-resources
```

Or as a `pipx` package for system-wide installation:

```bash
pipx install alea-data-resources
```

## Examples
```bash
# Download the CMU Pronouncing Dictionary
$ alea-data-resources download cmudict

# List all available data resources
$ alea-data-resources list

# List as JSON
$ alea-data-resources list --format json

# Delete a data resource
$ alea-data-resources delete cmudict
```

## License

This ALEA project is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions about using this ALEA project, please [open an issue](https://github.com/alea-institute/alea-data-resources/issues) on GitHub.

## Learn More

To learn more about ALEA and its software and research projects like KL3M, visit the [ALEA website](https://aleainstitute.ai/).
