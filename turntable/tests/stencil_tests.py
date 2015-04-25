'''
nose test suite for stencil module

To run some specific tests below use;
nosetests -w tests tests/stencil_tests.py:test_series_loader
'''



from nose.tools import *
from turntable import press

import datetime
import pandas as pd



def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "Test basic"


def test_series_loader():
    print "Testing class SeriesLoader"
    
    series_loader = press.SeriesLoader()
    series_loader.one = 'one'
    print series_loader.series
    assert series_loader.one == 'one'
    assert series_loader.series.one == 'one'


def test_record():
	print "Testing class Record"

	record = press.Record(test = 'test')
	assert record.test == 'test'
	assert record.series.test == 'test'