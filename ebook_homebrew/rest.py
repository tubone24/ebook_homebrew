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
def status(req, resp):
    resp.media = {"status": "ok"}


@api.route("/data/upload")
async def upload_image_file(req, resp):
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
    for i, content in enumerate(images_b64):
        image = base64.b64decode(content)
        file_name = os.path.join(tmp_dir, str(i) + "." + extension)
        _logger.debug("file_name: {}".format(file_name))
        with open(file_name, "wb") as f:
            f.write(image)
    return True


@api.route("/convert/pdf")
async def convert_image_to_pdf(req, resp):
    data = await req.media()
    _logger.debug(data)
    upload_id = data["uploadId"]
    content_type = data["contentType"]
    result_meta = os.path.join(upload_id, "result_meta.txt")
    if os.path.exists(result_meta):
        os.remove(result_meta)
    extension = convert_content_type_to_extension(content_type)
    file_list = sorted(glob.glob(os.path.join(upload_id, "*." + extension)), reverse=True)
    file_base, _ = os.path.splitext(os.path.basename(file_list[0]))
    digits = len(file_base)
    _logger.debug(file_list)
    convert_pdf(digits, extension, upload_id)
    resp.media = {"upload_id": upload_id}


@api.background.task
def convert_pdf(digits, extension, upload_id):
    converter = Image2PDF(digits=digits, extension=extension, directory_path=upload_id)
    converter.make_pdf("result.pdf")
    with open(os.path.join(upload_id, "result_meta.txt"), "w") as f:
        now = datetime.datetime.now()
        result = {"upload_id": upload_id, "digits": digits, "extension": extension,
                  "datetime": now.strftime("%Y/%m/%d %H:%M:%S")}
        f.write(json.dumps(result))
    return True


@api.route("/convert/pdf/download")
async def download_result_pdf(req, resp):
    data = await req.media()
    _logger.debug(data)
    upload_id = data["uploadId"]
    result_meta = os.path.join(upload_id, "result_meta.txt")
    if os.path.exists(result_meta):
        with open(os.path.join(upload_id, "result.pdf"), "rb") as f:
            resp.headers["Content-Type"] = "application/pdf"
            resp.content = f.read()
    else:
        resp.status_code = api.status_codes.HTTP_404


def convert_content_type_to_extension(content_type):
    if content_type == "image/jpeg":
        return "jpg"
    elif content_type == "image/png":
        return "png"
    elif content_type == "image/gif":
        return "gif"
    else:
        return False


if __name__ == "__main__":
    api.run(port=8080)
