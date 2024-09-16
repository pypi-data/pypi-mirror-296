from pathlib import Path

import fitz

from .processed_page import ProcessedPage


class ProcessedDoc(fitz.Document):
    """Class to provide extra methods to pymupdf doc class"""

    def __init__(self, fname: Path = None, stream: bytes = None) -> None:
        if not fname:
            super().__init__(stream=stream)
        else:
            super().__init__(filename=str(fname))

    def crop_pdf_bytes(self, from_page: int, to_page: int) -> bytes:
        """
        Crop the PDF document from the specified starting page to the specified ending page and return the cropped document as bytes.

        Args:
        - from_page (int): The starting page number (inclusive) for cropping the document.
        - to_page (int): The ending page number (inclusive) for cropping the document.

        Returns:
        - bytes: The cropped document as bytes.
        """
        page_doc = fitz.open()
        page_doc.insert_pdf(self, from_page=from_page, to_page=to_page)
        page_doc_bytes = page_doc.write()
        page_doc.close()
        return page_doc_bytes

    def load_page(self, key) -> ProcessedPage:
        return ProcessedPage(super().load_page(key))

    def __getitem__(self, i: int = 0) -> ProcessedPage | list[ProcessedPage]:
        if isinstance(i, slice):
            return [self[j] for j in range(*i.indices(len(self)))]
        assert isinstance(i, int) or (
            isinstance(i, tuple) and len(i) == 2 and all(isinstance(x, int) for x in i)
        ), f"Invalid item number: {i=}."
        if i not in self:
            raise IndexError(f"page {i} not in document")
        return self.load_page(i)
