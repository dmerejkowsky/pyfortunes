from distutils.core import setup


setup(name='pyfortunes',
    version='0.1',
    description='XML RPC client/server for a fortune database',
    author_email = 'yannicklm1337@gmail.com',
    author = 'yannicklm',
    packages = ['pyfortunes'],
    scripts  = [
        'pyfortunes/bin/pyf-add',
        'pyfortunes/bin/pyf-get',
        'pyfortunes/bin/pyfd',
    ],
    data_files = [
        ('/etc', ["etc/pyfd.conf"]),
    ],
    license  = 'BSD',
    classifiers      = [
        "Development Status :: 4 - Beta"
        "Environment :: Console",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Topic :: System :: Shells",
        "Operating System :: POSIX :: Linux",
    ],
)

