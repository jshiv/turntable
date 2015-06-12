'''The press module is used to create Record Collections.

'''

import shutil
import sys
import os
import pandas as pd
import turntable.utils
import traceback

import turntable

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
    >>>     self.class_path = turntable.utils.path_to_filename(pickle_path+'/'+self.__class__.__name__)[0]
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
                    filename=self.class_path + name + '.pkl', clean_disk=False)
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
            if any([attr in name for attr in ['pickle', 'class_path', 'pickles']]) == False:
                return_value = turntable.utils.to_pickle(
                    obj=value,
                    filename=self.class_path+name+'.pkl', 
                    clean_memory=True)
                # return_value = None #for testing memmory
                self.__dict__[name] = return_value
                # use the below line to not default memory clearing
                # turntable.utils.to_pickle(obj = value, filename = self.class_path + name + '.pkl', clean_memory = False) 
                # add the name to the list of pickled attributes, so we know which attributes have been pickled
                self.pickles.append(name)
                self.pickles = list(set(self.pickles))
        #         print "writing to disk: ", self.class_path + name + '.pkl'
        #     else:
        #         pass
        #         print "writing to memory: ", name
        # else:
        #     pass
        #     print "writing to memory: ", name

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
    and a run method for running a class method by name


    Parameters
    ----------
    kwargs : name : value

    Examples
    --------
    RecordSetter is a general python class that assigns **kwargs as instances of it self.

    >>> obj = RecordSetter(name = 'me')
    >>> print obj.name
    me

    '''

    def __init__(self, **kwargs):
        self._set_attributes(kwargs)

    def _set_attributes(self, kwargs):
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
    def load(self, **kwargs):
        '''
        Takes an instance of Record() and named arguments from **kwargs
        returns the record instance with the named arguemnts added to the record


        Paremeters
        ----------
        **kwargs : named arguments
            first_arg = 1, second_arg = 'two'


        Returns
        -------
        record.first_arg -> 1
        record.second_arg -> 'two'

        Examples
        --------
        >>> import turntable
        >>> record = turntable.press.Record(first_arg = 1)
        >>> record = record.load(second_arg = 'two')
        >>> record.series
        first_arg       1
        second_arg    two
        '''
        
        self._set_attributes(kwargs)


    def run_method(self, method):
        '''
        Calls a specied method by name using run_method

        '''

        method_to_call = getattr(self, method)
        result = method_to_call()


class SeriesLoader(object):

    '''SeriesLoader assigns given properties to a special pandas.Series property: self.series.

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
        # if the name of the assigned attribute is not a required name, go
        # ahead and pickle it
        blacklisted_keys = ['series','pressed']
        if any([attr in name for attr in blacklisted_keys]) == False:
            if 'series' in self.__dict__.keys():
                self.series[name] = value
            else:
                self.series = pd.Series(dict(
                    [(key, value) for key, value in self.__dict__.items() if key not in blacklisted_keys]))



# class PressedRecord:
    
#     '''Record is a container object with the special property "series". Any 
#     property added to Record will also be added to the pandas.Series

#     Properties
#     ----------
#     series : pandas.Series
#         container for parameters set to the instance

#     Methods
#     -------
#     _set_attributes : assigns items of a dictionary to the class and to the series parameter
#     runMethod : runs a method by a string call

#     Examples
#     --------
#     lets see how we can add a propertie to the record object

#     >>> record = Record(first_item = 'one')
#     >>> record.second_item = 'two'
#     >>> print record.series
#     '''
#     mint = True




class Record(RecordSetter, SeriesLoader):
    
    '''Record is a container object with the special property "series". Any 
    property added to Record will also be added to the pandas.Series

    Properties
    ----------
    series : pandas.Series
        container for parameters set to the instance

    Methods
    -------
    load : assigns items of a **kwargs to the class and to the series parameter
    _set_attributes : assigns items of a dictionary to the class and to the series parameter
    runMethod : runs a method by a string call

    Examples
    --------
    lets see how we can add a propertie to the record object

    >>> record = Record(first_item = 'one')
    >>> record.second_item = 'two'
    >>> print record.series
    '''
    mint = True
    def __init__(self, **kwargs):
        self._set_attributes(kwargs)


# def load_record(index_series_tuple, kwargs):
#     '''
#     Generates an instance of Record() from a tuple of the form (index, pandas.Series) 
#     with associated parameters kwargs

#     Paremeters
#     ----------
#     index_series_tuple : tuple
#         tuple consisting of (index, pandas.Series)
#     kwargs : dict
#         aditional arguments

#     Returns
#     -------
#     Record : object

#     '''

#     index_record = index_series_tuple[0]
#     series = index_series_tuple[1]
#     record = Record()
#     record.series = series
#     record.index_record = index_record
#     record._set_attributes(kwargs)
#     return record


def load_record(record, **kwargs):
    '''
    Takes an instance of Record() and named arguments from **kwargs
    returns the record instance with the named arguemnts added to the record


    Paremeters
    ----------
    record : Record()
        either full or empty record object
    **kwargs : named arguments
        first_arg = 1, second_arg = 'two'


    Returns
    -------
    record.first_arg -> 1
    record.second_arg -> 'two'
    
    Examples
    --------
    >>> import turntable
    >>> record = load_record(turntable.press.Record(), first_arg = 1, second_arg = 'two')
    >>> record.series
    first_arg       1
    second_arg    two

    '''
    
    record._set_attributes(kwargs)
    return record




def build_collection(df, **kwargs):
    '''
    Generates a list of Record objects given a DataFrame.
    Each Record instance has a series attribute which is a pandas.Series of the same attributes 
    in the DataFrame.
    Optional data can be passed in through kwargs which will be included by the name of each object.

    parameters
    ----------
    df : pandas.DataFrame
    kwargs : alternate arguments to be saved by name to the series of each object

    Returns
    -------
    collection : list
        list of Record objects where each Record represents one row from a dataframe

    Examples
    --------
    This is how we generate a Record Collection from a DataFrame.

    >>> import pandas as pd
    >>> import turntable
    >>>
    >>> df = pd.DataFrame({'Artist':"""Michael Jackson, Pink Floyd, Whitney Houston, Meat Loaf, 
        Eagles, Fleetwood Mac, Bee Gees, AC/DC""".split(', '),
    >>> 'Album' :"""Thriller, The Dark Side of the Moon, The Bodyguard, Bat Out of Hell, 
        Their Greatest Hits (1971-1975), Rumours, Saturday Night Fever, Back in Black""".split(', ')})
    >>> collection = turntable.press.build_collection(df, my_favorite_record = 'nevermind')
    >>> record = collection[0]
    >>> print record.series

    '''

    print 'Generating the Record Collection...\n'

    df['index_original'] = df.index
    df.reset_index(drop=True, inplace=True)

    if pd.__version__ >= '0.15.0':
        d = df.T.to_dict(orient='series')
    else:
        d = df.T.to_dict(outtype='series')

    collection = [load_record(Record(), index_record = item[0], series = item[1], **kwargs) for item in d.items()]
    return collection

def collection_to_df(collection):
    ''' 
    Converts a collection back into a pandas DataFrame

    parameters
    ----------
    collection : list
        list of Record objects where each Record represents one row from a dataframe

    Returns
    -------
    df : pandas.DataFrame
        DataFrame of length=len(collection) where each row represents one Record 

    '''

    return pd.concat([record.series for record in collection], axis=1).T


def spin_frame(df, method):
    ''' 
    Runs the full turntable process on a pandas DataFrame

    parameters
    ----------
    df : pandas.DataFrame
        each row represents a record
    method : def method(record)
        function used to process each row

    Returns
    -------
    df : pandas.DataFrame
        DataFrame processed by method

    Example
    -------
    >>> import pandas as pd
    >>> import turntable
    >>>
    >>> df = pd.DataFrame({'Artist':"""Michael Jackson, Pink Floyd, Whitney Houston, Meat Loaf, Eagles, Fleetwood Mac, Bee Gees, AC/DC""".split(', '), 'Album':"""Thriller, The Dark Side of the Moon, The Bodyguard, Bat Out of Hell, Their Greatest Hits (1971–1975), Rumours, Saturday Night Fever, Back in Black""".split(', ')})
    >>>
    >>> def method(record):
    >>>    record.cost = 40
    >>>    return record
    >>>
    >>> turntable.press.spin_frame(df, method)
    

    '''
    collection = build_collection(df)
    collection = turntable.spin.batch(collection, method)
    return collection_to_df(collection)
