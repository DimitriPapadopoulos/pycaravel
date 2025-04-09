##########################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module contains the generic parser definition.
"""

# Imports
import re
import warnings
from itertools import product
from string import Formatter

from caravel.parsers import BIDSParser

# Global parameters
# > define all the available parsers
PARSERS = [BIDSParser]


def get_parser(project, confdir, layoutdir):
    """Method to return the appropriate parser for your study.

    Parameters
    ----------
    project: str
        the name of the project you are working on.
    confdir: str
        the locations of the configuration file of the current project.
    layoutdir: str
        the location of the pre-generated parsing representations. If None
        switch to managers mode.

    Returns
    -------
    parser: obj
        the dataset appropriate parser.
    """
    for parser_class in PARSERS:
        parser = parser_class(project, confdir, layoutdir)
        if parser.can_load():
            return parser
    raise ValueError(f"No loader available for '{project}'.")


def listify(obj):
    """Wraps all non-list or tuple objects in a list."""
    return obj if isinstance(obj, (list, tuple, type(None))) else [obj]


def _expand_keys(entities):
    """Generate multiple replacement queries based on all combinations
    of values.

    Examples
    --------
    >>> entities = {'subject': ['01', '02'], 'session': ['1', '2'],
                    'task': ['rest', 'finger']}
    >>> out = _expand_entities(entities)
    >>> len(out)
    8
    >>> {'subject': '01', 'session': '1', 'task': 'rest'} in out
    True
    >>> {'subject': '02', 'session': '1', 'task': 'rest'} in out
    True
    >>> {'subject': '01', 'session': '2', 'task': 'rest'} in out
    True
    >>> {'subject': '02', 'session': '2', 'task': 'rest'} in out
    True
    >>> {'subject': '01', 'session': '1', 'task': 'finger'} in out
    True
    >>> {'subject': '02', 'session': '1', 'task': 'finger'} in out
    True
    >>> {'subject': '01', 'session': '2', 'task': 'finger'} in out
    True
    >>> {'subject': '02', 'session': '2', 'task': 'finger'} in out
    True
    """
    keys = list(entities.keys())
    values = list(product(*[entities[k] for k in keys]))
    return [dict(zip(keys, combs)) for combs in values]


_PATTERN_FIND = re.compile(r"({([\w\d]*?)(?:<([^>]+)>)?(?:\|((?:\.?[\w])+))?\})")


def build_path(keys, path_patterns, strict=False):
    """Constructs a path given a set of keys and a list of potential filename
    patterns to use.

    Parameters
    ----------
    keys: dict
        A dictionary mapping key names to key values.
        None key or empty-string key will be removed.
        Otherwise, kets will be cast to string values, therefore
        if any format is expected (e.g., zero-padded integers), the
        value should be formatted.
    path_patterns: str or list of str
        One or more filename patterns to write the file to.
        Keys should be represented by the name surrounded by curly braces.
        Optional portions of the patterns should be denoted by square brackets.
        Keys that require a specific value for the pattern to match can pass
        them inside angle brackets.
    strict: bool
        If True, all passed keys must be matched inside a pattern in order to
        be a valid match.
        If False, extra keys will be ignored so long as all mandatory keys are
        found.

    Returns
    -------
    path: str
        A constructed path for this file based on the provided patterns, or
        None if no path was built given the combination of keys and patterns.
    """
    path_patterns = listify(path_patterns)
    keys = {key: listify(val) for key, val in keys.items() if val or val == 0}

    # Loop over available patterns, return first one that matches all
    for pattern in path_patterns:
        keys_matched = list(_PATTERN_FIND.findall(pattern))
        defined = [elem[1] for elem in keys_matched]

        # If strict, all keys must be contained in the pattern
        if strict and set(keys.keys()) - set(defined):
            continue

        # Iterate through the provided path patterns
        new_path = pattern
        # Expand options within valid values and
        # check whether keys provided have acceptable value
        tmp_keys = keys.copy()
        for fmt, name, valid, defval in keys_matched:
            valid_expanded = valid.split("|")
            if valid_expanded and defval and defval not in valid_expanded:
                warnings.warn(
                    f"Pattern '{fmt}' is inconsistent as it defines "
                    "an invalid default value."
                )
            if (
                valid_expanded
                and name in keys
                and set(keys[name]) - set(valid_expanded)
            ):
                continue
            if defval and name not in tmp_keys:
                tmp_keys[name] = [defval]

            # At this point, valid & default values are checked &
            # set - simplify pattern
            new_path = new_path.replace(fmt, f"{{{name}}}")

        optional_patterns = re.findall(r"(\[.*?\])", new_path)
        # Optional patterns with selector are cast to mandatory or removed
        for op in optional_patterns:
            for ent_name in {
                k
                for k, v in keys.items()
                if (v is not None) and not (v[0] != v[0])  # noqa: SIM202 FIXME?
            }:
                if (f"{{{ent_name}}}") in op:
                    new_path = new_path.replace(op, op[1:-1])
                    continue

            # Surviving optional patterns are removed
            new_path = new_path.replace(op, "")
        # Replace keys
        fields = {
            pat[1]
            for pat in Formatter().parse(new_path)
            if pat[1] and not pat[1].isdigit()
        }
        if fields - set(tmp_keys.keys()):
            continue

        tmp_keys = {k: v for k, v in tmp_keys.items() if k in fields}
        new_path = [new_path.format(**e) for e in _expand_keys(tmp_keys)]
        if new_path:
            if len(new_path) == 1:
                new_path = new_path[0]
            return new_path

    return None
