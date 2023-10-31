""" XmlSigner class definition """

import subprocess as sup
from pathlib import Path
from tempfile import TemporaryDirectory
from barsxml.xmlproc.configx import ConfigAttrs

class XmlSigner:
    """ class definition """

    # openssl test
    TEST_ENGINE = 'openssl engine'
    #(dynamic) Dynamic engine loading support
    #(gost) Reference implementation of GOST engine

    TEST_CIPHERS='openssl engine gost -c'
    #md_gost12_256, md_gost12_512, gost-mac-12
    #gost2012_256, gost2012_512

    SIGN_FILE='''openssl cms -sign -signer {crt} -inkey {key} -CAfile {ca} \
    -engine gost -binary -outform DER \
    -in {file} -out {file}.sig'''


    # all files have fixed names
    PEM_FILES = {
        'crt': 'crt.der', # pub key certificate
        'key': 'key.pem', # priv key pem file
        'ca': 'ca.pem', # CA auth pem file (may be in chain)
    }

    def __init__(self, cfg: ConfigAttrs, tmpdir: TemporaryDirectory):

        self.pem_dir = Path( str(cfg.base_xml_dir) ) / 'pem'
        assert self.pem_dir.exists(), f"Каталог клчей {self.pem_dir} не найден"
        for _file in XmlSigner.PEM_FILES.values():
            assert (self.pem_dir / _file).exists(), f"Файл {_file} не найден"
        self.cwd = tmpdir

    def sign_xml(self, file):
        """ sign file with openssl """
        cmd = XmlSigner.SIGN_FILE.format(
            crt=self.pem_dir / XmlSigner.PEM_FILES['crt'],
            key=self.pem_dir / XmlSigner.PEM_FILES['key'],
            ca=self.pem_dir / XmlSigner.PEM_FILES['ca'],
            file=Path(self.cwd) / file)
        print(cmd)
        # if exeption will be arised it will be blown up
        sup.run(cmd, capture_output=True, check=True, text=True, shell=True)
