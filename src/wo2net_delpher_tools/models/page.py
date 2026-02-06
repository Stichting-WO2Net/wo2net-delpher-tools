from typing import Optional
from wo2net_delpher_tools.models.article import Article

class Page:
    def __init__(
        self,
        identifier: str,
        page_number: Optional[int] = None,
        image: Optional[str] = None,
        url: Optional[str] = None,
        articles: Optional[list[Article]] = None,
    ):
        self.identifier = identifier
        self.page_number = page_number
        self.image = image
        self.url = url
        self.articles = articles

    def to_dict(self):
        return {
            'identifier': self.identifier,
            'page_number': self.page_number,
            'image': self.image,
            'url': self.url,
            'article_identifiers': [article.identifier for article in self.articles]
        }