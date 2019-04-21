"""
Overview:
  Client App with ebook-homebrew's rest API

Usage:
  main.py [-h|--help] [-v|--version]
  main.py upload <directory> <extension> [--host <host>] [--port <port>]
  main.py convert <id> <extension> [--host <host>] [--port <port>]
  main.py download <id> <file> [--host <host>] [--port <port>]

Options:
  upload         : upload
  convert        : convert
  <directory>    : directory
  <extension>    : extension
  <id>           : upload_id
  <file>         : filename
  -h, --help     : show this help message and exit
  -v, --version  : show version
  --host         : API server host
  --port         : API server port
"""

import json
import os
import glob
import base64
import requests
from docopt import docopt

__version__ = "2.0.0"


def main(args):
    """Call submodules"""

    if args["upload"]:
        upload(args)
    elif args["convert"]:
        convert(args)
    elif args["download"]:
        download(args)
    elif args["--version"]:
        show_version()


def upload(args):
    """upload image file"""
    if not args["--host"]:
        host = "http://localhost"
    else:
        host = args["<host>"]
    if not args["--port"]:
        port = 8080
    else:
        port = args["<port>"]
    print("URL: {host}:{port}".format(host=host, port=port))
    url = "{host}:{port}/data/upload".format(host=host, port=port)

    directory = args["<directory>"]
    extension = args["<extension>"]

    content_type = _convert_extension_to_content_type(extension)

    images_b64 = _create_imageb64_list(directory, extension)

    data = json.dumps({"contentType": content_type, "images": images_b64})
    r = requests.post(url, data=data).json()
    upload_id = r["upload_id"]
    print("upload_id: {}".format(upload_id))


def convert(args):
    """convert requests"""

    if not args["--host"]:
        host = "http://localhost"
    else:
        host = args["<host>"]
    if not args["--port"]:
        port = 8080
    else:
        port = args["<port>"]
    upload_id = args["<id>"]
    extension = args["<extension>"]
    print("URL: {host}:{port}".format(host=host, port=port))
    url = "{host}:{port}/convert/pdf".format(host=host, port=port)

    content_type = _convert_extension_to_content_type(extension)

    data = json.dumps({"uploadId": upload_id, "contentType": content_type})
    r = requests.post(url, data=data).json()
    upload_id = r["upload_id"]
    print("upload_id: {}".format(upload_id))


def download(args):
    """download result PDF"""

    if not args["--host"]:
        host = "http://localhost"
    else:
        host = args["<host>"]
    if not args["--port"]:
        port = 8080
    else:
        port = args["<port>"]
    upload_id = args["<id>"]
    file_name = args["<file>"]
    print("URL: {host}:{port}".format(host=host, port=port))
    url = "{host}:{port}/convert/pdf/download".format(host=host, port=port)
    data = json.dumps({"uploadId": upload_id})
    r = requests.post(url, data=data)
    if r.status_code == requests.codes.ok:
        with open(file_name, "wb") as result_file:
            result_file.write(r.content)
    else:
        print("No result file")


def show_version():
    """Show version"""
    print("ebook-homebrew Rest Client: {version}".format(version=__version__))


def _convert_extension_to_content_type(extension):
    if extension == "jpg":
        content_type = "image/jpeg"
    elif extension == "png":
        content_type = "image/png"
    elif extension == "gif":
        content_type = "image/gif"
    else:
        content_type = False
    return content_type


def _create_imageb64_list(directory, extension):
    images_b64 = []
    images = glob.glob(os.path.join(directory, "*." + extension))
    for image in images:
        with open(image, "rb") as image_binary:
            images_b64.append(base64.b64encode(image_binary.read()).decode("utf-8"))

    return images_b64


if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
