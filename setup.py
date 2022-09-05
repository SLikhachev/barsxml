from setuptools import setup, find_packages

setup(name='barsxml',
    version='0.2.0',
    url='https://github.com/SLikhachev/zomspa',
    author='SLikhachev',
    author_email='polaughing@yahoo.com',
    license='BSD2',
    description='comin soon',
    long_description='',
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
    install_requires=['psycopg2-binary == 2.9.2'],
    zip_safe=False
)
