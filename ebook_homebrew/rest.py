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
from marshmallow import Schema, fields, ValidationError

from .convert import Image2PDF
from .utils.logging import get_logger
from .models.models import UploadModel, ErrorModel, FileNotFoundModel, StatusModel
from .__init__ import __version__

api = responder.API(
    title="Ebook-homebrew",
    debug=True,
    cors=True,
    cors_params={
        "allow_origins": ["*"],
        "allow_methods": ["GET", "POST"],
        "allow_headers": ["*"],
    },
    version=__version__,
    static_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
    static_route="/static",
    openapi="3.0.2",
    docs_route="/docs",
    openapi_route="/schema.yml",
    description="Make PDF file taken in "
    "some image files such as "
    "jpeg, png and gif.",
    contact={
        "name": "tubone24",
        "url": "https://tubone-project24.xyz",
        "email": "tubo.yyyuuu@gmail.com",
    },
    license={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)

_logger = get_logger("RestAPI")


@api.schema("HealthCheck")
class HealthCheckSchema(Schema):
    status = fields.Str()
    version = fields.Str()


@api.schema("UploadImagesReq")
class UploadImagesReqSchema(Schema):
    contentType = fields.Str(required=True)
    images = fields.List(fields.Str(required=True), required=True)


@api.schema("UploadIdResp")
class UploadIdRespSchema(Schema):
    upload_id = fields.Str()
    release_date = fields.Date()


@api.schema("ConvertReq")
class ConvertReqSchema(Schema):
    uploadId = fields.Str(required=True)
    contentType = fields.Str(required=True)


@api.schema("DownloadReq")
class DownloadReqSchema(Schema):
    uploadId = fields.Str(required=True)


@api.schema("ErrorResp")
class ErrorRespSchema(Schema):
    error = fields.Str()
    errorDate = fields.Date()


@api.schema("FileNotFoundResp")
class FileNotFoundRespSchema(Schema):
    reason = fields.Str()
    errorDate = fields.Date()


api.add_route("/", static=True)


@api.route("/status")
def status(_, resp):
    """Health Check Response.
    ---
    get:
        description: Get Status
        responses:
            "200":
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/HealthCheck"
    """
    _logger.debug("health Check")
    resp.media = HealthCheckSchema().dump(StatusModel("ok", __version__)).data


@api.route("/data/upload")
async def upload_image_file(req, resp):
    """Upload Image files.
    ---
    post:
        summary: Base64 encoded Images

        requestBody:
            description: base64 encoded Images in images Array
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/UploadImagesReq"
        responses:
            "200":
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/UploadIdResp"
            "400":
                description: BadRequest
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/ErrorResp"
    """
    request = await req.media()
    try:
        data = UploadImagesReqSchema(strict=True).load(request).data
    except ValidationError as error:
        resp.status_code = api.status_codes.HTTP_400
        resp.media = ErrorRespSchema().dump(ErrorModel(error)).data
        return
    _logger.debug(data)
    content_type = data["contentType"]
    extension = convert_content_type_to_extension(content_type)
    images_b64 = data["images"]
    tmp_dir = tempfile.mkdtemp()
    write_image(images_b64, extension, tmp_dir)
    resp.media = UploadIdRespSchema().dump(UploadModel(tmp_dir)).data


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
        image = base64.b64decode(content.split(",")[-1])
        file_name = os.path.join(tmp_dir, str(i) + "." + extension)
        _logger.debug("file_name: {}".format(file_name))
        with open(file_name, "wb") as image_file:
            image_file.write(image)
    return True


@api.route("/convert/pdf")
async def convert_image_to_pdf(req, resp):
    """Convert Image files to PDF.
    ---
    post:
        summary: Upload Id witch get upload images and ContentType

        requestBody:
            description: Upload Id and ContentType
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/ConvertReq"
        responses:
            "200":
                description: OK
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/UploadIdResp"
            "400":
                description: BadRequest
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/ErrorResp"
            "404":
                description: UploadIdNotFound
                content:
                    application/json:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/FileNotFoundResp"
    """
    request = await req.media()
    try:
        data = ConvertReqSchema(strict=True).load(request).data
    except ValidationError as error:
        resp.status_code = api.status_codes.HTTP_400
        resp.media = ErrorRespSchema().dump(ErrorModel(error)).data
        return
    _logger.debug(data)
    upload_id = data["uploadId"]
    content_type = data["contentType"]
    if not os.path.isdir(upload_id):
        resp.status_code = api.status_codes.HTTP_404
        resp.media = (
            FileNotFoundRespSchema()
            .dump(FileNotFoundModel("upload_id is NotFound"))
            .data
        )
        return
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
    resp.media = UploadIdRespSchema().dump(UploadModel(upload_id)).data


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
    """Upload Image files.
    ---
    post:
        summary: Upload Id witch get upload images

        requestBody:
            description: Upload Id
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/DownloadReq"
        responses:
            "200":
                description: OK
                content:
                    application/pdf:
                        schema:
                            type: string
                            format: binary
            "400":
                description: BadRequest
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/ErrorResp"
            "404":
                description: ResultFileNotFound
                content:
                    application/json:
                        schema:
                            $ref: "#/components/schemas/FileNotFoundResp"
    """
    request = await req.media()
    try:
        data = DownloadReqSchema(strict=True).load(request).data
    except ValidationError as error:
        resp.status_code = api.status_codes.HTTP_400
        resp.media = ErrorRespSchema().dump(ErrorModel(error)).data
        return
    upload_id = data["uploadId"]
    result_meta = os.path.join(upload_id, "result_meta.txt")
    if os.path.exists(result_meta):
        with open(os.path.join(upload_id, "result.pdf"), "rb") as result_pdf:
            resp.headers["Content-Type"] = "application/pdf"
            resp.content = result_pdf.read()
    else:
        resp.status_code = api.status_codes.HTTP_404
        resp.media = (
            FileNotFoundRespSchema().dump(FileNotFoundModel("resultFile NotFound")).data
        )


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
