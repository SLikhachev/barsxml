""" Abstarct class def """

from abc import ABC, abstractmethod


class XmlReport(ABC):
    """ base class for reporter """

    @abstractmethod
    def make_xml(self, mark_sent: bool, get_fresh: bool, check=False) -> tuple:
        """ single method to make xml report
            @param: mark_sent: mark records included in report as sent if True
            @param: get_fresh: ignore already sent records if True else include all records
            @param: check: if TRUE -> check records only, don't make xml pack

            return None
        """
