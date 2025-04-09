##########################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module contains the BIDS parser definition.
"""

# Imports
import datetime
import os
import pickle

import numpy as np
import pandas as pd
from grabbit import Layout

from .parser_base import ParserBase


class BIDSParser(ParserBase):
    """Object to retrieve data from a BIDS directory."""

    BASE_ENTITIES = ["subject", "session", "task", "run", "suffix"]
    EXT = ".pkl"

    def export_layout(self, name):
        """Export a layout as a pandas DataFrame.

        Parameters
        ----------
        name: str
            the name of the layout.

        Returns
        -------
        df: pandas DataFrame
            the converted layout.
        """
        layout = self._load_layout(name)
        return layout.as_data_frame()

    def list_keys(self, name):
        """List all the filtering keys available in the layout.

        Parameters
        ----------
        name: str
            the name of the layout.

        Returns
        -------
        keys: list
            the layout keys.
        """
        layout = self._load_layout(name)
        return [elem.replace(f"{name}.", "") for elem in layout.entities]

    def list_values(self, name, key):
        """List all the filtering key values available in the layout.

        Parameters
        ----------
        name: str
            the name of the layout.
        key: str
            the name of key in the layout.

        Returns
        -------
        values: list
            the key associated values in the layout.
        """
        layout = self._load_layout(name)
        _key = f"{name}.{key}"
        if _key not in layout.entities:
            raise ValueError(f"Unrecognize layout key '{key}'.")
        return list(layout.unique(_key))

    def filter_layout(self, name, extension=None, **kwargs):
        """Filter the layout by using a combination of key-values rules.

        Parameters
        ----------
        name: str
            the name of the layout.
        extension: str or list of str
            a filtering rule on the file extension.
        kwargs: dict
            the filtering options.

        Returns
        -------
        df: pandas DataFrame
            the filtered layout.
        """
        layout = self._load_layout(name)
        if extension is not None:
            kwargs["extensions"] = extension
        header = None
        files = layout.get(**kwargs)
        if len(files) == 0:
            df = pd.DataFrame()
        else:
            file_obj = files[0]
            header = ["filename"] + self.list_keys(name)
            data = []
            for file_obj in files:
                row = [getattr(file_obj, key, np.nan) for key in header]
                data.append(row)
            df = pd.DataFrame(data, columns=header)
        df = df.dropna(axis="columns", how="all")
        return df

    def pickling_layout(self, bids_root, name, outdir, subset=None):
        """Load the requested BIDS layout and save it as a pickle.

        Parameters
        ----------
        bids_root: str
            path to the BIDS folder.
        name: str
            the name of subfolder to be parsed (the layout name).
        outdir: str
            the folder where the pickle will be generated.
        subset: list of str, default None
            a selector to focus only on specific folders.

        Returns
        -------
        outfile: str
            the generated layout representation location.
        """
        self._check_layout(name)
        self._check_conf(name)
        layout_root = os.path.join(bids_root, name)
        if not os.path.isdir(layout_root):
            raise ValueError(f"'{layout_root}' is not a valid directory.")
        if subset is None:
            layout = Layout([(layout_root, self.conf[name])])
        else:
            layout = Layout(
                [
                    (os.path.join(layout_root, dirname), self.conf[name])
                    for dirname in subset
                ]
            )
        self.layouts[name] = layout
        now = datetime.datetime.now()
        timestamp = f"{now.year}-{now.month}-{now.day}"
        outfile = os.path.join(outdir, f"{self.project}_{name}_{timestamp}.pkl")
        with open(outfile, "wb") as open_file:
            pickle.dump(layout, open_file, -1)
        return outfile
