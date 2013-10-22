Resume Creator
==============

Installation
------------

Resume Creator requires `xetex` (actually `xelatex`), Python 2.7, and pandoc to run.

### On Linux

``` bash
sudo apt-get install texlive-xetex pandoc
pip install -r requrements.txt
```

### On Windows

TODO

Usage
-----

The `./resume.py` file is the core piece of this setup. It takes an input YAML file, and a [Jinja2](http://jinja.pocoo.org/docs/) template and produces an output file based on the flags given to it. There are sample files for producing LaTeX output and reST output.

To get you started, I've included a sample YAML file (`resume-sample.yml`) which you can rename to `resume.yml` and use as your starting point.

Simple usage:

``` bash
# open, watch and build
make go

# make all the outputs
make all
```

Customization:

For now, just run `./resume.py --help` to see what's available, and modify `Makefile` to fit your needs.

TODO: write more about this

TODO
----

-   Make odt and html work again
-   Get rid of tables in html
-   Use new odt interface (libreoffice 4)
-   Better styling in odt
-   More docs
