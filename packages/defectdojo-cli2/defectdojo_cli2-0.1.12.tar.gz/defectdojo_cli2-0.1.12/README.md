# DefectDojo CLI

[![License](https://img.shields.io/badge/license-MIT-_red.svg)](https://opensource.org/licenses/MIT)

A CLI wrapper for [DefectDojo](https://github.com/DefectDojo/django-DefectDojo)

## Installation

Simply run:

```sh
python3 -m pip install defectdojo-cli2
```

This will install it as `defectdojo`.

## Usage

```sh
defectdojo --help
```

### Upload scans

Example:

```sh
defectdojo reimport_scan upload --product_name="test dd" --engagement_name="DefectDojoImporter" --scan_type="GitLab Container Scan" --active --verified --test_title="GitLab Container Scan" --file=gl-container-scanning.json
```

This wil upload a Gitlab Container Scan report to DefectDojo to the product named `test dd` and engagement called `DefectDojoImporter` and name the test GitLab Container Scan, if it exists it do a reimport on that test, if it doesn't exists, it will create a new test with that name. If you name the engagement to something that doesn't already exists, it will create a name engagement with the provided name.

### Upload languages

Example:

```sh
defectdojo import_languages upload --product=21 --file=cloc.json
```

This will upload a language file for a project (normally generated with [cloc](https://github.com/AlDanial/cloc)) to the product with the id provided.

## Development

```sh
poetry env use /usr/local/bin/python3 # = your full path to the Python executable.
poetry install
poetry run python3 defectdojo_cli2
```

Update dependencies <https://github.com/MousaZeidBaker/poetry-plugin-up>

```sh
poetry self add poetry-plugin-up
poetry up
```

## Using environment variables

The goal of this cli is not only to be used as a cli tool for accessing DefectDojo API, but also to be able to run automated jobs in a CI environment, like importing scans to DefectDojo.

To use Defectdojo CLI in a CI context, there is `DEFECTDOJO_` prefixed environment variables you could set. This, so you don't need to provide the arguments.

```sh
DEFECTDOJO_API_KEY
DEFECTDOJO_BRANCH_TAG
DEFECTDOJO_COMMIT_HASH
DEFECTDOJO_ENGAGEMENT_END_DATE
DEFECTDOJO_ENGAGEMENT_ID
DEFECTDOJO_ENGAGEMENT_NAME
DEFECTDOJO_LANGUAGES_FILE
DEFECTDOJO_PASSWORD
DEFECTDOJO_PRODUCT_ID
DEFECTDOJO_PRODUCT_NAME
DEFECTDOJO_PUSH_TO_JIRA
DEFECTDOJO_SCAN_TYPE
DEFECTDOJO_TEST_NAME
DEFECTDOJO_TEST_TITLE
DEFECTDOJO_TEST_TYPE
DEFECTDOJO_URL
DEFECTDOJO_USER_NAME
```

## Docker images

Docker images containing defectdojo cli is [published on docker hub](https://hub.docker.com/repository/docker/digitalist/defectdojo-cli2/general).

## Example of running defectdojo cli in GitLab Runner

To upload results of GitLab Container Scan:

```yaml
defectdojo:upload:container:scanning:
  image: digitalist/defectdojo-cli2:latest
  needs:
    - job: container_scanning
      artifacts: true
  stage: .post
  variables:
    GIT_STRATEGY: none
    DEFECTDOJO_API_KEY: c1ca1f4193f2460f9f6a3dab22b723ab
    DEFECTDOJO_URL: https://defectdojo.url
    DEFECTDOJO_ENGAGEMENT_NAME: "Gitlab Runner"
    DEFECTDOJO_PRODUCT_NAME: ${CI_PROJECT_TITLE}
    DEFECTDOJO_BRANCH_TAG: ${CI_COMMIT_REF_NAME}
    DEFECTDOJO_COMMIT_HASH: ${CI_COMMIT_SHA}
    DEFECTDOJO_SCAN_TYPE: "GitLab Container Scan"
    DEFECTDOJO_TEST_TITLE: "GitLab Container Scan"
  script:
    - defectdojo reimport_scan upload --file=gl-container-scanning-report.json

```

To upload results of cloc (languages) to project number 42 in DefectDojo:

```yaml
defectdojo:upload:cloc:
  image: digitalist/defectdojo-cli2:latest
  needs:
    - job: cloc
      artifacts: true
  variables:
    DEFECTDOJO_API_KEY: c1ca1f4193f2460f9f6a3dab22b723ab
    DEFECTDOJO_URL: https://defectdojo.url
    DEFECTDOJO_PRODUCT_ID: 42
  script:
    - defectdojo import_languages upload --file=cloc.json

```

## Fork

This started as a fork of <https://github.com/adiffpirate/defectdojo-cli>.
