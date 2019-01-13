"""Example import modules and use ebook_homebrew
"""

from ebook_homebrew.convert import Image2PDF
from ebook_homebrew.rename import ChangeFilename


def main():
    """Example import modules and use ebook_homebrew
    """
    rename = ChangeFilename(directory_path="example_file",
                            digits="3",
                            extension="png")

    rename.filename_to_digit_number()

    convert = Image2PDF(digits="3", extension="png")
    convert.make_pdf(filename="examples.pdf")


if __name__ == '__main__':
    main()
