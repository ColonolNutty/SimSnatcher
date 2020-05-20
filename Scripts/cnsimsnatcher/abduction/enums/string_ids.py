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


class SSAbductionStringId(Int):
    """ LocalizedString identifiers used by SS Abduction. """
    # Abduction
    ABDUCTION = 2846876820

    # Interactions
    ATTEMPT_TO_ABDUCTION_SIM = 3900732511
    FIGHT_OFF_ABDUCTOR = 2214457484

    # Settings
    ABDUCTION_SETTINGS_NAME = 3591174281
    ABDUCTION_SETTINGS_DESCRIPTION = 3458631732
    ABDUCTION_INTERACTIONS_SWITCH_NAME = 2603904112
    ABDUCTION_INTERACTIONS_SWITCH_DESCRIPTION = 2011744203
    ABDUCTION_ALWAYS_SUCCESSFUL_SWITCH_NAME = 2420613639
    ABDUCTION_ALWAYS_SUCCESSFUL_SWITCH_DESCRIPTION = 951168703

    # Abduction Buffs
    FROM_SUCCESSFUL_ABDUCTION = 3121336685
    FROM_FAILED_ABDUCTION = 2536085864
    ABDUCTION_FAILED_BUFF_NAME = 2470368147
    ABDUCTION_FAILED_BUFF_DESCRIPTION = 4110362632
    ABDUCTION_SUCCESS_BUFF_NAME = 4195708933
    ABDUCTION_SUCCESS_BUFF_DESCRIPTION = 3140996812
    ABDUCTION_DEFENSE_FAILED_BUFF_NAME = 1687626060
    ABDUCTION_DEFENSE_FAILED_DESCRIPTION = 1002134136
    ABDUCTION_DEFENSE_SUCCESS_BUFF_NAME = 4128798297
    ABDUCTION_DEFENSE_SUCCESS_BUFF_DESCRIPTION = 3136504656
    FROM_BEING_ABDUCTED_SUCCESS = 3545292369
    FROM_BEING_ABDUCTED_FAILED = 3443180383

    CANNOT_ABDUCT_A_SIM_THAT_IS_A_PART_OF_YOUR_HOUSEHOLD = 1619260374
    # Tokens: {0.SimFirstName}
    SIM_IS_ALREADY_CAPTURED = 2654925971
    # Tokens: {0.SimFirstName}
    SIM_IS_NOT_BEING_HELD_CAPTIVE = 486918903
    CANNOT_ABDUCT_YOURSELF = 486508635

    # Tokens: {0.SimFirstName} {1.SimFirstName}
    SIM_HAS_ABDUCTED_SIM = 2417922355
    # Tokens: {0.SimFirstName} {1.SimFirstName}
    SIM_FAILED_TO_ABDUCT_SIM = 3245106485