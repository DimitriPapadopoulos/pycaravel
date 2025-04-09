##########################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module defines the CSV dataset loader.
"""

# Third party import
from pandas_plink import read_plink1_bin

# Package import
from .loader_base import LoaderBase


class PLINK(LoaderBase):
    """Define the TSV loader."""

    allowed_extensions = [".bed"]

    def load(self, path):
        """A method that load the table data.

        Parameters
        ----------
        path: str
            the path to the table to be loaded.

        Returns
        -------
        data: xarray.core.dataarray.DataArray
            the loaded table.
        """
        data_array = read_plink1_bin(path, verbose=False)

        return data_array
