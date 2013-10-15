Resume Creator
==============

Installation
------------

Resume Creator requires :code:`xetex` (actually :code:`xelatex`) and Python 2.7
to run. It also requires LibreOffice to generate ODT files.

On Linux
^^^^^^^^

.. code:: sh
    sudo apt-get install texlive-xetex
    # setup virtualenv
    pip install -r requrements.txt

On Windows
^^^^^^^^^^

TODO


Usage
-----

The :sh:`./resume.py` file is the core piece of this setup. It takes an input
YAML file, and a `Cheetah <http://www.cheetahtemplate.org/>`_ template and produces an output file
based on the flags given to it.  There are sample files for producing LaTeX
output and reST output.

To get you started, I've included a sample YAML file
(:code:`resume-sample.yml`) which you can rename to :code:`resume.yml` and use
as your starting point.

Simple usage:

.. code:: sh
    # open, watch and build
    make go

    # make all the outputs
    make all


Customization:

For now, just run :sh:`./resume.py --help` to see what's available, and modify
:sh:`Makefile` to fit your needs.

TODO: write more about this

.. role:: sh(code)
   :language: sh


TODO
----

* Make odt and html work again
* Get rid of tables in html
* Use new odt interface (libreoffice 4)
* Better styling in odt
* More docs
