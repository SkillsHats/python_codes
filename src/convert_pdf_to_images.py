import argparse
import os
import sys
import tempfile
from pathlib import Path
from typing import List
from pdf2image import convert_from_path
from pdf2image import exceptions

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)


# USAGE
"""
# python convert_pdf_to_images.py -i myfile.pdf
# python convert_pdf_to_images.py -i myfile.pdf -o output
"""


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] ...",
        description="Convert PDF file into image(s)."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-i', '--input', type=argparse.FileType('r'), help='Input PDF file', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output path', required=False, default='images')
    return parser


def convert_pdf_to_image(target_file: str, output_folder: str) -> List[str]:
    """ Convert PDF File into the images.
    Parameter:
        target_file: str
            File should be PDF format.
        output_folder: str
            Output folder where output images would be save.
    
    Return:
        List of images url.
    """

    output_images = list()

    try:
        with tempfile.TemporaryDirectory() as path:
            images = convert_from_path(target_file, output_folder=path)
    except PDFInfoNotInstalledError as e:
        print(e)
    except PDFPageCountError as e:
        print(e)
    except PDFSyntaxError as e:
        print(e)
    except Exception as e:
        raise Exception(e)

    # Create Output Folder if does not exists or skip
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Make a base output file name
    base_filename  =  os.path.splitext(os.path.basename(target_file))[0]

    # Iterate the pages
    for i, page in enumerate(images):
        fname = f"{base_filename}_{str(i)}.jpg"
        image_path = os.path.join(output_folder, fname)
        page.save(image_path, 'JPEG')
        output_images.append(image_path)
    return output_images


def main():
    parser = init_argparse()
    args = parser.parse_args()

    target_file = args.input.name
    output_folder = args.output

    is_pdf_input = lambda filename: filename.lower().endswith('pdf')
    if not is_pdf_input(target_file):
        sys.stderr.write('Input file must be .pdf')
        sys.exit(1)

    images = convert_pdf_to_image(target_file, output_folder)
    print(images)


if __name__ == '__main__':
    main()
