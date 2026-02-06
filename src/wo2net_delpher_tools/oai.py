from sickle import Sickle

def oai_get_record(identifier: str, prefix: str = 'DDD:'):
    oai_identifier = prefix + identifier
    sickle = Sickle('https://services.kb.nl/mdo/oai')
    record = sickle.GetRecord(identifier=oai_identifier, metadataPrefix='didl')
    return record