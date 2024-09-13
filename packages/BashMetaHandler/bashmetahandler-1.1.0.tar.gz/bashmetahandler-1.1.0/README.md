# BashMetaHandler

[![PyPI](https://img.shields.io/pypi/v/BashMetaHandler.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/BashMetaHandler.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/BashMetaHandler)][python version]
[![License](https://img.shields.io/pypi/l/BashMetaHandler)][license]

[![Read the documentation at https://BashMetaHandler.readthedocs.io/](https://img.shields.io/readthedocs/BashMetaHandler/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/000AG000/BashMetaHandler/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/000AG000/BashMetaHandler/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/BashMetaHandler/
[status]: https://pypi.org/project/BashMetaHandler/
[python version]: https://pypi.org/project/BashMetaHandler
[read the docs]: https://BashMetaHandler.readthedocs.io/
[tests]: https://github.com/000AG000/BashMetaHandler/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/000AG000/BashMetaHandler
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

It provites an interpreter for a own bash meta languange. Currently only tested for linux systems.

## Requirements

click>=8.1.7 ; python_version >= "3.7" and python_version < "4.0"
colorama>=0.4.6 ; python_version >= "3.7" and python_version < "4.0" and platform_system == "Windows"
datetime>=5.5 ; python_version >= "3.7" and python_version < "4.0"
importlib-metadata>=4.2.0 ; python_version >= "3.7" and python_version < "3.8"
pexpect>=4.9.0 ; python_version >= "3.7" and python_version < "4.0"
ptyprocess>=0.7.0 ; python_version >= "3.7" and python_version < "4.0"
pytz>=2024.1 ; python_version >= "3.7" and python_version < "4.0"
setuptools>=68.0.0 ; python_version >= "3.7" and python_version < "4.0"
typing-extensions>=4.7.1 ; python_version >= "3.7" and python_version < "3.8"
zipp>=3.15.0 ; python_version >= "3.7" and python_version < "3.8"
zope-interface>=6.4.post2 ; python_version >= "3.7" and python_version < "4.0"

## Installation

You can install _bmh_ via [pip] from [PyPI]:

```console
$ pip install BashMetaHandler
```

## Usage

The main purpose of this library is to provide an interpreter for the self-created metabashlanguage. The MetaBashHandler-class handles this interpretation. When on object of this class is created it initiates a bash terminal where the interpreted language is executed.

Firstly, it a provided file is read and lines for the goto-command are searched and indexed. They must be a word followed by an ":".Secondly, the execute_file function will run the interpreter.

The metabashlanguange has normally the ending ".msh". When not a special case the input goes directly to the bash terminal. It has the advantage to not care whether you are directly in the bash terminal are input of a program run by the terminal. Keywords implemented are: while, if, elif, else. When used you have to use a tab to indicate how long these keywords effect should be (similar to python).

Additionally you are provided with functions to be used. They are used as follows functionname(arg1,arg2,...). There are a few prebuild functions to use given as default parameters to the MetaBashHandler. These are: check, do_not, equal, expect, expect_check, get_input, println and wait. The actual functionname are sometimes different to the actual python functionnames. You can also create your own function, the first argument should always be the MetaBashHandler object.

Finally there you can use variables indicated by $(variable name). They will be replaced with the content of the variable given to the MetaBashHandler object.

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_bmh_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/000AG000/BashMetaHandler/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/000AG000/BashMetaHandler/blob/main/LICENSE
[contributor guide]: https://github.com/000AG000/BashMetaHandler/blob/main/CONTRIBUTING.md
[command-line reference]: https://BashMetaHandler.readthedocs.io/en/latest/usage.html
