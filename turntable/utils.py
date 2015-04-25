'''
Provides a collection of methods used across the package or of general utility.

Example
~~~~~~~
>>> from relpy import utils
>>>
>>> string_date = '2014-05-03'
>>> date = utils.date_extract(string_date)

'''

import os
import re
import sys
import shutil
import numpy as np
import pandas as pd
try:
    import cPickle as pickle
except:
    import pickle
import fnmatch
import errno
import time


def readfile(filename):
    '''
    Checks the extension on the filename and reads the file with the appropriate method.
    *readfile* supports 'csv', 'xls', 'json' and 'pkl' formats.

    Parameters
    ----------
    filename : string, or file-like
        Valid file path or file handle. The string could be a URL.

    Returns
    -------
    The content of the file (DataFrame, array, etc...)

    '''

    if '.csv' in filename:
        content = pd.read_csv(filename)
        content = set_timestamps(content)
        # if we happen to pull the index from a previous save, remove the extra
        # column
        try:
            if all(content['Unnamed: 0'].values == content.index.values):
                content.drop(labels=['Unnamed: 0'], axis=1, inplace=True)
        except:
            pass
    elif '.xls' in filename:
        content = pd.read_excel(filename)
        content = set_timestamps(content)
    elif '.json' in filename:
        content = pd.read_json(filename)
    elif '.pkl' in filename:
        content = pd.read_pickle(filename)
    else:
        content = None
    return content


def to_pickle(obj, filename, cleanMemory=False):
    '''http://stackoverflow.com/questions/7900944/read-write-classes-to-files-in-an-efficent-way'''

    path, filename = path2filename(filename)

    create_dir(path)

    with open(path + filename, "wb") as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    if cleanMemory:
        obj = None

    # setting the global object to None requires a return assignment
    return obj


def from_pickle(filename, cleanDisk=False):
    # to deserialize the object
    with open(filename, "rb") as input:
        obj = pickle.load(input)  # protocol version is auto detected

    if cleanDisk:
        os.remove(filename)
    return obj


def path2filename(pathfile):
    '''path2filename takes a path filename string and returns the split between the path and the filename

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


def add_path_string(rootPath='./results', pathString=None):
    rootPath = path2filename(rootPath)[0]
    regEx = '[.<>"!,:;*/ -]'
    if pathString is not None:
        return path2filename(rootPath + re.sub(regEx, '_', pathString))[0]
    else:
        return rootPath


def create_dir(path, dirDict={}):
    '''
    Tries to create a new directory in the given path.
    **create_dir** can also create subfolders according to the dictionnary given as second argument.

    Parameters
    ----------
    path : string
        string giving the path of the location to create the directory, either absolute or relative.
    dirDict : dictionnary, optional (the default is {}, which means that no subfolders will be created)
        Dictionnary ordering the creation of subfolders. Keys must be strings, and values either None or path dictionnaries.

    Examples
    --------

    >>> path = './project'
    >>> dirDict = {'dir1':None, 'dir2':{'subdir21':None}}
    >>> utils.create_dir(path,dirDict)

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

    for key in dirDict.keys():
        rootPath = path + "/" + key
        try:
            os.makedirs(rootPath)
        # If the file already exists (EEXIST), raise exception and do nothing
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        if dirDict[key] is not None:
            create_dir(rootPath, dirDict[key])


def Walk(root='.', recurse=True, pattern='*'):
    """
        Generator for walking a directory tree.
        Starts at specified root folder, returning files
        that match our pattern. Optionally will also
        recurse through sub-folders.

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

    """
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                yield os.path.join(path, name)
        if not recurse:
            break


def scanPath(root='.', recurse=False, pattern='*'):
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
    pathList : list
        The list of all the matching files paths.

    '''

    pathList = []
    for path in Walk(root=root, recurse=recurse, pattern=pattern):
        pathList.append(path)
    return pathList


class Timer:

    '''

    Timer that calculates time remaining for a process and the percent complete

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


def float_to_string(float_array):
    '''
    Converts an array of  floats into a "readable"
    array of strings (i.e. strings without too many
    caracters, easier to print out on a plot or else).

    Parameters
    ----------
    float_array : array-like
        Array of floats

    Returns
    -------
    string_array : list of strings
        Array of strings made from the floats

    Examples
    --------
    >>> float_ar = [12154.4861652, 2135.355,.0000168498,0.001265,125.35]
    >>> utils.float_to_string(float_ar)
    ['1.22e4', 2135, '1.68e-5', '1.26e-3', '125.3']

    '''

    scalar = np.isscalar(float_array)
    if scalar:
        float_array = [float_array]

    string_array = []
    for f in float_array:
        es = format(f, 'e')
        core, exp = es.split('e')
        core = float(core)
        exp = int(exp)
        if exp > 3 or exp < -1:
            core = round(core, 2)
            sf = str(core) + 'e' + str(exp)
        elif exp > -2 and exp < 3:
            prec = 3 - abs(exp)
            core = round(f, prec)
            sf = str(core)
        else:
            sf = int(f)
        string_array.append(sf)

    if scalar:
        return string_array[0]
    else:
        return string_array
