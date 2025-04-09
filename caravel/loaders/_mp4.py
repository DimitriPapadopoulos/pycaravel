##########################################################################
# NSAp - Copyright (C) CEA, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module defines the mp4 dataset loader.
"""

# Third party import
import imageio

# Package import
from .loader_base import LoaderBase


class MP4(LoaderBase):
    """Define the mp4 loader."""

    allowed_extensions = [".mp4"]

    def load(self, path):
        """A method that load the mp4 data.

        Parameters
        ----------
        path: str
            the path to the mp4 file to be loaded.

        Returns
        -------
        data: imageio numpy array
            the loaded image.
        """
        return imageio.get_reader(path, "ffmpeg")

    def save(self, data, outpath, fps=24):
        """A method that save the image in mp4.

        Parameters
        ----------
        data: list of path
            list of path for each image for the video.
        outpath: str
            the path where the the mp4 image will be saved.
        """

        writer = imageio.get_writer(outpath, fps)
        for png_path in data:
            im = (imageio.imread(png_path),)
            writer.append_data(im[:, :, 1])
        writer.close()
