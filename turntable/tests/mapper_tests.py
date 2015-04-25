'''
nose test suite for stencil module

To run some specific tests below use;
nosetests -w tests tests/stencil_tests.py:test_series_loader
'''



from nose.tools import *
import time
from turntable import spin

import datetime
import pandas as pd



def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "Test basic"


def test_mapper_series():
    print "Testing mapper.series"
    
    f = lambda x:x**2.
    seq = range(100)
    assert sum(spin.series(seq, f)) == 328350.0

def f(i):
    o = i*i
    time.sleep(1)
    return o


def test_mapper_process():
    print "Testing mapper.process"


    seq = range(16)
    seq = spin.parallel(seq, f)

    assert sum(seq)==1240


def test_mapper_batch():
    print "Testing mapper.batch"


    seq = range(16)
    seq = spin.batch(seq, f)

    assert sum(seq)==1240

