# -*- coding: utf-8 -*-
"""Provides helper for command line interface
"""

import sys

from .convert import Image2PDF
from .exceptions import BaseError
from .rename import ChangeFilename
from .utils.logging import get_logger

# from archive import MakeArchive

logger = get_logger("helper")


def auto(args):
    try:
        rename = ChangeFilename(directory_path=args.src_dir[0],
                                digits=args.digit[0],
                                extension=args.extension[0])
        rename.filename_to_digit_number()
        if args.manual is True:
            rename.change_name_manually(overwrite=args.assume_yes)

        convert = Image2PDF(digits=args.digit[0], extension=args.extension[0])
        convert.make_pdf(filename=args.filename[0], remove_flag=args.remove)

        if args.dst_dir is not None:
            convert.move_file(file=args.filename[0], dst=args.dst_dir[0], assume_yes=args.assume_yes)
    except BaseError as e:
        logger.exception(e)
        sys.exit(2)
    except Exception as e:
        logger.error("Unhandled Error occurred.")
        logger.exception(e)
        logger.critical(e)
        sys.exit(1)
