# -*- coding: utf-8 -*-
"""Provides Rest API interfaces
"""

import os
import base64
import glob
import json
import datetime
import tempfile
import responder

from .convert import Image2PDF
from .utils.logging import get_logger

api = responder.API()

_logger = get_logger("RestAPI")


@api.route("/status")
def status(_, resp):
    """Health Check
    """
    _logger.debug("health Check")
    resp.media = {"status": "ok"}


@api.route("/data/upload")
async def upload_image_file(req, resp):
    """Endpoint: File uploader
    """
    data = await req.media()
    _logger.debug(data)
    content_type = data["contentType"]
    extension = convert_content_type_to_extension(content_type)
    images_b64 = data["images"]
    tmp_dir = tempfile.mkdtemp()
    write_image(images_b64, extension, tmp_dir)
    resp.media = {"upload_id": tmp_dir}


@api.background.task
def write_image(images_b64, extension, tmp_dir):
    """Images write at tmp_dir

    This API is background task.

    Args:
     images_b64: Base64 encoded images list
     extension: Image extension
     tmp_dir: Temp directory writing images
    Returns:
        bool: If success return true.

    """
    for i, content in enumerate(images_b64):
        image = base64.b64decode(content)
        file_name = os.path.join(tmp_dir, str(i) + "." + extension)
        _logger.debug("file_name: {}".format(file_name))
        with open(file_name, "wb") as image_file:
            image_file.write(image)
    return True


@api.route("/convert/pdf")
async def convert_image_to_pdf(req, resp):
    """Endpoint Image converter to PDF
    """
    data = await req.media()
    _logger.debug(data)
    upload_id = data["uploadId"]
    content_type = data["contentType"]
    result_meta = os.path.join(upload_id, "result_meta.txt")
    if os.path.exists(result_meta):
        os.remove(result_meta)
    extension = convert_content_type_to_extension(content_type)
    file_list = sorted(
        glob.glob(os.path.join(upload_id, "*." + extension)), reverse=True
    )
    file_base, _ = os.path.splitext(os.path.basename(file_list[0]))
    digits = len(file_base)
    _logger.debug(file_list)
    convert_pdf(digits, extension, upload_id)
    resp.media = {"upload_id": upload_id}


@api.background.task
def convert_pdf(digits, extension, upload_id):
    """Convert images to PDF

    This API is background task.

    Args:
     digits: file serial number digits
     extension: Image extension
     upload_id: Request ID
    Returns:
        bool: If success return true.

    """
    converter = Image2PDF(digits=digits, extension=extension, directory_path=upload_id)
    converter.make_pdf("result.pdf")
    with open(os.path.join(upload_id, "result_meta.txt"), "w") as result_txt:
        now = datetime.datetime.now()
        result = {
            "upload_id": upload_id,
            "digits": digits,
            "extension": extension,
            "datetime": now.strftime("%Y/%m/%d %H:%M:%S"),
        }
        result_txt.write(json.dumps(result))
    return True


@api.route("/convert/pdf/download")
async def download_result_pdf(req, resp):
    """Endpoint download result PDF
    """
    data = await req.media()
    _logger.debug(data)
    upload_id = data["uploadId"]
    result_meta = os.path.join(upload_id, "result_meta.txt")
    if os.path.exists(result_meta):
        with open(os.path.join(upload_id, "result.pdf"), "rb") as result_pdf:
            resp.headers["Content-Type"] = "application/pdf"
            resp.content = result_pdf.read()
    else:
        resp.status_code = api.status_codes.HTTP_404


def convert_content_type_to_extension(content_type):
    """Convert image extension to Content-Type

    Args:
     content_type: Content-Type
    Returns:
        str: extension

    """
    if content_type == "image/jpeg":
        extension = "jpg"
    elif content_type == "image/png":
        extension = "png"
    elif content_type == "image/gif":
        extension = "gif"
    else:
        extension = False

    return extension
