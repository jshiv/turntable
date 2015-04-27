"""This is the docstring for the example.py module.  Modules names should
have short, all-lowercase names.  The module name may have underscores if
this improves readability.

Every module should have a docstring at the very top of the file.  The
module's docstring may extend over multiple lines.  If your docstring does
extend over multiple lines, the closing three quotation marks must be on
a line by itself, preferably preceeded by a blank line.

"""
# uncomment the following line to use python 3 features
#from __future__ import division, absolute_import, print_function

import shutil
import sys
import os  # standard library imports first

# Do NOT import using *, e.g. from numpy import *
#
# Import the module using
#
#   import numpy
#
# instead or import individual functions as needed, e.g
#
#  from numpy import array, zeros
#
# If you prefer the use of abbreviated module names, we suggest the
# convention used by NumPy itself::


import pandas as pd

import turntable.utils
#import parallel
import traceback


# These abbreviated names are not to be used in docstrings; users must
# be able to paste and execute docstrings after importing only the
# numpy module itself, unabbreviated.


class RecordPress(object):
    '''This class auto-seralizes any attributes assigned to an instance and clears them from memmory
    when an attribute is called via the dot operator, it is read from disk

    Parameters
    ----------
    pickle : Boolean [True]
        if False, the instance will behave as a normal class
    pickle_path : string ['./tmp']
        the path underwhich the files will be stored

    Methods
    -------
    clean_disk()
        deletes all files stored by the instance
    clean_memmory()
        sets the in memory attribute values to None reducing the memory footprint


    Examples
    --------
    This class can be encapsulated to be used elsewhere

    >>> class NewClass(RecordPress):
    >>>
    >>>  def __init__(self, pickle = True, pickle_path = './tmp'):
    >>>     self.pickle = pickle
    >>>     self.class_path = turntable.utils.path2filename(pickle_path+'/'+self.__class__.__name__)[0]
    >>>     self.pickles = []
    >>>
    >>> newClass = NewClass()
    >>> newClass.x = 10
    >>> y = newClass.x
    >>> newClass.clean_disk()
    '''
    def __init__(self, pickle=True, pickle_path='./tmp'):
        '''
        Parameters
        ----------
        pickle : pickle the class properties
        pickle_path : where to pickle
        '''

        self.pickle = pickle  # required for over setattr override function
        self.class_path = turntable.utils.path2filename(
            pickle_path + '/' + self.__class__.__name__)[0]
        self.pickles = []

    def __getattribute__(*args):
        # ignore these standard calls to class properties
        ignore_args_list = ['__dict__', '__members__', '__methods__',
                            '__class__', 'trait_names', '_getAttributeNames']
        if any([attr in args[1]
                for attr in ['pickle', 'class_path', 'pickles'] + ignore_args_list]):
            # if the name of the args matches the standard or required names,
            # recurse normally
            return object.__getattribute__(*args)
        else:
            self = args[0]  # 0th index is the class instance
            name = args[1]  # 1st index is the attribute lable requested
            # if this is a attribute from the pickles list, grab it from disk
            if self.pickle & (name in self.pickles):
                # print "Reading disk: ", self.class_path + name + '.pkl'
                return turntable.utils.from_pickle(
                    filename=self.class_path + name + '.pkl', cleanDisk=False)
            else:  # otherwise return the attribute from the class instance
                # print "Reading memory: ", name
                return object.__getattribute__(*args)

    def __setattr__(self, name, value):
        # first set the attribute to the instance of the class
        object.__setattr__(self, name, value)

        # test for the pickle command
        if self.pickle:
            # if the name of the assignend attribute is not a required name, go
            # ahead and pickle it
            if any(
                    [attr in name for attr in ['pickle', 'class_path', 'pickles']]) == False:
                return_value = turntable.utils.to_pickle(
                    obj=value,
                    filename=self.class_path +
                    name +
                    '.pkl',
                    cleanMemory=True)
                # return_value = None #for testing memmory
                self.__dict__[name] = return_value
                # turntable.utils.to_pickle(obj = value, filename = self.class_path + name + '.pkl', cleanMemory = False) #use this line to not default memory clearing
                # add the name to the list of pickled attributes, so we know
                # which attributes have been pickled
                self.pickles.append(name)
                self.pickles = list(set(self.pickles))
                # print "writing to disk: ", self.class_path + name + '.pkl'
            else:
                pass
                # print "writing to memory: ", name
        else:
            pass
            print  # "writing to memory: ", name

    def clean_memory(self):
        '''sets all attribute values from the attribute list pickles to None
        -this is the default behaviure so this method is redundent'''
        for key in self.pickles:
            self.__dict__[key] = None

    def clean_disk(self):
        '''clean removes all files and folders under the class_path directory'''
        shutil.rmtree(self.class_path)


class RecordSetter:

    '''RecordSetter provides a simple interface for initalizing arguments passed in kwargs
    and a runMethod method for running a class method by name


    Parameters
    ----------
    kwargs : name : value

    Examples
    --------
    RecordSetter is a general python class that assigns **kwargs as instances of its self.

    >>> obj = RecordSetter( name = 'me')
    >>> print obj.name
    me
    '''

    def __init__(self, **kwargs):
        self.set_attributes(kwargs)

    def set_attributes(self, kwargs):
        '''
        Initalizes the given argument structure as properties of the class
        to be used by name in specific method execution.

        Parameters
        ----------
        kwargs : dictionary
            Dictionary of extra attributes,
            where keys are attributes names and values attributes values.

        '''
        for key, value in kwargs.items():
            setattr(self, key, value)
            # print key, value

    def run_method(self, method):
        '''call a specied method by name using runMethod'''
        methodToCall = getattr(self, method)
        result = methodToCall()


class SeriesLoader(object):
    '''This class assignes given properties to a special pandas.Series propertie

    self.series

    Parameters
    ----------
    series : all atributes of the class get added to an internal pandas series


    Examples
    --------
    This class can be encapsulated to be used elsewhere

    >>> series_loader = SeriesLoader()
    >>> series_loader.one = 'one'
    >>> print series_loader.series
    '''
    def __init__(self):
        pass

    def __setattr__(self, name, value):
        # first set the attribute to the instance of the class
        object.__setattr__(self, name, value)
        # if the name of the assignend attribute is not a required name, go
        # ahead and pickle it
        blacklisted_keys = ['series']
        if any([attr in name for attr in blacklisted_keys]) == False:
            if 'series' in self.__dict__.keys():
                self.series[name] = value
            else:
                self.series = pd.Series(dict(
                    [(key, value) for key, value in self.__dict__.items() if key not in blacklisted_keys]))


class Record(RecordSetter, SeriesLoader):
    '''
    Record is a container object with a the special propertie "series"

    any propertie added to Record will also be added to the pandas.Series

    Properties
    ----------
    series : pandas.Series
        container for parameters set to the instance

    Methods
    -------
    set_attributes : assigns items of a dictionary to the class and to the series parameter
    runMethod : runs a method by a string call

    Examples
    --------
    lets see how we can add a propertie to the record object

    >>> record = Record(first_item = 'one')
    >>> record.second_item = 'two'
    >>> print record.series
    '''
    def __init__(self, **kwargs):

        self.set_attributes(kwargs)


def load_record(index_series_touple, kwargs):
    '''
    generates an instance of Record() from a touple of the form (index, pandas.Series) with associated parameters kwargs

    Paremeters
    ----------
    index_series_touple : (index, pandas.Series)
    kwargs : dict
        aditional arguments

    Returns
    -------
    Record()
    '''
    index_record = index_series_touple[0]
    series = index_series_touple[1]
    record = Record()
    record.series = series
    record.index_record = index_record
    record.set_attributes(kwargs)
    return record


def build_collection(df, **kwargs):
    '''
    build_collection generates a list of Record objects given a population DataFrame.
    Each record instance has a series attribute which is a pandas.Series of the same attributes in df.
    Optional datasets can be passed in through kwargs which
    will be included by the name of each object

    parameters
    ----------
    df : pandas.DataFrame
        each record represents a one individual from a population
    kwargs : alternate arguments to be saved by name to the series of each object

    Returns
    -------
    fleet : list
        list of Record() objects
    '''
    print 'Generating the Record Collection...'
    print ' '

    df['index_original'] = df.index
    df.reset_index(drop=True, inplace=True)

    if pd.__version__ >= '0.15.0':
        d = df.T.to_dict(orient='series')
    else:
        d = df.T.to_dict(outtype='series')

    collection = [load_record(item, kwargs) for item in d.items()]

    #collection = parallelBox.batch(d.items(), load_record, nb_proc=None, batchSize=None, quiet=True, kwargs_to_dump=None, args = kwargs)

    return collection


def collection_to_df(collection):
    return pd.concat([record.series for record in collection], axis=1).T


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
    The expected output of fcn or prints the exception traceback'''
    try:
        # remove the special kwargs key "spit" and use it to return if it
        # exists
        spit = kwargs.pop('spit')
    except:
        spit = None

    try:
        results = fcn(*args, **kwargs)
        if results is not None:
            return results
    except:
        # traceback.print_exc()
        print traceback.format_exc()
        if spit is not None:
            return spit


def foo(var1, var2, long_var_name='hi'):
    r"""A one-line summary that does not use variable names or the
    function name.

    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`.

    Parameters
    ----------------
    var1 : array_like
        Array_like means all those objects -- lists, nested lists, etc. --
        that can be converted to an array.  We can also refer to
        variables like `var1`.
    var2 : int
        The type above can either refer to an actual Python type
    Long_variable_name : {'hi', 'ho'}, optional
        Choices in brackets, default first when optional.

    Returns
    ----------------
    type
        Explanation of anonymous return value of type ``type``.
    describe : type
        Explanation of return value named `describe`.
    out : type
        Explanation of `out`.

    Other Para
    ----------------
    only_seldom_used_keywords : type
        Explanation
    common_parameters_listed_above : type
        Explanation

    Raises
    ------
    BadException
        Because you shouldn't have done that.

    See Also
    --------
    otherfunc : relationship (optional)
    newfunc : Relationship (optional), which could be fairly long, in which
              case the line wraps here.
    thirdfunc, fourthfunc, fifthfunc

    Notes
    -----
    Notes about the implementation algorithm (if needed).

    This can have multiple paragraphs.

    You may include some math:

    .. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

    And even use a greek symbol like :math:`omega` inline.

    References
    ----------
    Cite the relevant literature, e.g. [1]_.  You may also cite these
    references in the notes section above.

    .. [1] O. McNoleg, "The integration of GIS, remote sensing,
       expert systems and adaptive co-kriging for environmental habitat
       modelling of the Highland Haggis using object-oriented, fuzzy-logic
       and neural-network techniques," Computers & Geosciences, vol. 22,
       pp. 585-588, 1996.

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> a=[1,2,3]
    >>> print [x + 3 for x in a]
    [4, 5, 6]
    >>> print "a\n\nb"
    a
    b

    """

    pass
