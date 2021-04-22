from setuptools import setup, find_packages

setup(name='barsxml',
      version='0.1',
      url='https://github.com/SLikhachev/barsxml',
      license='BSD2',
      author='SLikhachev',
      author_email='polaughing@yahoo.com',
      description='make BARS XML packet from SQL',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)