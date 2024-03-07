""" funct to get the Reporter class """

''' Not Used potentially lead to error of the circular import
from .barsxml import BarsXml


def get_reporter(mis='bars'):
    """ return reporter class of the MIS, default 'bars' """
    return {
        'bars': BarsXml
    }[mis]

'''