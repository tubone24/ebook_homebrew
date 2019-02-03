![ebook_homebrew](https://raw.githubusercontent.com/tubone24/ebook_homebrew/master/doc_src/bookicon.png
 "ebook_homebrew_icon")


# ebook_homebrew

[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Build Status](https://travis-ci.org/tubone24/ebook_homebrew.svg?branch=master)](https://travis-ci.org/tubone24/ebook_homebrew)
[![Documentation Status](https://readthedocs.org/projects/ebook-homebrew/badge/?version=latest)](https://ebook-homebrew.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/tubone24/ebook_homebrew/branch/master/graph/badge.svg)](https://codecov.io/gh/tubone24/ebook_homebrew)
[![Maintainability](https://api.codeclimate.com/v1/badges/a3e2d70a87998a18e225/maintainability)](https://codeclimate.com/github/tubone24/ebook_homebrew/maintainability)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/tubone24/ebook_homebrew/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/tubone24/ebook_homebrew/?branch=master)
[![Code Intelligence Status](https://scrutinizer-ci.com/g/tubone24/ebook_homebrew/badges/code-intelligence.svg?b=master)](https://scrutinizer-ci.com/code-intelligence)
![Downloads](https://img.shields.io/pypi/dm/ebook-homebrew.svg)
![PyPi](https://img.shields.io/pypi/v/ebook-homebrew.svg)
![Python version](https://img.shields.io/pypi/pyversions/ebook-homebrew.svg)
[![format](https://img.shields.io/pypi/format/ebook-homebrew.svg)](https://pypi.org/project/ebook-homebrew/)
![Gitter](https://img.shields.io/gitter/room/tubone24/ebook_homebrew.svg)

Change file name to only digit name like `001.jpg` and make e-book format files.

## Getting Started

Ebook_homebrew is a python package, so that you can use `setup.py` or `pip` installer.

### Using setup.py

```bash
$ python setup.py install
```

### Or using pip installer


```bash
$ pip install ebook-homebrew
```

## Usage

You can use global command "ebookhomebrew".

Show help.

```bash
$ ebookhomebrew -h
```

Ex) Rename image file to only digit and Create PDF file.

```bash
$ ebookhomebrew auto -s ./tests -d 3,4 -e jpg -f test.pdf
```

### ebookhomebrew command line interface

#### Subcommands

```bash
  Choose subcommands. Usually choose "auto"

  {auto}
    auto      Make only digit file name, convert e-book file such as PDF
```
  
#### Options

```bash
  -h, --help            show this help message and exit
  -s SRC_DIR, --src_dir SRC_DIR
                        Source directory which put original image files.
  --dst_dir DST_DIR     Destination directory which put e-book file.
  -d N,N, --digit N,N   Serial number digits you remain file name
  -e EXT, --extension EXT
                        Destination directory which put e-book file.
  -f FILENAME, --filename FILENAME
                        Destination directory which put e-book file.
  -m, --manual          Duplicate file name, solving manually.
  -r, --remove          Remove original image file.
  -y, --assume_yes      no verify users.
```

## Testing

### Unit Test

Using pytest, if you want to test.

```bash
pytest
```

If you get coverage report, run coverage and report.

```bash
$ coverage run --source=ebook_homebrew -m pytest
$ coverage report -m
```

Or pytest-cov param for pytest

```bash
$ pytest --cov=ebook_homebrew --cov-report html --cov-report xml
```

### Integration Test

Using pytest, if you want to test with mark "--it"

```bash
pytest --it
```

### With tox

With tox, you can test multiple python version.(only python3.5, 3.6)

```bash
tox
```

### Travis-CI

This repository uses [Travis-CI](https://travis-ci.org/) and be building jobs by push or PR branches.

## Licence

This software is released under the MIT License, see LICENSE.

## API Document

See `Read the Docs`

[document](https://ebook-homebrew.readthedocs.io/en/latest/)