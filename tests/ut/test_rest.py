import os
import shutil
import logging
import base64
import json
from unittest.mock import patch
from unittest.mock import MagicMock

import pytest

import ebook_homebrew.rest as target


@pytest.fixture
def api():
    return target.api


@pytest.fixture
def image_b64():
    with open(os.path.join(os.path.dirname(__file__), "assets", "test_image.png"), "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def copy_image_file(directory):
    test_file = os.path.join(os.path.dirname(__file__), "assets", "test_image.png")
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
    json_response = json.loads(r.text)
    assert "status" in json_response
    actual = json_response["status"]
    expect = "ok"
    assert actual == expect


def test_list_upload_files(api):
    file_list = {"id": 1,
                 "name": "test",
                 "file_path": "/tmp/test",
                 "file_type": "image/png",
                 "last_index": 0,
                 "created_at": "2019-07-28 16:21:14",
                 "updated_at": "2019-07-28 16:21:14"}
    mock_uploadedfile = MagicMock()
    mock_get_all_uploaded_file = MagicMock(return_value=[file_list])
    mock_uploadedfile.get_all_uploaded_file = mock_get_all_uploaded_file
    with patch.object(target, "UploadedFile", return_value=mock_uploadedfile):
        r = api.requests.get("/data/upload/list")
        json_response = json.loads(r.text)
        assert "fileList" in json_response
        actual = json_response["fileList"]
        expect = [file_list]
        assert actual == expect


def test_upload_image_file(api, image_b64, tmpdir):
    event = json.dumps({"fileName": "test.pdf",
                        "contentType": "image/png",
                        "images": [image_b64]})
    with patch.object(target, "write_image", return_value=True) as mock_write_image, \
            patch("tempfile.mkdtemp", return_value=str(tmpdir)) as mock_mkdtemp:
        r = api.requests.post("/data/upload", event)
        assert r.status_code == 200
        json_response = json.loads(r.text)
        assert "upload_id" in json_response
        assert "release_date" in json_response
        assert json_response["upload_id"] == str(tmpdir)
        mock_write_image.assert_called_once_with([image_b64], "image/png", str(tmpdir))
        mock_mkdtemp.assert_called_once_with()


def test_upload_image_file_data_uri_schema(api, image_b64, tmpdir):
    event = json.dumps({"fileName": "test.pdf",
                        "contentType": "image/png",
                        "images": ["data:image/png;base64," + image_b64]})
    with patch.object(target, "write_image", return_value=True) as mock_write_image, \
            patch("tempfile.mkdtemp", return_value=str(tmpdir)) as mock_mkdtemp:
        r = api.requests.post("/data/upload", event)
        assert r.status_code == 200
        json_response = json.loads(r.text)
        assert "upload_id" in json_response
        assert "release_date" in json_response
        assert json_response["upload_id"] == str(tmpdir)
        mock_write_image.assert_called_once_with(["data:image/png;base64," + image_b64], "image/png", str(tmpdir))
        mock_mkdtemp.assert_called_once_with()


def test_write_image(image_b64, tmpdir):
    mock_uploadedfile = MagicMock()
    mock_add_uploaded_file = MagicMock()
    mock_uploadedfile.add_uploaded_file = mock_add_uploaded_file
    file_name = os.path.join(tmpdir, "0.png")
    with patch.object(target, "UploadedFile", return_value=mock_uploadedfile):
        future = target.write_image([image_b64], "image/png", tmpdir)
        actual = future.result()
        expected = True
        assert actual == expected
        mock_add_uploaded_file.assert_called_once_with(name=file_name,
                                                       file_path=str(tmpdir),
                                                       file_type="image/png",
                                                       last_index=0)


def test_write_image_data_uri_schema(image_b64, tmpdir):
    future = target.write_image(["data:image/png;base64," + image_b64], "image/png", tmpdir)
    actual = future.result()
    expected = True
    assert actual == expected


@pytest.mark.parametrize("event, expected", [
    ({"fileName": "test.pdf", "contentType": "image/png"}, "{'images': ['Missing data for required field.']}"),
    ({"fileName": "test.pdf", "images": ["test"]}, "{'contentType': ['Missing data for required field.']}"),
    ({"contentType": "image/png", "images": "test"}, "{'images': ['Not a valid list.']}")])
def test_validation_error_upload_image_file(api, event, expected):
    r = api.requests.post("/data/upload", json.dumps(event))
    assert r.status_code == 400
    json_response = json.loads(r.text)
    assert "error" in json_response
    assert "errorDate" in json_response
    actual = json_response["error"]
    assert actual == expected


def test_convert_image_to_pdf(api, tmpdir):
    copy_image_file(str(tmpdir))
    event = json.dumps({"uploadId": str(tmpdir),
                        "contentType": "image/png"})
    r = api.requests.post("/convert/pdf", event)
    json_response = json.loads(r.text)
    assert "upload_id" in json_response
    assert "release_date" in json_response
    assert json_response["upload_id"] == str(tmpdir)
    r = api.requests.post("/convert/pdf", event)
    json_response = json.loads(r.text)
    assert "upload_id" in json_response
    assert "release_date" in json_response
    assert json_response["upload_id"] == str(tmpdir)


@pytest.mark.parametrize("event, expected", [
    ({"contentType": "image/png"}, "{'uploadId': ['Missing data for required field.']}"),
    ({"uploadId": "test"}, "{'contentType': ['Missing data for required field.']}")])
def test_validation_error_convert_image_to_pdf(api, event, expected):
    r = api.requests.post("/convert/pdf", json.dumps(event))
    assert r.status_code == 400
    json_response = json.loads(r.text)
    assert "error" in json_response
    assert "errorDate" in json_response
    actual = json_response["error"]
    assert actual == expected


@pytest.mark.parametrize("event, expected", [
    ({"contentType": "image/png", "uploadId": "test"}, "upload_id is NotFound")])
def test_not_found_upload_id_convert_image_to_pdf(api, event, expected):
    r = api.requests.post("/convert/pdf", json.dumps(event))
    assert r.status_code == 404
    json_response = json.loads(r.text)
    assert "reason" in json_response
    assert "errorDate" in json_response
    actual = json_response["reason"]
    assert actual == expected


@pytest.mark.parametrize("event, expected", [
    ({"contentType": "image/png"}, "{'uploadId': ['Missing data for required field.']}")])
def test_validation_error_download_result_pdf(api, event, expected):
    r = api.requests.post("/convert/pdf/download", json.dumps(event))
    assert r.status_code == 400
    json_response = json.loads(r.text)
    assert "error" in json_response
    assert "errorDate" in json_response
    actual = json_response["error"]
    assert actual == expected


@pytest.mark.parametrize("event, expected", [
    ({"uploadId": "test"}, "resultFile NotFound")])
def test_not_found_upload_id_download_result_pdf(api, event, expected):
    r = api.requests.post("/convert/pdf/download", json.dumps(event))
    assert r.status_code == 404
    json_response = json.loads(r.text)
    assert "reason" in json_response
    assert "errorDate" in json_response
    actual = json_response["reason"]
    assert actual == expected


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
