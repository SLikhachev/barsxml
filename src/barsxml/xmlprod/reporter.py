""" Abstarct class def """

from typing import Tuple
from abc import ABC, abstractmethod


class XmlReport(ABC):
    """ base class for reporter """

    @abstractmethod
    def make_xml(self, limit: int, mark_sent: bool, get_fresh: bool, check: bool =False, sign: bool =False) -> Tuple[int, int, str, int]:
        """ main class method
            @params
            :limit: int - number of recorde to select from sql table as LIMIT sql clause
            :mark_sent: bool - if TRUE set records field talon_type = 2 else ignore
            :get_fresh: bool - if TRUE ignore already sent else get all records
            :check: bool - if TRUE -> check tables recs only, don't make xml pack
            :sign: bool - if TRUE -> sign each xml file with private key, and include *.sig file

            return Tuple[int, int, str, int]:
        """
