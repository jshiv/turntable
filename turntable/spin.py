'''parallel contains best practices for parallel processing turntable.utilsities
	Authors: Jason Shiverick <jshiverick@teslamotors.com>
			 Carlo Torniai <ctorniai@teslamotors.com>
'''

# import multiprocessing tools (source:
# http://chriskiehl.com/article/parallelism-in-one-line/)
import multiprocessing as mp  # for processes
from multiprocessing.dummy import Pool as ThreadPool  # for threads

import time
import pickle
import os
import shutil

import turntable.utils


def series(sequence, function, *args, **kwargs):
    '''
    series(sequence[, sequence, ...], function) -> list

    Parameters
    ----------
    sequence : list of items to process
    function : function to process each item


    Return a list of the results of applying the function to the items of
    the argument sequence(s).  If more than one sequence is given, the
    function is called with an argument list consisting of the corresponding
    item of each sequence, substituting None for missing values when not all
    sequences have the same length.  If the function is None, return a list of
    the items of the sequence (or a list of tuples if more than one sequence).
    '''

    if 'verbose' in kwargs.keys():
        verbose = kwargs['verbose']
    else:
        verbose = True

    results = []
    timer = turntable.utils.Timer(nLoops=len(sequence), numPrints=15, verbose=verbose)
    for subject in sequence:
        results.append(function(subject, *args, **kwargs))
        timer.loop()
    timer.fin()
    return results


def batch(sequence, function, processes=None, batch_size=None, quiet=False,
          kwargs_to_dump=None, args=None, **kwargs):
    '''runs a process in series for batches where each batch is run parallel over the number of processes specified.
    Allows for aggregation and incremental storage and runs the in memory processes

    sequence is an array of car instances
    batch_size is the specified size of each batch. defaults to len(sequence)/processes
    processes is the number of processes to use
            Defaults to the number processes multiprocessing calculates up to a max of 20'''

    if processes is None:
        # default to the number of processes, not exceeding 20 or the number of
        # subjects
        processes = min(mp.cpu_count(), 20, len(sequence))

    if batch_size is None:
        # floor divide rounds down to nearest int
        batch_size = max(len(sequence) // processes, 1)
    print 'size of each batch =', batch_size

    mod = len(sequence) % processes
    # batch_list is a list of cars broken in to batch size chunks
    batch_list = [sequence[x:x + batch_size]
                  for x in xrange(0, len(sequence) - mod, batch_size)]
    # remainder handling
    if mod != 0:
        batch_list[len(batch_list) - 1] += sequence[-mod:]
    print 'number of batches =', len(batch_list)

    # #if the sequence is shorter than batch_size
    # #the system will run parallel to completion in one iteration
    # if batch_size >= len(sequence):
    # 	verbose = False
    # else:
    # 	verbose = (not quiet)

    # timer = turntable.utils.Timer(nLoops = len(batch_list), numPrints = len(batch_list), verbose = verbose)
    # #run the list of batches in series
    # tic = time.time()
    # returnList = []
    # for batch in batch_list:
    # 	#Process each batch in parallel
    # 	batch = thread(function = function, sequence = batch, processes = processes, runSeries = False, quiet = quiet)
    # 	[returnList.append(subject) for subject in batch]#bring all previously runs into a single list
    # 	timer.loop()

    # New args
    if args is None:
        args = function
    else:
        if isinstance(args, tuple) == False:
            args = (args,)
        args = (function,) + args

    # Applying the mp function w/ or w/o dumping using the custom operator
    # function
    if kwargs_to_dump is None:
        res = parallel(
            batch_list,
            new_function_batch,
            processes=processes,
            args=args,
            **kwargs)
    else:
        res = process_dump(
            batch_list,
            new_function_batch,
            kwargs_to_dump,
            processes=processes,
            args=args,
            **kwargs)

    returnList = []
    for l in res:
        returnList += l

    # toc = time.time()
    # elapsed = toc-tic
    # if quiet is False:
    # 	if processes is None:
    # 		print "Total Elapsed time: %s  :-)" % str(elapsed)
    # 	else:
    # print "Total Elapsed time: %s  on %s processes :-)" %
    # (str(elapsed),str(processes))

    return returnList



def new_function_batch(sequence, function, *args, **kwargs):

    proc_name = mp.current_process().name
    print proc_name + ' starts'
    print 'Processing ' + str(len(sequence)) + ' arguments'

    results = []
    timer = turntable.utils.Timer(nLoops=len(sequence), numPrints=10, verbose=False)
    for subject in sequence:
        results.append(function(subject, *args, **kwargs))
        timer.loop()
    timer.fin()
    # return results

    # proc_name = mp.current_process().name
    # print proc_name+' starts'
    # tic = time.time()
    # res = []
    # print 'Processing '+str(len(main_arg_l))+' arguments'
    # for main_arg in main_arg_l:
    # 	res.append(function(main_arg,*args,**kwargs))

    # print proc_name+' ends in '+str(time.time()-tic)
    return results


def thread(
        function, sequence, cores=None, runSeries=False, quiet=False):
    '''sets up the threadpool with map for parallel processing'''

    # Make the Pool of workes
    if cores is None:
        pool = ThreadPool()
    else:
        pool = ThreadPool(cores)

    # Operate on the list of subjects with the requested function
    # in the split threads
    tic = time.time()
    if runSeries is False:
        try:
            results = pool.map(function, sequence)
            # close the pool and wiat for teh work to finish
            pool.close()
            pool.join()
        except:
            print 'thread Failed... running in series :-('
            results = series(sequence, function)
    else:
        results = series(sequence, function)
    toc = time.time()
    elapsed = toc - tic

    if quiet is False:
        if cores is None:
            print "Elapsed time: %s  :-)" % str(elapsed)
        else:
            print "Elapsed time: %s  on %s threads :-)" % (str(elapsed), str(cores))
    # Noes:
    # import functools
    # abc = map(functools.partial(sb.dist, distName = 'weibull'), wbldfList)

    return results


def parallel(sequence, function, processes=None, args=None, **kwargs):

    if processes is None:
        # default to the number of cores, not exceeding 20
        processes = min(mp.cpu_count(), 20)
    print "Running parallel process on " + str(processes) + " cores. :-)"

    pool = mp.Pool(processes=processes)
    PROC = []
    tic = time.time()
    for main_arg in sequence:
        if args is None:
            ARGS = (main_arg,)
        else:
            if isinstance(args, tuple) == False:
                args = (args,)
            ARGS = (main_arg,) + args
        PROC.append(pool.apply_async(function, args=ARGS, kwds=kwargs))
    #RES = [p.get() for p in PROC]
    RES = []
    for p in PROC:
        try:
            RES.append(p.get())
        except Exception as e:
            print "shit happens..."
            print e
            RES.append(None)
    pool.close()
    pool.join()

    toc = time.time()
    elapsed = toc - tic
    print "Elapsed time: %s  on %s processes :-)" % (str(elapsed), str(processes))

    return RES


def new_function_dumping(
        args_to_load_names, function, main_arg, *args, **kwargs):

    for name in args_to_load_names:
        f_toread = open('./temp_pickle/' + name + '.pkl', 'r')
        kwargs[name] = pickle.load(f_toread)
        f_toread.close()
    if args is not None:
        res = function(main_arg, *args, **kwargs)
    else:
        res = function(main_arg, **kwargs)
    return res


def process_dump(
        sequence,
        function,
        kwargs_to_dump,
        processes=None,
        args=None,
        **kwargs):

    if processes is None:
        # default to the number of cores, not exceeding 20
        processes = min(mp.cpu_count(), 20)
    print "Running parallel process on " + str(processes) + " cores. :-)"

    tic = time.time()
    turntable.utils.create_dir('./temp_pickle/')
    for name, obj in kwargs_to_dump.iteritems():
        f_pkl = open('./temp_pickle/' + name + '.pkl', 'w+')
        pickle.dump(obj, f_pkl)
        f_pkl.close()
    args_to_load_names = kwargs_to_dump.keys()

    def arg_list(main_arg, args):
        if args is None:
            ARGS = (args_to_load_names, function, main_arg)
        else:
            if isinstance(args, tuple) == False:
                args = (args,)
            ARGS = (args_to_load_names, function, main_arg,) + args
        return ARGS

    pool = mp.Pool(processes=processes)
    PROC = []

    for main_arg in sequence:
        ARGS = arg_list(main_arg, args)
        PROC.append(
            pool.apply_async(new_function_dumping, args=ARGS, kwds=kwargs))

    #RES = [p.get() for p in PROC]
    RES = []
    for p in PROC:
        try:
            RES.append(p.get())
        except Exception as e:
            print "shit happens..."
            print e
            RES.append(None)
    print 'Closing processes...'
    pool.close()
    pool.join()

    if os.path.exists('./temp_pickle/'):
        shturntable.utils.rmtree('./temp_pickle/')

    toc = time.time()
    elapsed = toc - tic
    print "Elapsed time: %s on %s processes :-)" % (str(elapsed), str(processes))

    return RES
