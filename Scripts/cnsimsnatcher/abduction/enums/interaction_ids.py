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


class SSAbductionInteractionId(Int):
    """ Interaction identifiers used by SS Abduction. """
    # Start/End
    START_ABDUCTION = 1405055796410444763
    TRIGGER_ATTEMPT_TO_ABDUCT_HUMAN_DEFAULT = 215148008884324789
    ATTEMPT_TO_ABDUCT_HUMAN_DEFAULT = 2400829702527701296
    ATTEMPT_TO_ABDUCT_HUMAN_FAILURE_OUTCOME = 8737107597856615939
    ATTEMPT_TO_ABDUCT_HUMAN_SUCCESS_OUTCOME = 11764291177810940936
    END_ABDUCTION = 11795441756578568704
    
    # Debug Interactions
    DEBUG_CLEAR_ABDUCTION_DATA = 5976813455778857347
