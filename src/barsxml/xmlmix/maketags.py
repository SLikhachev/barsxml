"""  doc """

#import xml.etree.cElementTree as ET
import xml.etree.ElementTree as ET
#from barsxml.xmlproc.datadict import DataDict
from barsxml.xmlstruct.hmxml import HmStruct as hmNS
from barsxml.xmlstruct.pmxml import PmStruct as pmNS
from barsxml.xmlstruct.lmxml import LmStruct as lmNS


class TagError(Exception):
    """ doc """

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
    __slots__ = ('mo_code', '_mo', 'lpu', 'xns', 'const', 'countable', 'count')

    def __init__(self, mo_code: str, _mo: str):
        self.mo_code = mo_code  # string(6) digits
        self._mo = _mo  # string(3) last 3 digits
        self.lpu = mo_code
        self.xns = {'hm': hmNS, 'pm': pmNS, 'lm': lmNS}
        self.const = {}
        self.countable = {}
        self.count = {}
        self.init_const_count()

    def init_const_count(self):
        """ doc """
        for ns_name, ns_obj in self.xns.items():

            # init const tags dict
            const = getattr(ns_obj, 'CONST', None)
            if const and isinstance(const, dict):
                self.const[ns_name] = const

            # init count tags dict
            count = getattr(ns_obj, 'COUNTABLE', None)
            if count and isinstance(count, dict):
                self.count[ns_name] = {}
                self.countable[ns_name] = count

    def next_item(self, cns: str, tag: str):
        """ doc """
        if self.count.get(cns, None) is None:
            return None
        if self.count[cns].get(tag, None) is None:
            return None
        if (self.count.get(cns, None) or self.count[cns].get(tag, None)) is None:
            return None
        self.count[cns][tag] += 1
        return self.count[cns][tag]

    def next_init(self, cns: str, tag: str):
        """ doc """
        tcount = self.countable[cns].get(tag, None)
        if tcount:
            self.count[cns][tcount] = 0

    def nxt_el(self, tag: str, val: any):
        """ doc """
        if val is None or len(str(val)) == 0:
            return None
        _el = ET.Element(tag.upper())
        _el.text = f'{val}'
        return _el

    def leaf_els(self, cns: str, tag: any, data: dict):
        """ cns current namespace
            tag current tag
            data current UserDict
        """
        # if tree (root: string, body: tuple)
        if isinstance(tag, tuple):

            # data dict has list - {tag: list(items)}
            assert isinstance(tag[0], str), f"Неверная структра элемента {tag}"
            value = data.get(tag[0].lower(), None)

            # print(f'{tag[0]}={value}')

            # if must be dropped, enclosed trees should be present as empty list in data
            if isinstance(value, list):
                if len(value) > 0:
                    # return an [ET.Element]
                    return self.make_list(cns, tag, value)
                # drop this tree
                return None

            # return single tree el
            return [self.make_tree(cns, tag, data)]

        # simple tag
        # ignore tag
        if tag in self.xns[cns].IGNORED:
            return None

        # get value from data dict or self.attrs or NS CONST or COUNT
        val = data.get(tag, None)
        if val is None:
            val = getattr(self, tag, None)
            if val is None:
                val = self.const[cns].get(tag, None)
                if val is None:
                    val = self.next_item(cns, tag)

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

    def make_tree(self, cns: str, tree: tuple, data: dict):
        """ Start make Xml Tree
            tags must be tuple always
            (root: string, body: tuple)
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
                    _e) from _e

        return proot

    def make_list(self, cns: str, tag: tuple, elems: list):
        """doc """
        self.next_init(cns, tag[0])
        return [self.make_tree(cns, tag, el) for el in elems]
