
import importlib

def get_sql_provider(config):
    #print('SQL %s ' % config.SQL)
    return importlib.import_module(f'barsxml.sql.sql{config.SQL}')