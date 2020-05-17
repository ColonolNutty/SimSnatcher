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


class SSInteractionId(Int):
    """ Interaction identifiers used by SS. """
    # Settings
    SS_OPEN_SETTINGS = 17997355933418421807

    CONFIGURE_CAPTIVE_SLAVE = 1987689498033677476
    
    # Debug Interactions
    SS_DEBUG_LOG_ALL_INTERACTIONS = 14801299013239108791
