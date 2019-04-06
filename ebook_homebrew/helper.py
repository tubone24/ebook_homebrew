# -*- coding: utf-8 -*-
"""Provides helper for command line interface
"""

from .__init__ import __version__
from .convert import Image2PDF
from .exceptions import BaseError
from .rename import ChangeFilename
from .utils.logging import get_logger
from .archive import MakeArchive

_logger = get_logger("helper")


def auto(args):
    """ Rename file, convert pdf.

    Args:
        args: argparse namespace object

    Returns:
        bool: If success, return true.
    """
    try:
        rename_obj = ChangeFilename(
            directory_path=args.src_dir[0],
            digits=args.digit[0],
            extension=args.extension[0],
        )
        rename_obj.filename_to_digit_number()
        if args.manual is True:
            rename_obj.change_name_manually(overwrite=args.assume_yes)

        convert_obj = Image2PDF(digits=args.digit[0], extension=args.extension[0])
        convert_obj.make_pdf(filename=args.filename[0], remove_flag=args.remove)

        if args.dst_dir is not None:
            convert_obj.move_file(
                file=args.filename[0], dst=args.dst_dir[0], assume_yes=args.assume_yes
            )
        return True
    except BaseError as base_error:
        _logger.exception(base_error)
        raise base_error
    except Exception as other_error:
        _logger.error("Unhandled Error occurred.")
        _logger.exception(other_error)
        _logger.critical(other_error)
        raise other_error


def make_zip(args):
    """Make zip file

    Args:
        args: argparse namespace object

    Returns:
        bool: If success, return true.
    """
    try:
        make_zip_obj = MakeArchive(
            extension=args.extension[0], directory_path=args.src_dir[0]
        )
        make_zip_obj.make_zip(
            filename=args.filename[0], remove_flag=args.remove, overwrite=False
        )
        if args.dst_dir is not None:
            make_zip_obj.move_file(
                file=args.filename[0], dst=args.dst_dir[0], assume_yes=args.assume_yes
            )
        return True
    except BaseError as base_error:
        _logger.exception(base_error)
        raise base_error
    except Exception as other_error:
        _logger.error("Unhandled Error occurred.")
        _logger.exception(other_error)
        _logger.critical(other_error)
        raise other_error


def show_version():
    """Show version
    """
    print("ebook_homebrew: {version}".format(version=__version__))
