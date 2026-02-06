from typing import Optional
from .article import Article
from .page import Page
from lxml import etree

class Issue:
    def __init__(
        self,
        identifier: str,
        url: str,
        ppn: str,
        title: Optional[str] = None,
        date: Optional[str] = None,
        source: Optional[str] = None,
        rights: Optional[str] = None,
        publisher: Optional[str] = None,
        volume: Optional[str] = None,
        issue_number: Optional[str] = None,
        issued: Optional[str] = None,
        spatial: Optional[str] = None,
        articles: Optional[list[Article]] = None,
        pages: Optional[list[Page]] = None
    ):
        self.identifier = identifier
        self.url = url
        self.ppn = ppn
        self.title = title
        self.source = source
        self.date = date
        self.rights = rights
        self.publisher = publisher
        self.volume = volume
        self.issue_number = issue_number
        self.issued = issued
        self.spatial = spatial
        self.articles = articles or []
        self.pages = pages or []
    
    @classmethod
    def from_oai_record(cls, record):
        root = etree.fromstring(record.raw)
        ns = {
            'didl': 'urn:mpeg:mpeg21:2002:02-DIDL-NS',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'dcx': 'http://krait.kb.nl/coop/tel/handbook/telterms.html',
            'oai': 'http://www.openarchives.org/OAI/2.0/',
            'srw_dc': 'info:srw/schema/1/dc-v1.1',
            'dcterms': 'http://purl.org/dc/terms/',
            'dcmitype': 'http://purl.org/dc/dcmitype/',
            'ddd': 'http://www.kb.nl/namespaces/ddd',
            'didmodel': 'urn:mpeg:mpeg21:2002:02-DIDMODEL-NS',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        }

        def get_text(element, xpath, namespaces):
            result = element.xpath(xpath, namespaces=namespaces)
            return result[0].text if result else None
        
        def get_attribute(element, xpath, namespaces):
            result = element.xpath(xpath, namespaces=namespaces)
            return result[0] if result else None

        issue_identifier = root.xpath('//oai:header/oai:identifier', namespaces = ns)[0].text.split('DDD:')[-1]
        url = 'https://resolver.kb.nl/resolve?urn=' + issue_identifier.split(':mpeg21')[0]
        item = root.xpath(f'//didl:Item[@dc:identifier="{issue_identifier}"]', namespaces = ns)[0]
        metadata = item.xpath(f'./didl:Component[@dc:identifier="{issue_identifier}:metadata"]/didl:Resource/srw_dc:dcx', namespaces = ns)[0]
        ppn = get_text(metadata, './dc:identifier[@xsi:type="dcx:PPN"]', ns)
        title = get_text(metadata, './dc:title', ns)
        date = get_text(metadata, './dc:date', ns)
        source = get_text(metadata, './dc:source', ns)
        rights = get_text(metadata, './dc:rights', ns)
        publisher = get_text(metadata, './dc:publisher', ns)
        volume = get_text(metadata, './dcx:volume', ns)
        issue_number = get_text(metadata, './dcx:issuenumber', ns)
        issued = get_text(metadata, './dcterms:issued', ns)
        spatial = get_text(metadata, './dcterms:spatial', ns)

        issue = cls(
            identifier = issue_identifier,
            url = url,
            ppn = ppn,
            title = title,
            date = date,
            source = source,
            rights = rights,
            publisher = publisher,
            volume = volume,
            issue_number = issue_number,
            issued = issued,
            spatial = spatial
        )

        article_indicator = f"{issue_identifier}:a"
        article_items = item.xpath(f'./didl:Item[contains(@dc:identifier, "{article_indicator}")]', namespaces=ns)

        for article in article_items:
            identifier = article.get('{http://purl.org/dc/elements/1.1/}identifier')
            article_metadata = article.xpath(f'./didl:Component[@dc:identifier="{identifier}:metadata"]/didl:Resource/srw_dc:dcx', namespaces = ns)[0]
            title = get_text(article_metadata, './dc:title', ns)
            subject = get_text(article_metadata, './dc:subject', ns)
            url = get_text(article_metadata, './dc:identifier', ns)
            ocr = get_attribute(article, f'./didl:Component[@dc:identifier="{identifier}:ocr"]/didl:Resource/@ref', ns)
            article_object = Article (
                identifier = identifier,
                title = title,
                subject = subject,
                url = url,
                ocr = ocr
            )
            issue.articles.append(article_object)

        page_indicator = f"{issue_identifier}:p"
        page_items = item.xpath(f'./didl:Item[contains(@dc:identifier, "{page_indicator}")]', namespaces=ns)
        for page in page_items:
            identifier = page.get('{http://purl.org/dc/elements/1.1/}identifier')
            page_metadata = page.xpath(f'./didl:Component[@dc:identifier="{identifier}:metadata"]/didl:Resource/srw_dc:dcx', namespaces = ns)[0]
            page_number = get_text(page_metadata, './ddd:nativePageNumber', ns)
            image_url = get_attribute(page, f'./didl:Component[@dc:identifier="{identifier}:image"]/didl:Resource/@ref', ns)
            page_url = get_text(page_metadata, './dc:identifier', ns)
            
            page_articles = []
            page_object = Page(
                identifier = identifier,
                page_number = page_number,
                image = image_url,
                url = page_url,
                articles = page_articles
            )

            page_article_items = page.xpath(f'.//didl:Item[@ddd:article_id]', namespaces=ns)
            for page_article_item in page_article_items:
                article_id = page_article_item.get('{http://www.kb.nl/namespaces/ddd}article_id')
                for article in issue.articles:
                    if article.identifier == article_id:
                        page_object.articles.append(article)

            issue.pages.append(page_object)
        return issue

    def to_dict(self):
        return {
            'identifier': self.identifier,
            'url': self.url,
            'ppn': self.ppn,
            'title': self.title,
            'date': self.date,
            'source': self.source,
            'rights': self.rights,
            'publisher': self.publisher,
            'volume': self.volume,
            'issue_number': self.issue_number,
            'issued': self.issued,
            'spatial': self.spatial,
            'articles': [article.to_dict() for article in self.articles],
            'pages': [page.to_dict() for page in self.pages]
        }