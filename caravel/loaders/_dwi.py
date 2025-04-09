##########################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module defines the DWI bvec/bval dataset loader.
"""

# Third party import
import numpy as np

# Package import
from .loader_base import LoaderBase


class DWI(LoaderBase):
    """Define the DWI bvec bval loader."""

    allowed_extensions = [".bval", ".bvec"]

    def load(self, path):
        """A method that load a bvec/bvel file.

        Parameters
        ----------
        path: str
            the path to the bvec/bval file.

        Returns
        -------
        data: object
            the loaded data.
        """
        return np.loadtxt(path)

    def save(self, data, outpath):
        """A method that save the data in a bvec/bval file.

        Parameters
        ----------
        data: object
            the data to be saved.
        outpath: str
            the path where the the data will be saved.
        """
        np.savetxt(outpath, data)
