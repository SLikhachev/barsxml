from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='barsxml',
    version='0.1.19',
    url='https://github.com/SLikhachev/barsxml',
    author='SLikhachev',
    author_email='polaughing@yahoo.com',
    license='BSD2',
    description='make BARS XML packet from SQL',
    long_description=long_description,
    long_description_content_type="text/markdown",  
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    python_requires=">=3.6",
    
    packages=find_packages(
        where = 'src',
        exclude=['barsxml.tests']
    ),
    install_requires=['pyodbc >= 4.0.18', 'psycopg2 >= 2.7.3.2'], 
    zip_safe=False
)