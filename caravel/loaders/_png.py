##########################################################################
# NSAp - Copyright (C) CEA, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module defines the png dataset loader.
"""

# Third party import
import imageio

# Package import
from .loader_base import LoaderBase


class PNG(LoaderBase):
    """Define the PNG loader."""

    allowed_extensions = [".png"]

    def load(self, path):
        """A method that load the png data.

        Parameters
        ----------
        path: str
            the path to the png file to be loaded.

        Returns
        -------
        data: imageio numpy array
            the loaded image.
        """
        return imageio.imread(path)

    def save(self, data, outpath):
        """A method that save the image in png.

        Parameters
        ----------
        data: imageio numpy array
            the image to be saved.
        outpath: str
            the path where the the png image will be saved.
        """
        imageio.imwrite(outpath, data)
