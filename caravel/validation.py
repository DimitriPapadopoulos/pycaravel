###############################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
###############################################################################


"""
This module provides a registry with function to be applied during
the validation stage.
"""

# Imports
import logging
import re
import traceback
import warnings
from collections import namedtuple
from operator import itemgetter

from .info import __version__

logger = logging.getLogger("caravel")


class MetaRegister(type):
    """Simple Python metaclass registry pattern."""

    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        """Allocation.

        Parameters
        ----------
        name: str
            the name of the class.
        bases: tuple
            the base classes.
        attrs:
            the attributes defined for the class.
        """
        new_cls = type.__new__(cls, name, bases, attrs)
        if name in cls.REGISTRY:
            raise ValueError(f"'{name}' name already used in registry.")
        if name != "ValidationBase":
            cls.REGISTRY[name] = new_cls
        return new_cls


class ValidationBase(metaclass=MetaRegister):
    """A validation test must inherit from this base class."""

    LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }
    __family__ = "default"
    __priority__ = 7
    __function__ = None
    __level__ = "error"

    def __init__(self):
        """Initialize the ValidationBase class."""
        ValidationBase.setup_logging()

    @classmethod
    def setup_logging(cls, logfile=None):
        """Setup the logging.

        Parameters
        ----------
        logfile: str, default None
            the log file.
        """
        logging_format = logging.Formatter(
            "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        while len(logging.root.handlers) > 0:
            logging.root.removeHandler(logging.root.handlers[-1])
        while len(logger.handlers) > 0:
            logger.removeHandler(logger.handlers[-1])
        level = cls.LEVELS.get(cls.__level__, None)
        if level is None:
            raise ValueError("Unknown logging level.")
        logger.setLevel(level)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(logging_format)
        logger.addHandler(stream_handler)
        if logfile is not None:
            file_handler = logging.FileHandler(logfile, mode="a")
            file_handler.setLevel(level)
            file_handler.setFormatter(logging_format)
            logger.addHandler(file_handler)
        if level != logging.DEBUG:
            warnings.simplefilter("ignore", DeprecationWarning)

    def __call__(self, data):
        """The method to run the test.

        Parameters
        ----------
        data: dict
            the input data for the test.
        """
        logger.info(
            f"running '{self.__function__.__name__}' "
            f"with version '{__version__}' of pycaravel"
        )
        return self.__function__(**data)


class ValidationDecorator:
    """Dynamically create a validator.

    In order to make the class publicly accessible, we assign the result of
    the function to a variable dynamically using globals().
    """

    def __init__(self, family="default", priority=7):
        """Initialize the ValidationDecorator class.

        Parameters
        ----------
        family: str, default 'default'
            the family name of the test.
        priority: int, default 7
            the prioprity run of the validation.
        """
        self.destination_module_globals = globals()
        self.family = family
        self.priority = priority

    def __call__(self, function, *args, **kwargs):
        """Create the validator.

        Parameters
        ----------
        function: callable
            the function that perform the test.
        """
        class_name = function.__name__.replace("_", " ").title().replace(" ", "")
        mod_name = self.destination_module_globals["__name__"]
        class_parameters = {
            "__module__": mod_name,
            "_id": mod_name + "." + class_name,
            "__function__": function,
            "__family__": self.family,
            "__priority__": self.priority,
        }
        self.destination_module_globals[class_name] = type(
            class_name, (ValidationBase,), class_parameters
        )


def get_validators(family=None):
    """List/sort all available validators.

    Parameters
    ----------
    family: str or list of str, default None
        the validators family name.

    Returns
    -------
    validators: dict
        the requested validators.
    """
    available_validators = sorted(ValidationBase.REGISTRY.keys())
    if family is not None and not isinstance(family, list):
        family = [family]
    validators = {}
    for key in available_validators:
        fct = ValidationBase.REGISTRY[key]
        if family is not None:
            for cnt, regex in enumerate(family):
                if re.match(regex, fct.__family__) is not None:
                    break
                cnt += 1
            if cnt == len(family):
                continue
        validators.setdefault(fct.__family__, []).append(fct())
    return validators


def listify(validators):
    """Sort the validators by priority level.

    Parameters
    ----------
    validators: dict
        the validators as returned by the 'get_validators' function.

    Returns
    -------
    sorted_validators: list
        the validators sorted by priority level.
    """
    Validator = namedtuple("Validator", "name priority instance")
    sorted_validators = []
    for key, instances in validators.items():
        sorted_validators.extend(
            [
                Validator(name=key, priority=instance.__priority__, instance=instance)
                for instance in instances
            ]
        )
    sorted_validators = sorted(
        sorted_validators, key=itemgetter(Validator._fields.index("priority"))
    )
    return sorted_validators


def run_validation(data, validators=None, logfile=None):
    """Safely run a validation plane.

    Parameters
    ----------
    data: dict
        the validation data.
    validators: dict, default None
        the validators as returned by the 'get_validators' function.
    logfile: str, default None
        the log file.

    Returns
    -------
    report: dict
        the validation report.
    """
    ValidationBase.setup_logging(logfile=logfile)
    if validators is None:
        validators = get_validators()
    report = {}
    for validator in listify(validators):
        if validator.name not in report:
            report[validator.name] = {}
        try:
            result, extra_data = validator.instance(data)
            if isinstance(extra_data, dict):
                logger.info(f"adding extra kwargs '{extra_data.keys()}'")
                data.update(extra_data)
        except Exception:
            result = {"Internal error:": [traceback.format_exc()]}
        if result is None or result == {} or result == []:
            continue
        report[validator.name][validator.instance.__class__.__name__] = result
    return report
