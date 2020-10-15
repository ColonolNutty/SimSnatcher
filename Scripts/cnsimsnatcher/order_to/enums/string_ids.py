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


class SSOrderToStringId(Int):
    """ LocalizedString identifiers used by SS Order To. """
    # Settings
    ORDER_TO_SETTINGS_NAME = 545789941
    ORDER_TO_SETTINGS_DESCRIPTION = 2624333324

    # Orders
    SHOW_DEBUG_INTERACTIONS_IN_PERFORM_INTERACTION_DIALOG_NAME = 3634664288
    SHOW_DEBUG_INTERACTIONS_IN_PERFORM_INTERACTION_DIALOG_DESCRIPTION = 3165453633

    # Order Results
    ORDER_ACCEPTED = 2012015682
    # Tokens: {0.SimFirstName}
    SIM_WILL_CARRY_OUT_ORDER = 2099966338
    ORDER_REFUSED = 466113267
    # Tokens: {0.SimFirstName}
    SIM_REFUSED_TO_CARRY_OUT_ORDER = 3913276823

    # Dialog
    CHOOSE_A_SIM_FOR_ORDER = 3755011575
    CHOOSE_INTERACTION = 1854482898
    CHOOSE_INTERACTION_TO_PERFORM = 2092483933

    # Errors
    NO_INTERACTIONS_FOUND = 896196871
    NO_CAPTIVES_OR_SLAVES = 2792437650
    NO_CAPTIVES_OR_SLAVES_FOUND_ON_ACTIVE_LOT = 1990335706
    NO_CAPTIVES = 2792437650
    NO_CAPTIVES_FOUND_ON_ACTIVE_LOT = 1990335706
    NO_SLAVES = 2152185484
    NO_SLAVES_FOUND_ON_ACTIVE_LOT = 3143686684
    OBJECT_IS_IN_USE = 2127003382

    # Disclaimers
    ORDER_TO_DISCLAIMER_NAME = 3865364704
    ORDER_TO_DISCLAIMER_DESCRIPTION = 285047481
