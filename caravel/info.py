##########################################################################
# NSAp - Copyright (C) CEA, 2019 - 2024
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Module current version
version_major = 1
version_minor = 0
version_micro = 0

# Expected by setup.py: string of form "X.Y.Z"
__version__ = f"{version_major}.{version_minor}.{version_micro}"

# Expected by setup.py: the status of the project
CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Environment :: Console",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Scientific/Engineering",
]

# Project descriptions
description = """
pycaravel:  This module is designed to simplify continuous integration (CI) of
data from multiple projects.
"""
SUMMARY = """
.. container:: summary-carousel

    pycaravel is a Python module to simplify continuous integration (CI) of
    data from multiple projects:

    1. a common API for parsing multiple source of data (currently only BIDS).
    2. a common API to search in those datasets.
    3. a common API to validate incoming data.
"""
long_description = (
    "This module is designed to simplify continuous integration (CI) "
    "of data from multiple projects. "
)

# Main setup parameters
NAME = "pycaravel"
ORGANISATION = "CEA"
MAINTAINER = "Antoine Grigis"
MAINTAINER_EMAIL = "antoine.grigis@cea.fr"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
EXTRANAME = "NeuroSpin webPage"
EXTRAURL = "http://joliot.cea.fr/drf/joliot/Pages/Entites_de_recherche/NeuroSpin.aspx"
URL = "https://github.com/neurospin-cloud/pycaravel"
DOWNLOAD_URL = "https://github.com/neurospin-cloud/pycaravel"
LICENSE = "CeCILL-B"
CLASSIFIERS = CLASSIFIERS
AUTHOR = """
Antoine Grigis <antoine.grigis@cea.fr>
"""
AUTHOR_EMAIL = "antoine.grigis@cea.fr"
PLATFORMS = "Linux,OSX"
ISRELEASE = True
VERSION = __version__
PROVIDES = ["caravel"]
REQUIRES = [
    "pandas",
    "openpyxl",
    "grabbit @ git+https://github.com/grabbles/grabbit.git",
    "nibabel",
    "numpy",
    "imageio[ffmpeg]",
    "PyPDF2",
    "vcfpy",
    "pandas-plink",
    "pyEDFlib",
    "requests",
    "python-docx",
    "fire",
    "pymzml",
]
EXTRA_REQUIRES = {}
SCRIPTS = ["caravel/scripts/project-ci"]
