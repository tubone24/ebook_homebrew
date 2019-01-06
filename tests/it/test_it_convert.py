import os
import shutil
import pytest
import logging
import hashlib

from ebook_homebrew.convert import Image2PDF

_logger = logging.getLogger(name=__name__)


class TestItRename(object):

    @staticmethod
    def copy_image_file(directory):
        test_file = os.path.join(os.path.dirname(__file__), "assets", "test_image.png")
        test_file2 = os.path.join(os.path.dirname(__file__), "assets", "test_image2.png")
        for i in range(10):
            shutil.copy2(test_file, directory)
            dst_file_name = os.path.join(directory, str(i).zfill(3) + ".png")
            os.rename(os.path.join(directory, "test_image.png"), dst_file_name)
        shutil.copy2(test_file2, directory)
        dst_ext_file_name = os.path.join(directory, "foo099" + "bar.png")
        os.rename(os.path.join(directory, "test_image2.png"), dst_ext_file_name)
        return True

    @staticmethod
    def interactive_input():
        for out in ["y", "test.png"]:
            yield out

    @pytest.mark.it
    def test_it_make_pdf(self, tmpdir):
        _logger.debug("Temp directory: {tmp_dir}".format(tmp_dir=tmpdir))
        self.copy_image_file(tmpdir)
        target_ins = Image2PDF(directory_path=tmpdir, digits="3", extension="png")
        actual = target_ins.make_pdf("foobar.pdf", remove_flag=True)
        assert actual is True
        md5 = hashlib.md5()
        with open(os.path.join(tmpdir, "foobar.pdf"), "rb") as f:
            for chunk in iter(lambda: f.read(2048 * md5.block_size), b''):
                md5.update(chunk)
        checksum = md5.hexdigest()
        assert checksum == "07809f78db02d9357f6d8b1fdc7d7e4e"
