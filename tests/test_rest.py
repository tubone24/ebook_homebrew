import os
import shutil
import logging
import base64
import json
from unittest.mock import patch

import pytest

import ebook_homebrew.rest as target


@pytest.fixture
def api():
    return target.api


@pytest.fixture
def image_b64():
    with open(os.path.join(os.path.dirname(__file__), "it", "assets", "test_image.png"), "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def copy_image_file(directory):
    test_file = os.path.join(os.path.dirname(__file__), "it", "assets", "test_image.png")
    for i in range(100):
        shutil.copy2(test_file, directory)
        dst_file_name = os.path.join(directory, "foo" + str(i).zfill(3) + "bar.png")
        os.rename(os.path.join(directory, "test_image.png"), dst_file_name)
    shutil.copy2(test_file, directory)
    dst_ext_file_name = os.path.join(directory, "foofoo001" + "b_bar.png")
    os.rename(os.path.join(directory, "test_image.png"), dst_ext_file_name)
    return True


def test_indexhtml(api):
    r = api.requests.get("/")
    assert r.status_code == 200


def test_status(api):
    r = api.requests.get("/status")
    expect = json.dumps({"status": "ok"})
    assert r.text == expect


def test_upload_image_file(api, image_b64, tmpdir):
    event = json.dumps({"fileName": "test.pdf",
                        "contentType": "image/png",
                        "images": [image_b64]})
    with patch.object(target, "write_image", return_value=True) as mock_write_image, \
            patch("tempfile.mkdtemp", return_value=str(tmpdir)) as mock_mkdtemp:
        r = api.requests.post("/data/upload", event)
        assert r.status_code == 200
        assert r.text == json.dumps({"upload_id": str(tmpdir)})
        mock_write_image.assert_called_once_with([image_b64], "png", str(tmpdir))
        mock_mkdtemp.assert_called_once_with()


def test_convert_image_to_pdf(api, tmpdir):
    copy_image_file(str(tmpdir))
    event = json.dumps({"uploadId": str(tmpdir),
                        "contentType": "image/png"})
    r = api.requests.post("/convert/pdf", event)
    assert r.text == json.dumps({"upload_id": str(tmpdir)})
    r = api.requests.post("/convert/pdf", event)
    assert r.text == json.dumps({"upload_id": str(tmpdir)})


@pytest.mark.parametrize("input_param, expected", [
    ("image/jpeg", "jpg"),
    ("image/png", "png"),
    ("image/gif", "gif"),
    ("application/pdf", False)])
def test_convert_content_type_to_extension(input_param, expected):
    actual = target.convert_content_type_to_extension(input_param)
    assert actual == expected


def test_openapi_schema(api):
    with open(os.path.join(os.path.dirname(__file__), "assets", "schema.yml"), "r") as schema_yml:
        expected = schema_yml.read()
    r = api.session().get("http://;/schema.yml")
    actual = r.text

    assert actual == expected
