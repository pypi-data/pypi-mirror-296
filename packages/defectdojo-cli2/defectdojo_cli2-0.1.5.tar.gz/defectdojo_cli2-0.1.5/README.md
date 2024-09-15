# DefectDojo CLI

[![License](https://img.shields.io/badge/license-MIT-_red.svg)](https://opensource.org/licenses/MIT)

A CLI wrapper for [DefectDojo](https://github.com/DefectDojo/django-DefectDojo)

## Fork

This has been forked from <https://github.com/adiffpirate/defectdojo-cli>.

## Installation

Simply run:

```sh
python3 -m pip install defectdojo-cli2
```

## Usage

```sh
defectdojo --help
```

## Development

```sh
poetry env use /usr/local/bin/python3 # = your full path to the Python executable.
poetry install
poetry run python3 defectdojo_cli2


```

## WIP: DefectDojo for CI

The goal of this cli is not only to be used as a cli tool for accessing DefectDojo API, but also to be able to run automated jobs in a CI environment, like importing scans to DefectDojo.

We will publish a docker container when all needed basics are in place, to run DefectDojo CLI for this.

To use Defectdojo CLI in a CI context, there is DEFECTDOJO prefixed environment variables you could set. This, so you don't need to provide the arguments.

```sh
DEFECTDOJO_URL
DEFECTDOJO_API_KEY
DEFECTDOJO_PRODUCT_ID
DEFECTDOJO_ENGAGEMENT_ID
DEFECTDOJO_TEST_TYPE
DEFECTDOJO_USER_NAME
DEFECTDOJO_PASSWORD
```
