
from barsxml.path.thispath import Path
from barsxml.config.xmltype import TYPES


class ConfigAttrs:
    
    def __init__(self, config: object, pack_type: str, mo_code: str, month: str, pack_num: int):
        """ pack_type is: 'sss'( n - n is pack_num )
            app - app 0-1n ambulanse
            dsc - day stac 2n
            onk - onko 3n (C packet)
            dia - diagnostic 4n
            sto - stomatolog 5n
            not used 6n
            pcr - pcr 7n
            ifa  ifa 8n
            tra - travma 9n
            xml - for simple packages of diagnistic 0
        """
        self.pack_type = pack_type  # string(3)
        self.pack_type_digit = TYPES[pack_type] % 10 # digit 0-9

        # No chek for right code? may be exception
        self.mo_code = mo_code # string MO in 250796 format
        self.mo = mo_code[3:] # last 3 digits i.e 796

        self.xmldir = Path( str(config.BASE_XML_DIR) )
        if len(pack_type) > 0:
            self.xmldir = self.xmldir / pack_type   # str abs path to save xml file

        self.year = config.YEAR  # string(4) digits
        self.month = month  # string(2) digits
        self.pack_number = int(pack_num) % 10 # digit 0-9


