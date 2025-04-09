##########################################################################
# NSAp - Copyright (C) CEA, 2021
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module defines the PDF dataset loader.
"""

# Third party import
import PyPDF2

# Package import
from .loader_base import LoaderBase


class PDF(LoaderBase):
    """Define the PDF loader."""

    allowed_extensions = [".pdf"]

    def load(self, path):
        """A method that load the table data.

        Parameters
        ----------
        path: str
            the path to the table to be loaded.

        Returns
        -------
        data: object,
            the loaded table.
        """
        with open(path, "rb") as file:
            file_reader = PyPDF2.PdfReader(file)

        return file_reader
