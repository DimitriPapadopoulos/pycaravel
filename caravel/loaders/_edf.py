##########################################################################
# NSAp - Copyright (C) CEA, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module defines the edf dataset loader.
"""

# Third party import
import pyedflib

# Package import
from .loader_base import LoaderBase


class EDF(LoaderBase):
    """Define the mp4 loader."""

    allowed_extensions = [".edf"]

    def load(self, path):
        """A method that load the edf data.

        Parameters
        ----------
        path: str
            the path to the edf to be loaded.

        Returns
        -------
        data: pyedflib object
        """
        return pyedflib.EdfReader(path)

    def save(self, path, signals, signal_headers, header=None):
        """A method that save the image in edf."""
        pyedflib.highlevel.write_edf(
            path, signals=signals, signal_headers=signal_headers, header=header
        )
