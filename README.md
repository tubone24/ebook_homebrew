![ebook_homebrew](https://raw.githubusercontent.com/tubone24/ebook_homebrew/master/doc_src/bookicon.png
 "ebook_homebrew_icon")


# ebook_homebrew
Change file name to only digit name like `001.jpg` and make e-book format files.

# Getting Started
Ebook_homebrew is a python package, so that you can use `setup.py` or `pip` installer.

## Using setup.py
```bash
$ python setup.py install
```

## Or using pip installer
Unimplemented
```bash
$ pip install ebook_homebrew
```

# Usage
You can use global command "ebookhomebrew".

Show help.
```bash
$ ebookhomebrew -h
```

Ex) Rename image file to only digit and Create PDF file.

```bash
$ ebookhomebrew auto -s ./tests -d 3,4 -e jpg -f test.pdf
```

## ebookhomebrew command line interface

### Subcommands

```bash
  Choose subcommands. Usually choose "auto"

  {auto}
    auto      Make only digit file name, convert e-book file such as PDF
```
  
### Options
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

# Licence
This software is released under the MIT License, see LICENSE.