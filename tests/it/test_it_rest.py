import os
import shutil
import logging
import base64
import json
from time import sleep

import pytest

import ebook_homebrew.rest as target

_logger = logging.getLogger()

@pytest.fixture
def api():
    return target.api


@pytest.fixture
def image_b64():
    with open(os.path.join(os.path.dirname(__file__), "assets", "test_image3.png"), "rb") as f:
        return str(base64.b64encode(f.read()))


@pytest.mark.it
def test_it_rest_convert_pdf(api, image_b64):
    event1 = json.dumps({"fileName": "test.pdf",
                        "contentType": "image/png",
                         "images": [image_b64]})
    r1 = api.requests.post("/data/upload", event1)
    assert r1.status_code == 200
    json_response = json.loads(r1.text)
    upload_id = json_response["upload_id"]
    _logger.info(upload_id)
    event2 = json.dumps({"uploadId": str(upload_id)})
    r2 = api.requests.post("/convert/pdf/download", event2)
    assert r2.status_code == 404
    event3 = json.dumps({"uploadId": str(upload_id),
                        "contentType": "image/png"})
    r3 = api.requests.post("/convert/pdf", event3)
    assert r3.text == json.dumps({"upload_id": str(upload_id)})
    r3 = api.requests.post("/convert/pdf", event3)
    assert r3.text == json.dumps({"upload_id": str(upload_id)})
