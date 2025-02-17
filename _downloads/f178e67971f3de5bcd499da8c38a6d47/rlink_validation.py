"""
Validation
==========

Credit: A Grigis

pycaravel is a Python package that enables you to apply validators.
In this tutorial you will learn how to get and apply validators.

First checks
------------

In order to test if pycaravel package is installed on your machine, you can
check the package version.
"""

import os
from pprint import pprint

import rlink
from rlink.validation import get_validators

import caravel
from caravel.validation import run_validation

print(caravel.__version__)
print(caravel.info())

#############################################################################
# Load the validators
# -------------------
#
# First load the validators of the 'rlink' project that only check the
# MRI structure.

validators = get_validators(family="mri.structure")
print(validators)


#############################################################################
# Apply validators
# ----------------
#
# Apply the loaded validators and generate a report.

datadir = "/neurospin/rlink/workspace/ci_toy/rlink-mri-upload"
projectdir = os.path.dirname(os.path.realpath(rlink.__file__))
parser = caravel.get_parser(
    project="rlink-mri", confdir=os.path.join(projectdir, "conf"),
    layoutdir=None)
parser.pickling_layout(
    bids_root=datadir, name="sourcedata", outdir=datadir)
parser.pickling_layout(
    bids_root=datadir, name="rawdata", outdir=datadir)
data = {
    "layoutdir": datadir,
    "confdir": os.path.join(projectdir, "conf"),
    "project": "rlink-mri"}
report = run_validation(data, validators=validators, logfile=None)
pprint(report)
