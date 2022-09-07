""" Definition of the xml tree maker
    walks trough xml file definitons at xmlstruct pack/hm(lm, pm)struct.py NS
    and makes the xml tree, which then writes to the tmp files
    tags values get from dict which keys identical with tags names in the NS
"""

from typing import List
from collections import defaultdict
import xml.etree.ElementTree as ET
from barsxml.xmlstruct.hmxml import HmStruct as hmNS
from barsxml.xmlstruct.pmxml import PmStruct as pmNS
from barsxml.xmlstruct.lmxml import LmStruct as lmNS


class TagError(Exception):
    """ custom exc """

    def __init__(self, msg, original_exception):
        super(TagError, self).__init__(f'{msg}: ({original_exception})')
        self.original_exception = original_exception


class XmlTreeMaker:

    '''
    def __getattr__(self, name):
        if name in self.__dict__.keys():
            return self.__dict__[name]
        else:
            raise AttributeError("No such attribute: " + name)
    '''

    # self attributes for some xml tags: 'lpu', 'mo_code'
    __slots__ = ('mo_code', '_mo', 'lpu', 'xns', 'const', 'countable', 'count')

    def __init__(self, mo_code: str, _mo: str):
        self.mo_code = mo_code  # string(6) digits
        self._mo = _mo  # string(3) last 3 digits
        self.lpu = mo_code

        # namespaces def as dict, we need all three refs
        # case of xml files writes successively, no need three different classes
        self.xns = {'hm': hmNS, 'pm': pmNS, 'lm': lmNS}

        # const tags just dict(ns=dict(tag=value))
        self.const = {}

        # countable tags just dict(ns=dict(node_tag=count_tag))
        self.countable = {}

        # count values just dict(ns=dict(tag=value))
        self.count = {}

        self.init_const_and_count()


    def init_const_and_count(self):
        """ select const and countable tags from NSs, then fill the self state dicts"""
        for ns_name, ns_obj in self.xns.items():

            # init const tags dict( namespace: const_dict )
            const = getattr(ns_obj, 'CONST', None)
            if const and isinstance(const, dict):
                self.const[ns_name] = const

            # init count tags dict( namespace: count_dict )
            count = getattr(ns_obj, 'COUNTABLE', None)
            if count and isinstance(count, dict):
                self.count[ns_name] = defaultdict(int)
                self.countable[ns_name] = count


    def next_countable_item(self, cns: str, tag: str) -> int or None:
        """ produce next countable tag if any, workaround with simple dicts
            dont use complex datatypes (descriptors, classes, generators, ...)
            @param: cns - current namespace
            @param: tag - tag name

            return None or int
        """
        # Dont have countable tags in namespace
        if self.count.get(cns, None) is None:
            return None

        # Dont countable tag
        if self.count[cns].get(tag, None) is None:
            return None

        # increment tag value
        self.count[cns][tag] += 1
        return self.count[cns][tag]


    def next_countable_init(self, cns: str, tag: str):
        """ reset countable tag value """
        tag_count = self.countable[cns].get(tag, None)
        if tag_count:
            self.count[cns][tag_count] = 0


    def nxt_el(self, tag: str, val: any) -> ET.Element or None:
        """ produce next xml element node """
        if val is None or len(str(val)) == 0:
            return None
        _el = ET.Element(tag.upper())
        _el.text = f'{val}' # value to string
        return _el


    def leaf_els(self, cns: str, tag: any, data: dict) -> List[ET.Element] or None:
        """ main func analyze tag param with current name space and data
            @param: cns - current name space
            @param: tag - current tag: string | tuple(string, tuple)
            @param: data - current data dict

            return None if tag ignored else List[ET.Element]
        """
        # check if tree (root: string, body: tuple)
        if isinstance(tag, tuple):
            assert isinstance(tag[0], str), f"Неверная структра элемента {tag}"

            # get value from the dict
            value = data.get(tag[0].lower(), None)

            # may be data dict has list - {tag: list(items)}
            # if this tag must be dropped,
            # enclosed trees should be present as empty list in data
            if isinstance(value, list):
                if len(value) > 0:
                    # return a List[ET.Element]
                    return self.make_list(cns, tag, value)
                # drop this tree
                return None

            # return single ET.Element tail recursive call
            return [self.make_tree(cns, tag, data)]

        # simple tag
        # ignore tag
        if tag in self.xns[cns].IGNORED:
            return None

        # get value from data dict
        val = data.get(tag, None)

        # apply simple imperative logic
        if val is None:
            # or self.attrs
            val = getattr(self, tag, None)

            if val is None:
                # or NS.CONST
                val = self.const[cns].get(tag, None)

                if val is None:
                    # is a countable tag
                    val = self.next_countable_item(cns, tag)

        # value for tag not found is tag reqired ?
        if val is None:
            if tag in self.xns[cns].REQUIRED:
                raise AttributeError(
                    f'{data["idcase"]}-Нет тега: {tag} в талоне')
            return None

        # many same tags with differnet text value
        if isinstance(val, list):
            return [self.nxt_el(tag, v) for v in val]

        # simple text tag
        return [self.nxt_el(tag, val)]


    def make_tree(self, cns: str, tree: tuple, data: dict) -> ET.Element:
        """ Start point to make Xml Tree
            @params: cns - current namespace ('hm', 'lm', 'pm')
            @param: tree - must be tuple always (root: string, body: tuple)
            @param: data - dict which keys may be identical with tag names

        """
        root, body = tree
        proot = ET.Element(root.upper())
        for tag in body:
            els = self.leaf_els(cns, tag, data)
            if els is None:
                continue
            try:
                for _el in els:
                    if isinstance(_el, ET.Element):
                        proot.append(_el)
            except Exception as _e:
                raise TagError(
                f'{data["idcase"]}-Ошибка формиривания: TagError::  root: {root}, tag: {tag}, el: {_el}',
                _e
                ) from _e

        return proot


    def make_list(self, cns: str, tag: tuple, elems: list) -> List[ET.Element]:
        """ produce list of xml element nodes """

        # if tag is countable, reset
        self.next_countable_init(cns, tag[0])

        # make
        return [self.make_tree(cns, tag, el) for el in elems]
