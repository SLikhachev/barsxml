""" import sql provider module """

import importlib

def get_sql_provider(config):
    """ import """
    #print('SQL %s ' % config.SQL)
    return importlib.import_module(f'barsxml.sql.sql{config.SQL_PROVIDER}')
