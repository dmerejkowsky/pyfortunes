import sys
from distutils.core import setup

on_win = sys.platform.startswith("win")

scripts = ['bin/pyf-add',
           'bin/pyf-get']
packages = ["pyfortunes", "pyfortunes.thirdparty"]

if on_win:
    scripts.extend(['bin/pyf-add.bat',
                    'bin/pyf-get.bat',
                    'bin/pyfd_service.py',
                    'bin/install_pyfd_service.bat'])
    data_files = list()
    package_data = {"pyfortunes" : ["pyfd.conf"]}
else:
    scripts.append('bin/pyfd')
    data_files = [('/etc/', ["pyfortunes/pyfd.conf"])]
    package_data = dict()


setup(name='pyfortunes',
    version='1.1.2',
    description='XML RPC client/server for a fortune database',
    author_email = 'yannicklm1337@gmail.com',
    author = 'yannicklm',
    packages = packages,
    scripts  = scripts,
    data_files = data_files,
    package_data = package_data,
    license  = 'BSD',
    classifiers      = [
        "Development Status :: 4 - Beta"
        "Environment :: Console",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Topic :: System :: Shells",
    ],
)

