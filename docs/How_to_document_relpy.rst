How to document relpy
=====================

Here is a small summary of what you should do in order to properly add some content to this documentation.
It will start with the most basic actions (add a function in a module) to some more elaborated ones (add whole pages).

But first, let's have an overview of the basic things you should know about the documentation.

How relpy documentation works
-----------------------------

relpy documentation is built using Sphinx. Sphinx uses reSt format (reStructured text) so that each page of the documentation has a .rst file in the doc folder. 

The doc folder is located in relpy's main folder under "./docs". "./docs" contains all the main files and folders for the documentation.

Files:

* **conf.py**: python file which gives sphinx all the basic configuration options (main folder, name of the package, theme, etc...). You shouldn't need to modifiy this file, except to change the version and release number of the package ("version = ", "release = ").

* **make.py**: used to build the documentation. To build the html files, just type in the command **"python make.py html"**.

* **index.rst**: the main file/page of the documentation. This file generates "index.html" which is the home page of the html documentation.

* Other .rst files : other first level pages.

* Image files: images used in the html pages. 

Folders:

* **_build**: contains the "html" folder with all the html code generated. The html should always be generated under "./_build/html". The documentation home page can be then found at: **./docs/_buid/html/index.html**.

* **generated**: contains automatically generated .rst files. See `Document modules`_.

* **sphinxext**: contains extensions for the doc generation.

* **pyplots**: contains ".py" files with source code to generate plots (see the "plots" directive)

reSt syntax
-----------
Writing reSt docmentation pages is quite simple.
For a quick summary on how to write reSt files, I advise you to refer to this: http://sphinx-doc.org/rest.html
and this: http://docutils.sourceforge.net/docs/user/rst/quickref.html.

You can use the template below as a reference too.
Things you should know:

* All titles need to be underlined with a special character as shown. The underline must be at least the same length as the title.
* Titles of the same level must be underlined by the same character.
* You should leave blank lines between paragraphs.
* Special directives: used to give reSt special instructions. They can be of different types. Here is the right syntax (here the special directive is "special_directive")::

	.. special_directive:: something_optionnal
		:option:

		Content of the directive

* Lists are built this way::

	* item1 bullet list
	* item2 bullet list

	Or:

	1. item number 1
	2. item number 2

* You can add emphasis to words by surrounding them this way: \*words* \ (italic) or this way: \**words** \ (bold).

* You can even insert code lines using ">>>" or ipython lines that will be run with the special directive "ipython"

* Special directives :
	
	* "toctree" to insert a table of content. The main one is in index.rst
	* "plots" to insert plots. Source codes must be put in the "pyplots" folder.
	* "autosummary" to generate automatically ".rst" files for a bunch of functions (see: `Document functions`_)
	* "automodule" to generate automatically one ".rst" file to document a module (see: `Document modules`_)
	* "automodule" to generate automatically ".rst" files to document a class (see: `Document classes`_)
	* "currentmodule" to set the path for the current module to use (and to avoid writing it again each time)
	* "note" to write a note
	* "warning" to write a warning
	* "math" to write math using latex syntax
	* And others

.. note::

	When making references to other reSt files in a reSt file, never include the extension ".rst". For example, when inserting "file_1.rst" and "file_2.rst" in a toctree, do::

		.. toctree::

			file_1
			file_2

	If you also want to set a different name for the files in the table of content, do::

		.. toctree::

			Name of file 1 <file_1>
			Name of file 2 <file_2>


Template for a reSt file
------------------------
Here is an example of a ".rst" file. To see how this would render after generation, click here: :doc:`/_templates/generate_template`

::

	reSt example
	============

	Sub title 1
	-----------

	This is a paragraph.

	This is another paragraph.

	.. note::

	    And this is a note.

	If I want to insert a bullet list, I will do this:

	* **First item in bold**: this is a description of the first item
	* Second item: description

	I can also write math:

	.. math::

	    f(x) = G_{i+1}^{j+1} ( \sum_{k=1}^{n} e^{k ln(3x)} )

	Sub title 2
	-----------

	I can also insert some code if I want. There are different ways to do that.
	For example, using ">>>":

	>>> from scipy import stats
	>>> from relpy import statBox as sb
	>>> import numpy as np
	>>>
	>>> Xsample = np.random.randn(35)
	>>> distrib = sb.dist(X=Xsample)

	I can also use iPython directive, which will run the code, for example:

	.. ipython:: 

	    In [1]: x = 3

	    In [2]: y = x**2

	    In [3]: print(y)

	will generate an additional line in the doc under the code: "9"

Document functions
------------------
To document functions, classes and modules, we use the docstring extensions, which allows us to embed the documentation directly into the code comments. Please refer to this document: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt which gives the directives to write docstrings properly.

Here is a quick overview of what you could find there.

The docstring syntax is basically the same as the reSt syntax, but with more restrictions. Here is a template of a docstring function documentation.

.. warning::

	Be careful! Use exactly the same syntax. It won't work otherwise. For example, if you write "Parameter" instead of "Parameters", it won't be able to generate the doc. Same thing if you don't leave a space between the argument name and the semicolon: "arg1: type" instead of "arg1 : type".

::

	def function_name (arg1, arg2, arg3=default3, arg4=default4, ...):

		'''
		Quick description of the function (a few lines).

		Parameters
		----------
		arg1 : type
		    Description of the first parameter
		arg2 : type
		    Description of the second parameter
		arg3 : type (default is *default3*)
		    Description of the third parameter, what happens if default
		arg3 : type (default is *default4*)
		    Description of the fourth parameter, what happens if default
		...

		Other parameters
		----------------
		add_arg1 : type
		    Description of the first additionnal parameter
		add_arg2 : type
		    Description of the second additionnal parameter
		...

		Returns
		-------
		output1 : type
		    Description
		output2 : type
		    Description
		...

		Notes
		-----
		You can write some notes ("s" at the end of "notes" even if only one note!)

		Examples
		--------
		>>> value1 = 
		>>> value2 = 
		>>> res = function_name (value1, arg2=value2)

		'''

		Content of the function 


After writing the docstring, you need to insert the function documentation inside relpy documentation. To do that, you have different options:

* You can re-build the whole documentation using **"python make.py html"**. Doing this will automatically add the function inside "Modulelist.rst" and generate the doc and html.

* You can use **"python make.py add_functions"** which will just update the doc.

* Or you can do it manually by adding a line of code directly inside "Modulelist.rst".

For example, if you wrote a docstring for "fun4" which is in a module called "mod1", you need to find in "Modulelist.rst" the following section of code::

	relpy.mod1 module
	-----------------

	.. automodule:: relpy.mod1

	.. currentmodule:: relpy.mod1

	Content
	~~~~~~~

	.. autosummary:: 
	    :toctree: generated

	    fun1
	    fun2
	    fun3

Then, you need to add "fun4" under "fun3".
When you did, launch the command **"sphinx-autogen Modulelist.rst"** in the "docs" folder. It will generate a new file in the "generated" folder called "relpy.mod1.fun4.rst" containing the generated documentation for fun4. You can then build the documentation.


Document modules
----------------
To document modules, you first need to write a description of the module as a docstring within the code, just as you would do for functions. For module "mod1", at the very beginning of "mod1.py"::

	'''
	This is module mod1.
	Description bla bla bla...

	Examples
	~~~~~~~~
	[...]

	'''

	[content of the module]

Then, to insert the module in the doc:

* You can re-build the whole documentation using **"python make.py html"**. Doing this will automatically add the module inside "Modulelist.rst" and generate the doc and html.

* You can use **"python make.py add_modules"** which will just update the doc.

* Or you can do it manually by adding this part of code directly in "Modulelist.rst"::

	relpy.mod1 module
	-----------------

	.. automodule:: relpy.mod1

	.. currentmodule:: relpy.mod1

	Content
	~~~~~~~

	.. autosummary:: 
	    :toctree: generated

	    fun1
	    fun2
	    fun3
	    ...

where "fun1", "fun2"... are the module functions.
When you did, launch the command **"sphinx-autogen Modulelist.rst"** in the "docs" folder.

Document classes
----------------
First thing you need to do to write a class documentation is to insert the docstring in the code. The "Parameters" section lists the "__init__" function arguments. Use the following template::

	def class class1:

		'''

		Quick description of the class (a few lines).

		Parameters
		----------
		arg1 : type
		    Description of the first parameter
		arg2 : type
		    Description of the second parameter
		arg3 : type (default is *default3*)
		    Description of the third parameter, what happens if default
		arg3 : type (default is *default4*)
		    Description of the fourth parameter, what happens if default
		...

		Other parameters
		----------------
		add_arg1 : type
		    Description of the first additionnal parameter
		add_arg2 : type
		    Description of the second additionnal parameter
		...

		Attributes
		----------
		att1 : type
		    Description of the first parameter
		att2 : type
		    Description of the second parameter
		...

		Notes
		-----
		...

		Examples
		--------

		'''
		
		def _init__ (self, arg1, arg2, arg3=default3, arg4=default4, ...):
			[content]


		def method1 (...):
			'''
			[docstring]
			'''

		def method1 (...)
			'''
			[docstring]
			'''


Then, to insert the module in the doc:

* You can re-build the whole documentation using **"python make.py html"**. Doing this will automatically add the class inside "Modulelist.rst" and generate the doc and html.

* You can use **"python make.py add_classes"** which will just update the doc.

* Or you can do it manually by following these steps:
	* insert the class name in the "autosummary" directive of the module (and optionally some methods)
	* generate the files using "sphinx-autogen" command
	* go to the generated file for the class "generated/module.class1.rst"
	* Keep only the following lines::

		relpy.module.class1
		===================

		.. currentmodule:: relpy.module

		.. autoclass:: class1

	* Finally, we need to generate the methods doc files. To do that, use the command "sphinx-autogen generated/module.class1.rst"

Summary
-------

Automatic method to generate modules, functions, classes documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Write the docstring as explained
* Build using **"python make.py build"**

Manual method
~~~~~~~~~~~~~

1. Documenting a module

	* Insert a docstring at the beginning of the module file
	* In the "/docs" folder, choose a ".rst" file to write your module documentation ("Modulelist.rst" most likely) and insert an "automodule" directive at the right location.
	* Insert an "autosummary" directive with the names of all the functions and classes of the module to insert the functions and classes docstrings
	* Use the command "**sphinx-autogen name_of_the_file.rst**" (most likely "sphinx-autogen Modulelist.rst") to generate the doc files in "docs/generated"
	* Use the building command "**sphinx-build -b html ./ ./_build/html**" or "**make html**" to build the html files.

2. Documenting a class

	* Insert a docstring at the beginning of the class code
	* Document each method like you would do for a function
	* Insert the class name in the "autosummary" directive of its module (and optionally some methods)
	* Use the command "**sphinx-autogen name_of_the_file.rst**" (most likely "sphinx-autogen Modulelist.rst") to generate the doc files in "docs/generated"
	* Open the generated relpy.module_name.class_name and do the appropriate changes (as explained in `Document classes`_)
	* Use the building command "**sphinx-build -b html ./ ./_build/html**" or "**make html**" to build the html files.

3. Documenting a function
	* Insert a docstring at the beginning of the function code
	* Insert the function name in the "autosummary" directive of its module
	* Use the command "**sphinx-autogen name_of_the_file.rst**" (most likely "sphinx-autogen Modulelist.rst") to generate the doc files in "docs/generated"
	* Use the building command "**sphinx-build -b html ./ ./_build/html**" or "**make html**" to build the html files.

.. note::

	To delete a module, a class or a function, you also need to delete the generated files manually. 