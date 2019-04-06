import logging
import os
import shutil

import pytest

from ebook_homebrew.helper import auto, make_zip
from ebook_homebrew.exceptions import BaseError

_logger = logging.getLogger(name=__name__)


class ArgNameSpace(object):
    def __init__(self):
        self.src_dir = []
        self.dst_dir = []
        self.digit = []
        self.extension = []
        self.filename = []
        self.manual = False
        self.assume_yes = False
        self.remove = False


def copy_image_file(directory):
    test_file = os.path.join(os.path.dirname(__file__), "assets", "test_image.png")
    test_file2 = os.path.join(os.path.dirname(__file__), "assets", "test_image2.png")
    test_file3 = os.path.join(os.path.dirname(__file__), "assets", "test_text.txt")
    for i in range(10):
        shutil.copy2(test_file, directory)
        dst_file_name = os.path.join(directory, str(i).zfill(3) + ".png")
        os.rename(os.path.join(directory, "test_image.png"), dst_file_name)
    shutil.copy2(test_file2, directory)
    dst_ext_file_name = os.path.join(directory, "foo099" + "bar.png")
    os.rename(os.path.join(directory, "test_image2.png"), dst_ext_file_name)
    shutil.copy2(test_file3, directory)
    dst_ext_file_name = os.path.join(directory, "foo001" + "bar.txt")
    os.rename(os.path.join(directory, "test_text.txt"), dst_ext_file_name)
    os.mkdir(os.path.join(directory, "destination"))
    return True


@pytest.fixture
def args_ok_auto(tmpdir):
    _logger.debug("Temp directory: {tmp_dir}".format(tmp_dir=str(tmpdir)))
    copy_image_file(str(tmpdir))
    args_obj = ArgNameSpace()
    args_obj.src_dir.append(str(tmpdir))
    args_obj.dst_dir.append(os.path.join(str(tmpdir), "destination"))
    args_obj.digit.append("3")
    args_obj.extension.append("png")
    args_obj.filename.append("test.pdf")
    args_obj.manual = True
    args_obj.assume_yes = True
    args_obj.remove = True
    return args_obj


@pytest.mark.it
def test_ok_auto(args_ok_auto):
    auto(args_ok_auto)


@pytest.fixture
def args_ok_make_zip(tmpdir):
    _logger.debug("Temp directory: {tmp_dir}".format(tmp_dir=str(tmpdir)))
    copy_image_file(str(tmpdir))
    args_obj = ArgNameSpace()
    args_obj.src_dir.append(str(tmpdir))
    args_obj.dst_dir.append(os.path.join(str(tmpdir), "destination"))
    args_obj.extension.append("png")
    args_obj.filename.append("test.zip")
    args_obj.assume_yes = True
    args_obj.remove = True
    return args_obj


@pytest.mark.it
def test_ok_make_zip(args_ok_make_zip):
    make_zip(args_ok_make_zip)


@pytest.fixture
def args_no_support_file_auto(tmpdir):
    _logger.debug("Temp directory: {tmp_dir}".format(tmp_dir=str(tmpdir)))
    copy_image_file(str(tmpdir))
    args_obj = ArgNameSpace()
    args_obj.src_dir.append(str(tmpdir))
    args_obj.dst_dir.append(os.path.join(str(tmpdir), "destination"))
    args_obj.digit.append("3")
    args_obj.extension.append("txt")
    args_obj.filename.append("test.pdf")
    args_obj.manual = True
    args_obj.assume_yes = True
    args_obj.remove = True
    return args_obj


@pytest.mark.it
def test_base_error_auto(args_no_support_file_auto):
    with pytest.raises(BaseError):
        auto(args_no_support_file_auto)


@pytest.fixture
def args_no_support_file_make_zip(tmpdir):
    _logger.debug("Temp directory: {tmp_dir}".format(tmp_dir=str(tmpdir)))
    copy_image_file(str(tmpdir))
    args_obj = ArgNameSpace()
    args_obj.src_dir.append(str(tmpdir))
    args_obj.dst_dir.append(os.path.join(str(tmpdir), "destination"))
    args_obj.extension.append("png")
    args_obj.filename.append("foo001bar.txt")
    args_obj.manual = True
    args_obj.assume_yes = False
    args_obj.remove = True
    return args_obj


@pytest.mark.it
def test_base_error_make_zip(args_no_support_file_make_zip):
    with pytest.raises(BaseError):
        make_zip(args_no_support_file_make_zip)


@pytest.fixture
def args_unhandled(tmpdir):
    _logger.debug("Temp directory: {tmp_dir}".format(tmp_dir=str(tmpdir)))
    copy_image_file(str(tmpdir))
    args_obj = ArgNameSpace()
    return args_obj


@pytest.mark.it
def test_unhandled_error_auto(args_unhandled):
    with pytest.raises(Exception):
        auto(args_unhandled)


@pytest.mark.it
def test_unhandled_error_make_zip(args_unhandled):
    with pytest.raises(Exception):
        make_zip(args_unhandled)
