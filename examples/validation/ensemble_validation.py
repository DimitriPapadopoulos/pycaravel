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

import ensemble
from ensemble.validation import ValidationBase, get_validators

import caravel
from caravel.validation import run_validation

print(caravel.__version__)
print(caravel.info())

#############################################################################
# Load the validators
# -------------------
#
# First load the validators of the 'ensemble' project that only check the
# VIDEO data.

ValidationBase.__level__ = "debug"
ValidationBase.setup_logging()

validators = get_validators(family="video.*")
print(validators)


#############################################################################
# Apply validators
# ----------------
#
# Apply the loaded validators and generate a report.

datadir = "/neurospin/rlink/workspace/ci_toy/ensemble/ensemble-videoraw-upload"
projectdir = os.path.dirname(os.path.realpath(ensemble.__file__))
parser = caravel.get_parser(
    project="ensemble-videoraw",
    confdir=os.path.join(projectdir, "conf"),
    layoutdir=None,
)
parser.pickling_layout(bids_root=datadir, name="rawdata", outdir=datadir)
data = {
    "layoutdir": datadir,
    "confdir": os.path.join(projectdir, "conf"),
    "project": "ensemble-videoraw",
}
report = run_validation(data, validators=validators, logfile=None)
pprint(report)
