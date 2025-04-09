##########################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module defines the TARGZ dataset tester.
"""

# Third party import
import gzip

# Package import
from .loader_base import LoaderBase


class TARGZ(LoaderBase):
    """Define the TARGZ tester."""

    allowed_extensions = [
        ".tar.gz",
    ]

    def load(self, path):
        """A method that test a TARGZ file.

        Parameters
        ----------
        path: str
            the path to the TARGZ file.

        Returns
        -------
        data: object
            the loaded data.
        """
        with gzip.open(path, "rb") as open_file:
            for line in open_file:  # noqa: B007
                pass
