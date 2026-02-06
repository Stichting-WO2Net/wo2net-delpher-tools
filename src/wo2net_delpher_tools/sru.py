import requests
from urllib.parse import quote
from lxml import etree

def _get_delpher_item_identifiers_from_ppn(ppn_number: int, constraints: str = "(date >= 1940) AND (date <= 1945)", collection: str = 'DDD_artikel', max_records: int = 25):
    identifiers = []
    query = quote(f"{constraints} AND ppn any ({ppn_number})")
    start_record = 1

    while True:
        url = f"https://jsru.kb.nl/sru/sru?operation=searchRetrieve&version=1.2&recordSchema=dc&query={query}&x-collection={collection}&maximumRecords={max_records}&startRecord={start_record}"
    
        response = requests.get(url)
        
        if response.status_code != 200:
                raise Exception(f"SRU request failed: {response.status_code}")
        
        content = response.content
        root = etree.fromstring(content)
        ns = {
            "srw": "http://www.loc.gov/zing/srw/",
            "dc": "http://purl.org/dc/elements/1.1/"
        }

        nr_of_records = int(root.xpath("srw:numberOfRecords/text()", namespaces=ns)[0])
        batch_identifiers = root.xpath("//srw:recordData/dc:identifier/text()", namespaces=ns)
        identifiers.extend(batch_identifiers)


        if start_record + max_records > nr_of_records:
            break
        start_record += max_records
    return identifiers

def get_issue_identifiers(ppn_number: int, constraints: str = "(date >= 1940) AND (date <= 1945)", collection: str = 'DDD_artikel', max_records: int = 25):
    delpher_item_identifiers = _get_delpher_item_identifiers_from_ppn(ppn_number, constraints, collection, max_records)
    issue_identifiers = set()
    for item in delpher_item_identifiers:
        issue_id = item.split("urn=")[1].split(':a0')[0]
        issue_identifiers.add(issue_id)
    return list(issue_identifiers)