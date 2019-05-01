import os
import logging
import base64
import json

import pytest

import ebook_homebrew.rest as target

_logger = logging.getLogger()


@pytest.fixture
def api():
    return target.api


@pytest.fixture
def image_b64():
    with open(os.path.join(os.path.dirname(__file__), "assets", "test_image.png"), "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


@pytest.mark.it
def test_it_rest_convert_pdf(api, image_b64):
    event1 = json.dumps({"fileName": "test.pdf",
                        "contentType": "image/png",
                         "images": [image_b64, image_b64]})
    r1 = api.requests.post("/data/upload", event1)
    assert r1.status_code == 200

    json_response = json.loads(r1.text)
    upload_id = json_response["upload_id"]
    _logger.info("upload_id: {}".format(upload_id))
    event2 = json.dumps({"uploadId": str(upload_id)})
    r2 = api.requests.post("/convert/pdf/download", event2)
    assert r2.status_code == 404

    event3 = json.dumps({"uploadId": str(upload_id),
                        "contentType": "image/png"})
    r3 = api.requests.post("/convert/pdf", event3)
    json_response = json.loads(r3.text)
    assert "upload_id" in json_response
    assert "release_date" in json_response
    assert json_response["upload_id"] == str(upload_id)

    i = 0
    while True:
        event4 = json.dumps({"uploadId": str(upload_id)})
        r4 = api.requests.post("/convert/pdf/download", event4)
        if r4.status_code == 200:
            break
        else:
            _logger.info("404 Response: {}".format(i))
            i += 1
        if i < 10000:
            continue
        else:
            break
    assert r4.status_code == 200

    r5 = api.requests.post("/convert/pdf", event3)
    json_response = json.loads(r5.text)
    assert "upload_id" in json_response
    assert "release_date" in json_response
    assert json_response["upload_id"] == str(upload_id)
    i = 0
    while True:
        event5 = json.dumps({"uploadId": str(upload_id)})
        r5 = api.requests.post("/convert/pdf/download", event5)
        if r5.status_code == 200:
            break
        else:
            _logger.info("404 Response: {}".format(i))
            i += 1
        if i < 10000:
            continue
        else:
            break
    assert r5.status_code == 200
