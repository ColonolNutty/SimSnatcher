"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # noinspection PyMissingOrEmptyDocstring
    class Int:
        pass


class SSSlaveryStringId(Int):
    """ LocalizedString identifiers used by SS Slavery. """
    # Settings
    SLAVERY_SETTINGS_NAME = 2064190208
    SLAVERY_SETTINGS_DESCRIPTION = 3874655210

    ENABLE_SLAVERY_INTERACTIONS_NAME = 329089025
    ENABLE_SLAVERY_INTERACTIONS_DESCRIPTION = 2425145540
