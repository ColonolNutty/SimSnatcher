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


class SSSlaveryInteractionId(Int):
    """ Interaction identifiers used by SS Slavery. """

    # Attempt To Enslave
    SLAVERY_START = 1666915272075625784
    SLAVERY_END = 17836848419504865891
    TRIGGER_ATTEMPT_TO_ENSLAVE_HUMAN = 16657968019319956923
    ATTEMPT_TO_ENSLAVE_HUMAN = 7899283432188306464
    ATTEMPT_TO_ENSLAVE_HUMAN_SUCCESS_OUTCOME = 8861145126927277848
    ATTEMPT_TO_ENSLAVE_HUMAN_FAILURE_OUTCOME = 2873430086891705235

    # Debug
    CLEAR_SLAVERY_DATA = 1839805462840267879
