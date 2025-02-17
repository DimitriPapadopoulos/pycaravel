"""
BIDS directory parsing (user mode)
==================================

Credit: A Grigis

pycaravel is a Python package that enables you to parse various source of data.
In this tutorial you will learn how to parse and search in a BIDS directory.

First checks
------------

In order to test if pycaravel package is installed on your machine, you can
check the package version.
"""

import os
from pprint import pprint

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
# possible to specify these rules via the API.

cwdir = os.path.dirname(os.path.realpath(__file__))
parser = caravel.get_parser(
    project="hbn", confdir=os.path.join(cwdir, os.pardir, "conf"),
    layoutdir=cwdir)

#############################################################################
# You can now list the available configurations for your project, and the
# available layout representations pre-generated. Note that these
# representations are sorted by dates, and that the latest one will be used.

pprint(parser.conf)
pprint(parser.representation)

#############################################################################
# You can export the whole 'sourcedata' layout in a pandas DataFrame.

print(parser.export_layout("sourcedata"))

#############################################################################
# It is also possible to filter this dataset. You need first to list all the
# available filtering keys, then list all the available values for the
# filtering key(s) of interest, and finally filter your dataset.

print(parser.list_keys("sourcedata"))
print(parser.list_values("sourcedata", "subject"))
print(parser.list_values("sourcedata", "modality"))
search1 = parser.filter_layout("sourcedata", subject="NDARLU606ZDD",
                               modality="anat|func")
print(search1)
search2 = parser.filter_layout("sourcedata", extension="tsv")
print(search2)

#############################################################################
# Finally you may want to ask the system to load the filtered data. Only a
# couple of file extensions are supported. If no loader has been found the
# filename is returned
if not search1.empty:
    data1 = parser.load_data("sourcedata", search1)
    pprint(data1)
if not search2.empty:
    data2 = parser.load_data("sourcedata", search2)
    pprint(data2)

#############################################################################
# And for the derivatives
# -----------------------
#
# We can do the same for the derivatives


print(parser.export_layout("derivatives"))
print(parser.list_keys("derivatives"))
print(parser.list_values("derivatives", "process"))
search3 = parser.filter_layout("derivatives", subject="NDARAE199TDD",
                               process="scalars")
print(search3)
data3 = parser.load_data("derivatives", search3)
pprint(data3)
search3bis = parser.filter_layout("derivatives", process="tbss_stats",
                                  extension="tsv")
print(search3bis)
data3bis = parser.load_data("derivatives", search3bis)
pprint(data3bis)


#############################################################################
# And for the clinical data
# -------------------------
#
# We can do the same for the clinical data denoted in BIDS phenotype

print(parser.export_layout("phenotype"))
search4 = parser.filter_layout("phenotype", extension="tsv")
print(search4)
data4 = parser.load_data("phenotype", search4)
pprint(data4)
