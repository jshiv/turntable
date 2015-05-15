print '''
Installing turntable....

 _____ _   _ ____  _   _ _____  _    ____  _     _____ 
|_   _| | | |  _ \| \ | |_   _|/ \  | __ )| |   | ____|
  | | | | | | |_) |  \| | | | / _ \ |  _ \| |   |  _|  
  | | | |_| |  _ <| |\  | | |/ ___ \| |_) | |___| |___ 
  |_|  \___/|_| \_|_| \_| |_/_/   \_|____/|_____|_____|
                                                       
'''
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import versioneer
import sys


config = {
    'description': 'TURNTABLE provides a functional framework for parallel processing DataFrames',
    'author': 'Jason Shiverick',
    'url': 'https://github.com/jshiv/turntable',
    'download_url': 'https://github.com/jshiv/turntable',
    'author_email': 'jshiv00@gmail.com',
    'license':'MIT',
    'version': versioneer.get_version(),
    'cmdclass': versioneer.get_cmdclass(),
    
    'install_requires': [
    'pandas',
    ],

    'packages': find_packages(),#['turntable'],
    'scripts': [],
    'name': 'turntable'
}



print "system is: "+sys.platform
print ''
print "installing turntable dependencies... "
print config['install_requires']

setup(**config)