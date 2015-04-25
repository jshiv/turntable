print '''
Installing turntable. Built by the Reliability Engineering Data Science Team at

    ############     ##########      ##########     ##             ###########
     ##########       ########       #########      ##              #########
         ##                          ##             ##
         ##                          ##             ##
         ##          ##########      ##########     ##              ##########
         ##           ########       ##########     ##              ##########
         ##                                  ##     ##              ##      ##
         ##                                  ##     ##              ##      ##
         ##          ##########      ##########     ##########      ##      ##
         ##           ########       ##########      ########       ##      ##
'''
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

from version import *
import sys


config = {
    'name':'turntable',
    'description': 'turntable is a module that provides a framework for multi-processing pandas DataFrames',
    'author': 'Jason Shiverick, Carlo Torniai, Anmol Garg, Ariel Shemtov',
    'url': 'not yet',
    'download_url': 'Where to download it.',
    'author_email': 'jshiverick@teslamotors.com, ctorniai@teslamotors.com, agarg@teslamotors.com, ashemtov@teslamotors.com',
    'version': get_git_version(),
    
    'install_requires': [
    'numpy',
    'pandas',
    'nose',
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