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

    # Buffs
    BEING_ENSLAVED = 826176732
    FROM_BEING_ENSLAVED = 3180962173

    # Misc
    SLAVERY = 1373141301

    # Tokens: {0.SimFirstName} {1.SimFirstName}
    SIM_HAS_ENSLAVED_SIM = 3867320780
    # Tokens: {0.SimFirstName} {1.SimFirstName}
    SIM_FAILED_TO_ENSLAVE_SIM = 2602441454
