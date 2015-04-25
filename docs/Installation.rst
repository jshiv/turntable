Installation
=============

Below are the instructions for 
 
 * :ref:`installing_on_mac`

 * :ref:`installing_on_windows`


Python version support
-----------------------

turntable requires Python 2.7.x. It is not tested to work with Python 3.x.


.. _installing_on_mac:

Installing on Mac 
------------------

We suggest to use Anaconda for your Python environment.

1. Installing Anaconda

Download and install Anaconda from: http://continuum.io/downloads

If you already have a python distribution installed, your system could get confused about which version to use. So you may want to uninstall any python verison you already have installed. 

If you already have Anaconda for Python 3.x you can switch anaconda distributions using the following::

	$ conda create -n py3k python=3 anaconda
	$ source activate py3k
See for reference: http://continuum.io/blog/anaconda-python-3	

If you have chosen not to Install Anaconda make sure you have pip installed on your system


2. Install using pip as follows::

	pip install turntable

4. Test the installation. You can test your turntable installation with the following commands in terminal::

	python
	>>> import turntable



.. _installing_on_windows:

Installing on Windows
--------------------

We suggest to use Anaconda for your Python environment.

1. Installing Anaconda

Download and install Anaconda from: http://continuum.io/downloads

If you already have a python distribution installed, your system could get confused about which version to use. So you may want to uninstall any python verison you already have installed. 

If you already have Anaconda for Python 3.x you can switch anaconda distributions using the following::

	$ conda create -n py3k python=3 anaconda
	$ source activate py3k
See for reference: http://continuum.io/blog/anaconda-python-3	

2. After you have installed Anaconda you should add the following entries to your path. In what follows, %HOME% is your home directory in Windows. If your username is carlo your home directory will be C:\\User\\carlo::

	%HOME%\AppData\Local\Continuum\Anaconda\Scripts; 

	%HOME%\AppData\Local\Continuum\Anaconda

3. Run easy_install in your shell::

	pip install turntable

4. Test the installation. You can test your turntable installation with the following commands in terminal::

	python
	>>> import turntable



Dependencies
-------------
All the dependencies are taken care of in the setup file.

For windows, .exe downloads of dependencies can be found at this link: http://www.lfd.uci.edu/~gohlke/pythonlibs/

The following packages are installed:


* pandas
