import sys
import os
import argparse
import logging
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import landscape, A4

try:
    from PIL import Image
except ImportError:
    logging.debug('PIL not found; cannot auto-print horizonal canvas' \
                  'if it is wide image')
    Image = None

IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'gif', 'png')
A4_WIDTH, A4_HEIGHT = A4

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] ...",
        description="Convert images into the pdf."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('srcdir', metavar='DIR',
                        help='Directory contains source image')
    parser.add_argument('-i', '--output', default='output.pdf',
                        help='name of PDF file to save')
    parser.add_argument('-r', '--norotate', action="store_true",
                        help='do not rotate canvas even if image is wide')
    parser.add_argument('-w', '--wide', action="store_true",
                        help='print pdf using widespread canvas')
    parser.add_argument('-f', '--fill', action="store_true",
                        help='fit canvas size to original image size')
    parser.add_argument('-ws', '--widesplit', action='store_true',
                        help='split images when it is widespread')
    return parser

def is_wide_image(imagepath):
    if not Image: return False
    
    im = Image.open(imagepath)
    res = im.size[0] > im.size[1]
    del im # implicit memory release
    return res

def split_wide_image(imagepath):
    if not Image: return False
    if not is_wide_image(imagepath): return False
    
    name, ext = os.path.splitext(imagepath)
    
    im = Image.open(imagepath)
    width, height = im.size
    im.crop((0, 0, int(width/2), height)).save('%s_0%s' % (name, ext))
    im.crop((int(width/2), 0, width, height)).save('%s_1%s' % (name, ext))
    
    del im
    os.unlink(imagepath)
    return True

def get_image_size(imagepath):
    if not Image: return False
    
    im = Image.open(imagepath)
    res = im.size
    del im
    
    return res

class PdfBuilder(object):
    def __init__(self, filename, pagesize=A4, fill=False):
        self.pagesize = pagesize
        self.filename = filename
        self.canvas = Canvas(filename, pagesize)
        self.fill = fill
    
    def add_image(self, imagepath, horizon=False):
        if self.fill:
            width, height = self.pagesize
            if horizon:
                width, height = height, width
        else:
            width, height = get_image_size(imagepath)
        
        self.canvas.setPageSize((width, height))
        self.canvas.drawImage(imagepath, 0, 0, width=width, height=height,
                              preserveAspectRatio=True)
        self.canvas.showPage()
        
    def save(self):
        self.canvas.save()

def get_image_list(path):
    for root, dirs, files in os.walk(path):
        if dirs: continue
        
        for filename in files:
            ext = os.path.splitext(filename)[1][1:]
            if ext.lower() in IMAGE_EXTENSIONS:
                yield os.path.join(root, filename)

def main():
    global Image
    
    parser = init_argparse()
    args = parser.parse_args()
  
    if args.norotate: Image = None # turn off rotation
    
    pagesize = A4
    if args.wide: pagesize = landscape(A4)
    logging.debug('Pagesize: %s' % repr(pagesize))
    
    if args.widesplit:
        splitn = filter(lambda x: x is True, \
            map(split_wide_image, get_image_list(args.srcdir)))
        logging.debug('splitted %d images' % len(splitn))
    
    pdf = PdfBuilder(args.output, pagesize=pagesize, fill=args.fill)
    for imagename in sorted(get_image_list(args.srcdir)):
        logging.debug(' Adding image %s' % repr(imagename))
        pdf.add_image(imagename, horizon=is_wide_image(imagename))
    
    pdf.save()

if __name__ == '__main__':
    main()