##########################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module provides tools to check that all the dependencies are installed
properly.
"""

# Imports
from .info import __version__


def logo():
    """pySAP logo is ascii art using fender font.

    Returns
    -------
    logo: str
        the pysap logo.
    """
    logo = r"""
   _ __    _  _                                                     _
  | '_ \  | || |   __     __ _      _ _   __ _    __ __    ___     | |
  | .__/   \_, |  / _|   / _` |    | '_| / _` |   \ V /   / -_)    | |
  |_|__   _|__/   \__|_  \__,_|   _|_|_  \__,_|   _\_/_   \___|   _|_|
_|'''''|_| ''''|_|'''''|_|'''''|_|'''''|_|'''''|_|'''''|_|'''''|_|'''''|
'`-0-0-''`-0-0-''`-0-0-''`-0-0-''`-0-0-''`-0-0-''`-0-0-''`-0-0-''`-0-0-'
    """
    return logo


def info():
    """Display some useful information about the package.

    Returns
    -------
    info: str
        package information.
    """
    version = f"Package version: {__version__}\n\n"
    return logo() + "\n\n" + version
