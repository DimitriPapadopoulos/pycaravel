##########################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module defines the mzml dataset loader.
"""

# Third party import
import pymzml

# Package import
from .loader_base import LoaderBase


class MZML(LoaderBase):
    """Define the MZML loader."""

    allowed_extensions = [".mzML"]

    def load(self, path):
        """A method that load the table data.

        Parameters
        ----------
        path: str
            the path to the table to be loaded.

        Returns
        -------
        data: Ordered dict
            the loaded table.
        """

        return pymzml.run.Reader(path)
