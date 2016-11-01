import json
import os
import re


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name  for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


def get_dsn():
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        return get_elephantsql_dsn(VCAP_SERVICES)
    else:
        return """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""
