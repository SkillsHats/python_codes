from PyPDF4 import PdfFileMerger
import os
import argparse


def init_argparse() -> argparse.ArgumentParser:
    """Get user command line parameters"""
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] ...",
        description="Merge PDF File."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-i', '--input_files', dest='input_files', nargs='*',
                        type=str, required=True, help="Enter the path of the files to process")
    parser.add_argument('-p', '--page_range', dest='page_range', nargs='*',
                        help="Enter the pages to consider e.g.: (0,2) -> First 2 pages")
    parser.add_argument('-o', '--output_file', dest='output_file',
                        required=True, type=str, help="Enter a valid output file")
    parser.add_argument('-b', '--bookmark', dest='bookmark', default=True, type=lambda x: (
        str(x).lower() in ['true', '1', 'yes']), help="Bookmark resulting file")

    return parser


"""
USAGE:

python pdf_merger.py -i one.pdf,two.pdf -o output.pdf

# page range
python pdf_merger.py -i one.pdf,two.pdf -o output.pdf -p 0,2

# page range with step
python pdf_merger.py -i one.pdf,two.pdf -o output.pdf -p 0,6,2

# page range with step with bookmark
python pdf_merger.py -i one.pdf,two.pdf -o output.pdf -p 0,3 -b true
"""

class MergePDF:
    """ Merge a list of PDF files """

    def __init__(self, input_files: list, output_file: str):
        self.__input_files = input_files
        self.__output_file = output_file

        # strict = False -> To ignore PdfReadError - Illegal Character error
        self.__merger = PdfFileMerger(strict=False)

    def __append_pdf_page(self, page_range: tuple, bookmark: bool):
        for input_file in self.__input_files:
            bookmark_name = os.path.splitext(os.path.basename(input_file))[0] if bookmark else None
            
            # pages To control which pages are appended from a particular file.
            self.__merger.append(fileobj=open(input_file, 'rb'), 
                                pages=page_range, 
                                bookmark=bookmark_name)

    def __insert_pdf_page(self):
        """ Insert pdf page into the specific pages. """
        self.__merger.write(fileobj=open(self.__output_file, 'wb'))
        self.__merger.close()

    def merge_pdfs(self, page_range: tuple, bookmark: bool = True):
        """
        Merge a list of PDF files and save the combined result into the `output_file`.

        Args:
            page_range: tuple
                Select a range of pages (behaving like Python's range() function) from the input files
                e.g (0,2) -> First 2 pages 
                e.g (0,6,2) -> pages 1,3,5
            bookmark: bool
                Add bookmarks to the output file to navigate directly to the input file section within the output file.
        """
        
        # Append PDF Pages
        self.__append_pdf_page(page_range=page_range, bookmark=bookmark)
        
        # Insert the pdf at specific page
        self.__insert_pdf_page()


if __name__ == "__main__":
    # Parsing command line arguments entered by user
    parser = init_argparse()
    args = parser.parse_args()

    # convert a single str to a list 
    input_files = [str(x) for x in args.input_files[0].split(',')]
    page_range = None

    if args.page_range:
        page_range = tuple(int(x) for x in args.page_range[0].split(','))

    merge = MergePDF(input_files=input_files, output_file=args.output_file)
    merge.merge_pdfs(page_range=page_range, bookmark=args.bookmark)
