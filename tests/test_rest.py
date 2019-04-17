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
    with open("tests/it/assets/test_image.png", "rb") as f:
        return str(base64.b64encode(f.read()))


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
