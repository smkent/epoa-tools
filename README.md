# epoa-tools: WA EPOA pay transparency tools

[![Build](https://img.shields.io/github/checks-status/smkent/epoa-tools/main?label=build)][gh-actions]
[![codecov](https://codecov.io/gh/smkent/epoa-tools/branch/main/graph/badge.svg)][codecov]
[![GitHub stars](https://img.shields.io/github/stars/smkent/epoa-tools?style=social)][repo]

[Washington state's Equal Pay and Opportunities Act][li-epoa] requires pay
ranges to be included on job ads ([RCW 49.58.110][rcw]). WA L&I provides a [PDF
complaint form][li-complaint-form] for violations. `epoa-tools` automates some
of the toil around this form, such as filling out basic information, checking
the right boxes, and optionally including additional PDF files as evidence (e.g.
the related job posting without pay range information).

The output is a single PDF which can be dropped into [WA L&I's secure file
upload][li-file-upload].

## Prerequisites

`epoa-tools` depends on `pdftk` for filling out forms and joining pages.

On Debian / Ubuntu, install with:

```shell
sudo apt install pdftk-java
```

## Installation

```
pip install epoa-tools
```

## Usage

Save a PDF file with evidence of the violation (e.g. job ad or recruiter email).
Browsers can print or save web pages as PDFs.

Then, use `epoa-job-ad` to complete the complaint form, attaching your evidence
file:

```shell
epoa-job-ad \
    --name "John Q. Public" --email john.q.public@example.com \
    "ACME Anti-Pay Ranges, Inc." \
    saved_job_ad.pdf
```

To file anonymously, omit the `--name` argument. The complainant name on the
form will be listed as `Anonymous` and the signature line will contain
`Anonymous (your.email.address@example.com)`:

```shell
epoa-job-ad \
    --email anon.e.mouse@example.com \
    "ACME Anti-Pay Ranges, Inc." \
    saved_job_ad.pdf
```

Optionally include additional information text about your complaint with the
`-i` / `--addinfo` / `--additional-information` option:

```shell
epoa-job-ad \
    --email anon.e.mouse@example.com \
    "ACME Anti-Pay Ranges, Inc." \
    saved_job_ad.pdf \
    -i "This job ad is public, contains specific job requirements for a job in WA, but lists no pay range"
```

Word(s) can be redacted from evidence file attachments on a best effort basis:
```shell
epoa-job-ad \
    --email anon.e.mouse@example.com \
    "ACME Anti-Pay Ranges, Inc." \
    saved_job_ad.pdf \
    -r remove_this_word -r also_remove_this_word
```

Each of these examples creates a file such as
`john-q-public-acme-anti-pay-ranges-inc-20230101-pay-transparency-complaint.pdf`
which can then be [uploaded to WA L&I][li-file-upload].

## Development

### [Poetry][poetry] installation

Via [`pipx`][pipx]:

```console
pip install pipx
pipx install poetry
pipx inject poetry poetry-dynamic-versioning poetry-pre-commit-plugin
```

Via `pip`:

```console
pip install poetry
poetry self add poetry-dynamic-versioning poetry-pre-commit-plugin
```

### Development tasks

* Setup: `poetry install`
* Run static checks: `poetry run poe lint` or
  `poetry run pre-commit run --all-files`
* Run static checks and tests: `poetry run poe test`

---

Created from [smkent/cookie-python][cookie-python] using
[cookiecutter][cookiecutter]

[codecov]: https://codecov.io/gh/smkent/epoa-tools
[cookie-python]: https://github.com/smkent/cookie-python
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[gh-actions]: https://github.com/smkent/epoa-tools/actions?query=branch%3Amain
[li-complaint-form]: https://www.lni.wa.gov/forms-publications/F700-200-000.pdf
[li-epoa]: https://www.lni.wa.gov/workers-rights/wages/equal-pay-opportunities-act/
[li-file-upload]: https://lni.app.box.com/f/81096b771d1243c0aab00fea150f8c6a
[pipx]: https://pypa.github.io/pipx/
[poetry]: https://python-poetry.org/docs/#installation
[rcw]: https://app.leg.wa.gov/RCW/default.aspx?cite=49.58.110
[repo]: https://github.com/smkent/epoa-tools
