
import importlib
from barsxml.xmlprod.barsxml import BarsXml

def test_app():
    config =  importlib.import_module(f'barsxml.tests.xml_dbf_config')
    print('RR dir', config.RR_DIR)
    xml = BarsXml(config, "app", "04", "01")
    rc, pc, zname, errors = xml.make_xml(False, False, False)
    log = f"APP rc={rc}  pc={pc}  zname={zname}, errors={errors}"
    print(log)


def test_dsc():
    config = importlib.import_module(f'barsxml.tests.xml_dbf_config')
    xml = BarsXml(config, "dsc", "04", "01")
    rc, pc, zname, errors = xml.make_xml(False, False, False)
    log = f"DSC rc={rc}  pc={pc}  zname={zname}, errors={errors}"
    print(log)


def test_pcr():
    config =  importlib.import_module(f'barsxml.tests.xml_dbf_config')
    xml = BarsXml(config, "pcr", "04", "01")
    rc, pc, zname, errors = xml.make_xml(False, False, False)
    log = f"PCR rc={rc}  pc={pc}  zname={zname}, errors={errors}"
    print(log)


def test_ifa():
    config = importlib.import_module(f'barsxml.tests.xml_dbf_config')
    xml = BarsXml(config, "ifa", "04", "01")
    rc, pc, zname, errors = xml.make_xml(False, False, False)
    log = f"IFA rc={rc}  pc={pc}  zname={zname}, errors={errors}"
    print(log)


def test_tra():
    config = importlib.import_module(f'barsxml.tests.xml_dbf_travma_config')
    xml = BarsXml(config, "tra", "04", "01")
    rc, pc, zname, errors = xml.make_xml(False, False, False)
    log = f"TRA rc={rc}  pc={pc}  zname={zname}, errors={errors}"
    print(log)

