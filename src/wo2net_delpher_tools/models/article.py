from typing import Optional

class Article:
    def __init__(
        self,
        identifier: str,
        title: str,
        subject: Optional[str] = None,
        url: Optional[str] = None,
        ocr: Optional[str] = None,
        ocr_text: Optional[str] = None
    ):
        self.identifier = identifier
        self.title = title
        self.subject = subject
        self.url = url
        self.ocr = ocr
        self.ocr_text = ocr_text

    def to_dict(self):
        return {
            'identifier': self.identifier,
            'title': self.title,
            'subject': self.subject,
            'url': self.url,
            'ocr': self.ocr,
            'ocr_text': self.ocr_text
        }