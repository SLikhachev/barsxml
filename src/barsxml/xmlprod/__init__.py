""" funct to get the Reporter class """

from .barsxml import BarsXml


def get_reporter(mis='bars'):
    """ return reporter class of the MIS, default 'bars' """
    return {
        'bars': BarsXml
    }[mis]
