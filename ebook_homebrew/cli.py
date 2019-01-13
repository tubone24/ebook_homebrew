# -*- coding: utf-8 -*-
import argparse

from ebook_homebrew.helper import auto


def execute_auto(args_auto):
    auto(args_auto)


def main():
    parser = argparse.ArgumentParser(
        prog="ebook_homebrew",
        usage="ebookhomebrew",
        description="You can make e-books for some image files",
        epilog="More information? Access here: https://github.com/tubone24/ebook_homebrew",
        add_help=True,
    )

    subparsers = parser.add_subparsers(description="Choose subcommands. Usually choose \"auto\"")

    parser_auto = subparsers.add_parser("auto",
                                        description="Make only digit file name, "
                                                    "convert e-book file such as PDF",
                                        help="Make only digit file name, "
                                             "convert e-book file such as PDF")

    parser_auto.set_defaults(handler=execute_auto)

    parser_auto.add_argument("-s", "--src_dir",
                             action="store",
                             nargs=1,
                             const=None,
                             default=None,
                             required=True,
                             type=str,
                             help="Source directory which put original image files.",
                             metavar="SRC_DIR")

    parser_auto.add_argument("--dst_dir",
                             action="store",
                             nargs=1,
                             const=None,
                             default=None,
                             type=str,
                             help="Destination directory which put e-book file.",
                             metavar="DST_DIR")

    parser_auto.add_argument("-d", "--digit",
                             action="store",
                             nargs=1,
                             const=None,
                             default=None,
                             required=True,
                             type=str,
                             help="Serial number digits you remain file name",
                             metavar="N,N")

    parser_auto.add_argument("-e", "--extension",
                             action="store",
                             nargs=1,
                             const=None,
                             default=None,
                             required=True,
                             type=str,
                             help="Destination directory which put e-book file.",
                             metavar="EXT")

    parser_auto.add_argument("-f", "--filename",
                             action="store",
                             nargs=1,
                             const=None,
                             default=None,
                             required=True,
                             type=str,
                             help="Destination directory which put e-book file.",
                             metavar="FILENAME")

    parser_auto.add_argument("-m", "--manual",
                             action="store_true",
                             help="Duplicate file name, solving manually.")

    parser_auto.add_argument("-r", "--remove",
                             action="store_true",
                             help="Remove original image file.")

    parser_auto.add_argument("-y", "--assume_yes",
                             action="store_true",
                             help="no verify users.")

    args = parser.parse_args()

    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
