'''The utils module provides a collection of methods used across the package or of general utility.

'''

import os
import re
import sys
import shutil
import errno
import fnmatch
import numpy as np
import pandas as pd
try:
    import cPickle as pickle
except:
    import pickle
import random
import time

def catch(fcn, *args, **kwargs):
    '''try:
          retrun fcn(*args, **kwargs)
       except:
          print traceback
            if 'spit' in kwargs.keys():
                return kwargs['spit']

    Parameters
    ----------
    fcn : function
    *args : unnamed parameters of fcn
    **kwargs : named parameters of fcn
        spit : returns the parameter named return in the exception

    Returns
    -------
    The expected output of fcn or prints the exception traceback

    '''

    try:
        # remove the special kwargs key "spit" and use it to return if it exists
        spit = kwargs.pop('spit')
    except:
        spit = None

    try:
        results = fcn(*args, **kwargs)
        if results:
            return results
    except:
        print traceback.format_exc()
        if spit:
            return spit


def batch_list(sequence, batch_size, mod = 0, randomize = False):
    '''
    Converts a list into a list of lists with equal batch_size.

    Parameters
    ----------
    sequence : list
        list of items to be placed in batches
    batch_size : int
        length of each sub list
    mod : int
        remainder of list length devided by batch_size
        mod = len(sequence) % batch_size
    randomize = bool
        should the initial sequence be randomized before being batched
    
    '''

    if randomize:
        sequence = random.sample(sequence, len(sequence))

    return [sequence[x:x + batch_size] for x in xrange(0, len(sequence)-mod, batch_size)]



def to_pickle(obj, filename, clean_memory=False):
    '''http://stackoverflow.com/questions/7900944/read-write-classes-to-files-in-an-efficent-way'''

    path, filename = path_to_filename(filename)
    create_dir(path)

    with open(path + filename, "wb") as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    if clean_memory:
        obj = None

    # setting the global object to None requires a return assignment
    return obj


def from_pickle(filename, clean_disk=False):
    # to deserialize the object
    with open(filename, "rb") as input:
        obj = pickle.load(input)  # protocol version is auto detected

    if clean_disk:
        os.remove(filename)
    return obj


def path_to_filename(pathfile):
    '''
    Takes a path filename string and returns the split between the path and the filename

    if filename is not given, filename = ''
    if path is not given, path = './'

    '''

    path = pathfile[:pathfile.rfind('/') + 1]
    if path == '':
        path = './'

    filename = pathfile[pathfile.rfind('/') + 1:len(pathfile)]
    if '.' not in filename:
        path = pathfile
        filename = ''

    if (filename == '') and (path[len(path) - 1] != '/'):
        path += '/'

    return path, filename


def add_path_string(root_path='./results', path_string=None):
    rootPath = path_to_filename(rootPath)[0]
    regEx = '[.<>"!,:;*/ -]'
    if pathString is not None:
        return path_to_filename(root_path + re.sub(regEx, '_', path_string))[0]
    else:
        return root_path


def create_dir(path, dir_dict={}):
    '''
    Tries to create a new directory in the given path.
    **create_dir** can also create subfolders according to the dictionnary given as second argument.

    Parameters
    ----------
    path : string
        string giving the path of the location to create the directory, either absolute or relative.
    dir_dict : dictionary, optional 
        Dictionary ordering the creation of subfolders. Keys must be strings, and values either None or path dictionaries.
        the default is {}, which means that no subfolders will be created

    Examples
    --------

    >>> path = './project'
    >>> dir_dict = {'dir1':None, 'dir2':{'subdir21':None}}
    >>> utils.create_dir(path, dir_dict)

    will create:

    * *project/dir1*
    * *project/dir2/subdir21*

    in your parent directory.

    '''

    folders = path.split('/')
    folders = [i for i in folders if i != '']
    rootPath = ''
    if folders[0] == 'C:':
        folders = folders[1:]
    count = 0
    for directory in folders:
        count += 1

        # required to handle the dot operators
        if (directory[0] == '.') & (count == 1):
            rootPath = directory
        else:
            rootPath = rootPath + '/' + directory
        try:
            os.makedirs(rootPath)
        # If the file already exists (EEXIST), raise exception and do nothing
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    for key in dir_dict.keys():
        rootPath = path + "/" + key
        try:
            os.makedirs(rootPath)
        # If the file already exists (EEXIST), raise exception and do nothing
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        if dir_dict[key] is not None:
            create_dir(rootPath, dir_dict[key])

def Walk(root='.', recurse=True, pattern='*'):
    ''' 
    Generator for walking a directory tree.
    Starts at specified root folder, returning files that match our pattern. 
    Optionally will also recurse through sub-folders.

    Parameters
    ----------
    root : string (default is *'.'*)
        Path for the root folder to look in.
    recurse : bool (default is *True*)
        If *True*, will also look in the subfolders.
    pattern : string (default is :emphasis:`'*'`, which means all the files are concerned)
        The pattern to look for in the files' name.

    Returns
    -------
    generator
        **Walk** yields a generator from the matching files paths.

    '''

    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                yield os.path.join(path, name)
        if not recurse:
            break

def scan_path(root='.', recurse=False, pattern='*'):
    '''
    Runs a loop over the :doc:`Walk<relpy.utils.Walk>` Generator
    to find all file paths in the root directory with the given
    pattern. If recurse is *True*: matching paths are identified
    for all sub directories.

    Parameters
    ----------
    root : string (default is *'.'*)
        Path for the root folder to look in.
    recurse : bool (default is *True*)
        If *True*, will also look in the subfolders.
    pattern : string (default is :emphasis:`'*'`, which means all the files are concerned)
        The pattern to look for in the files' name.

    Returns
    -------
    path_list : list
        list of all the matching files paths.

    '''

    path_list = []
    for path in Walk(root=root, recurse=recurse, pattern=pattern):
        path_list.append(path)
    return path_list


class Timer:

    '''Timer that calculates time remaining for a process and the percent complete

    .. todo::

        Ask for details about the usage

    Parameters
    ----------
    nLoops : integer
    numPrints : integer (default is *100*)
    verbose : bool (default is *True*)

    Attributes
    ----------
    nLoops : integer
    numPrints : integer
    verbose : bool
        if *True*, print values when **loop** is called
    count : integer
    elapsed : float
        elapsed time
    est_end : float
        estimated end
    ti : float
        initial time
    tf : float
        current time
    display_amt : integer

    '''

    def __init__(self, nLoops, numPrints=100, verbose=True):

        self.nLoops = nLoops
        self.numPrints = numPrints
        self.verbose = verbose
        self.count = 0
        self.elapsed = 1
        self.est_end = 1
        self.ti = time.time()
        self.display_amt = 1

    def loop(self):
        '''
        Tracks the time in a loop. The estimated time to completion
        can be calculated and if verbose is set to *True*, the object will print
        estimated time to completion, and percent complete.
        Actived in every loop to keep track'''

        self.count += 1
        self.tf = time.time()
        self.elapsed = self.tf - self.ti

        if self.verbose:
            displayAll(self.elapsed, self.display_amt, self.est_end,
                       self.nLoops, self.count, self.numPrints)

    def fin(self):
        print "Elapsed time: %s  :-)" % str(time.time() - self.ti)


def displayAll(elapsed, display_amt, est_end, nLoops, count, numPrints):
    '''Displays time if verbose is true and count is within the display amount'''

    if numPrints > nLoops:
        display_amt = 1
    else:
        display_amt = round(nLoops / numPrints)

    if count % display_amt == 0:

        avg = elapsed / count
        est_end = round(avg * nLoops)

        (disp_elapsed,
         disp_avg,
         disp_est) = timeUnit(int(round(elapsed)),
                              int(round(avg)),
                              int(round(est_end)))

        print "%s%%" % str(round(count / float(nLoops) * 100)), "@" + str(count),

        totalTime = disp_est[0]
        unit = disp_est[1]

        if str(unit) == "secs":
            remain = totalTime - round(elapsed)
            remainUnit = "secs"
        elif str(unit) == "mins":
            remain = totalTime - round(elapsed) / 60
            remainUnit = "mins"
        elif str(unit) == "hr":
            remain = totalTime - round(elapsed) / 3600
            remainUnit = "hr"

        print "ETA: %s %s" % (str(remain), remainUnit)
        print

    return


def timeUnit(elapsed, avg, est_end):
    '''calculates unit of time to display'''
    minute = 60
    hr = 3600
    day = 86400

    if elapsed <= 3 * minute:
        unit_elapsed = (elapsed, "secs")
    if elapsed > 3 * minute:
        unit_elapsed = ((elapsed / 60), "mins")
    if elapsed > 3 * hr:
        unit_elapsed = ((elapsed / 3600), "hr")

    if avg <= 3 * minute:
        unit_avg = (avg, "secs")
    if avg > 3 * minute:
        unit_avg = ((avg / 60), "mins")
    if avg > 3 * hr:
        unit_avg = ((avg / 3600), "hr")

    if est_end <= 3 * minute:
        unit_estEnd = (est_end, "secs")
    if est_end > 3 * minute:
        unit_estEnd = ((est_end / 60), "mins")
    if est_end > 3 * hr:
        unit_estEnd = ((est_end / 3600), "hr")

    return [unit_elapsed, unit_avg, unit_estEnd]

