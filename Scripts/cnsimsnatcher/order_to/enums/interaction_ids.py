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


class SSOrderToInteractionId(Int):
    """ Interaction identifiers used by SS. """
    # Order To
    GO_TO_RESIDENCE = 15042292361705398427
    GO_HERE = 13318307452569550283
    PERFORM_INTERACTION = 14836922745355247494
    COOK_FOOD_FRIDGE = 12313142238814703697
