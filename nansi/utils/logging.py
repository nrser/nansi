"""Utility functions to setup logging."""

from typing import Iterable, Union

import splatlog as logging
from ansible.utils.display import Display

from nansi.constants import ROOT_LOGGER_NAMES
from nansi.utils.collections import each


def level_from_display() -> logging.TLevel:
    """
    Convert the `ansible.utils.display.Display.verbosity` instance attribute to
    a log level.

    The `verbosity` attribute is set by the `-vv` flag(s) provided to
    the `ansible-playbook` command.

    flag        | verbosity | log level
    ----------- | --------- | ---------
    None        | 0         | `logging.WARNING`
    `-v`        | 1         | `logging.INFO`
    `-vv`       | 2         | `logging.DEBUG`
    `-vvv...`   | >= 3      | `logging.DEBUG`

    """
    display = Display()
    if display.verbosity > 1:
        return logging.DEBUG
    if display.verbosity > 0:
        return logging.INFO
    return logging.WARNING


def setup_for_display(
    module_names: Union[None, str, Iterable[str]] = None
) -> None:
    """
    Setup logging for all `nansi.constants.ROOT_LOGGER_NAMES`, as well as any
    name(s) provided as `module_names`, using the `verbosity` attribute of
    `ansible.utils.display.Display` to set the log level.

    ## See Also

    -   `nansi.constants.ROOT_LOGGER_NAMES`
    -   `level_from_display()`

    """
    logging.setup(
        module_names=(*ROOT_LOGGER_NAMES, *each(str, module_names)),
        level=level_from_display(),
    )
