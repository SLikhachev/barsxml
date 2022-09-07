""" import sql provider module """

import importlib

def get_sql_provider(config):
    """ import settings from barsxml/sql/sql...py module """
    return importlib.import_module(f'barsxml.sql.sql{config.SQL_PROVIDER}')
