from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pile import Pile


class Parser(object):
    def __init__(self, filename):
        self._document = self._read_file(filename)
        self._device, self._interpreter = self._prepare_tools()
        self._pages = {}

        self._HTML_DEBUG = True

    def extract(self, max_page_num=None):
        for page in PDFPage.create_pages(self._document):
            self._interpreter.process_page(page)
            layout = self._device.get_result()

            if max_page_num != None and layout.pageid > max_page_num:
                break

            self._pages[layout.pageid] = layout

    def parse(self, page_num=None):
        piles = []
        if page_num == None:
            for page_num, page in list(self._pages.items()):
                piles += self._parse_page(page)
        else:
            page = self._pages[page_num]
            piles = self._parse_page(page)
        return piles

    def _read_file(self, filename):
        parser = PDFParser(open(filename, 'rb'))
        document = PDFDocument(parser)
        return document

    def _prepare_tools(self):
        laparams = LAParams()
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        return device, interpreter

    def _parse_page(self, page):
        pile = Pile()
        pile.parse_layout(page)
        piles = pile.split_piles()
        return piles
