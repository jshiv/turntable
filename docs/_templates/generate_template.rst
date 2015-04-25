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