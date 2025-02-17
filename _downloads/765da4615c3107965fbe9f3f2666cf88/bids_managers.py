"""
BIDS directory parsing (manager mode)
=====================================

Credit: A Grigis

pycaravel is a Python package that enables you to parse various source of data.
In this tutorial you will learn how to parse and search a BIDS directory, and
then create a representation of this parser. Using the described representation
will speed up the search for users.

First checks
------------

In order to test if pycaravel package is installed on your machine, you can
check the package version.
"""

import os
import caravel

print(caravel.__version__)
print(caravel.info())

#############################################################################
# Create a parser for your project
# --------------------------------
#
# The package provides a common interface to parse a BIDS directory. The
# parsing rules are defined by projects in the module, so we will need to
# specify the project name you are working on. For the moment it is not
# possible to specify these rules via the API. Set the layoutdir to None
# in order to switch to the managers mode.

cwdir = os.path.dirname(os.path.realpath(__file__))
parser = caravel.get_parser(
    project="hbn", confdir=os.path.join(cwdir, os.pardir, "conf"),
    layoutdir=None)

#############################################################################
# Create representation of your BIDS directory
# --------------------------------------------
#
# You will now parse your BIDS directory. As this step may be time consuming,
# the managers are in charge of creating a representation of the final
# parser that will be used during the user search steps. This can be done by
# using the following function, specifying the BIDS root directory and
# the subfolder name to be parsed (sourcedata, derivatives, phenotype, ...).
# This name must have a conresponding configuration file.

parser.pickling_layout(
    bids_root="/neurospin/psy/hbn",
    name="sourcedata",
    outdir=cwdir)
print(parser.list_keys("sourcedata"))
parser.pickling_layout(
    bids_root="/neurospin/psy/hbn/",
    name="derivatives",
    subset=["tbss_stats", "scalars"],
    outdir=cwdir)
print(parser.list_keys("derivatives"))
parser.pickling_layout(
    bids_root="/neurospin/psy/hbn",
    name="phenotype",
    outdir=cwdir)
print(parser.list_keys("phenotype"))
