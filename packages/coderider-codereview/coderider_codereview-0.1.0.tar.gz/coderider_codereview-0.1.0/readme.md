# CodeRider CodeReview

## How to set up

Create `.env` file:

```.env
GITLAB_HOST=
CODERIDER_HOST=
AI_BOT_PERSONAL_ACCESS_TOKEN=
CI_MERGE_REQUEST_PROJECT_PATH=
CI_MERGE_REQUEST_IID=
```

Install dependencies:

```shell
poetry install
```

## Publish

https://pypi.org/project/coderider-codereview/

```shell
poetry config pypi-token.pypi <pypi-token>
poetry publish
```

## Use it in local

```shell
pip install coderider_codereview
AI_BOT_PERSONAL_ACCESS_TOKEN="" CI_MERGE_REQUEST_PROJECT_PATH="" CI_MERGE_REQUEST_IID="" crcr
```

## GitLab CI Template File

https://jihulab.com/-/snippets/6198

```yml
include:
  - remote: 'https://jihulab.com/-/snippets/6198/raw/main/coderider-codereview.yml'
```
