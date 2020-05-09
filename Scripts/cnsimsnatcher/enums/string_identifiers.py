"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.int_enum import CommonEnumIntBase


class SSStringId(CommonEnumIntBase):
    """ LocalizedString identifiers used by SS. """
    SIM_SNATCHER = 1121220694
    SS_CHEATS_NAME = 1575501605
    SS_CHEATS_DESCRIPTION = 2391887144

    # Abduction
    ABDUCTION = 2846876820
    ATTEMPT_TO_ABDUCTION_SIM = 3900732511
    FIGHT_OFF_ABDUCTOR = 2214457484
    SIM_SNATCHER_SETTINGS_NAME = 4184531491
    SIM_SNATCHER_SETTINGS_DESCRIPTION = 2980311872
    ABDUCTION_SETTINGS_NAME = 3591174281
    ABDUCTION_SETTINGS_DESCRIPTION = 3458631732
    ABDUCTION_INTERACTIONS_SWITCH_NAME = 2603904112
    ABDUCTION_INTERACTIONS_SWITCH_DESCRIPTION = 2011744203
    ABDUCTION_ALWAYS_SUCCESSFUL_SWITCH_NAME = 2420613639
    ABDUCTION_ALWAYS_SUCCESSFUL_SWITCH_DESCRIPTION = 951168703

    # Order To
    SHOW_DEBUG_INTERACTIONS_IN_PERFORM_INTERACTION_DIALOG_NAME = 3634664288
    SHOW_DEBUG_INTERACTIONS_IN_PERFORM_INTERACTION_DIALOG_DESCRIPTION = 3165453633

    # Abduction Buffs
    FROM_SUCCESSFUL_ABDUCTION = 3121336685
    FROM_FAILED_ABDUCTION = 2536085864
    ABDUCTION_FAILED_BUFF_NAME = 2470368147
    ABDUCTION_FAILED_BUFF_DESCRIPTION = 4110362632
    ABDUCTION_SUCCESS_BUFF_NAME = 4195708933
    ABDUCTION_SUCCESS_BUFF_DESCRIPTION = 3140996812
    ABDUCTION_DEFENSE_FAILED_BUFF_NAME = 1687626060
    FROM_BEING_ABDUCTED_FAILED = 3443180383
    ABDUCTION_DEFENSE_FAILED_DESCRIPTION = 1002134136
    ABDUCTION_DEFENSE_SUCCESS_BUFF_NAME = 4128798297
    FROM_BEING_ABDUCTED_SUCCESS = 3545292369
    ABDUCTION_DEFENSE_SUCCESS_BUFF_DESCRIPTION = 3136504656

    CANNOT_ABDUCT_A_SIM_THAT_IS_A_PART_OF_YOUR_HOUSEHOLD = 1619260374
    # Tokens: {0.SimFirstName}
    SIM_IS_ALREADY_A_HOSTAGE = 2654925971
    # Tokens: {0.SimFirstName}
    SIM_IS_NOT_BEING_HELD_HOSTAGE = 486918903
    CANNOT_ABDUCT_YOURSELF = 486508635

    # Tokens: {0.SimFirstName} {1.SimFirstName}
    SIM_HAS_ABDUCTED_SIM = 2417922355
    # Tokens: {0.SimFirstName} {1.SimFirstName}
    SIM_FAILED_TO_ABDUCT_SIM = 3245106485

    SS_ABDUCTION_NO_HOSTAGES = 2792437650
    SS_ABDUCTION_NO_HOSTAGES_FOUND_ON_ACTIVE_LOT = 1990335706
    SS_ABDUCTION_CHOOSE_A_SIM_FOR_ORDER = 3284646197
    # Tokens: {0.SimFirstName}
    SIM_WILL_CARRY_OUT_ORDER = 2099966338
    ORDER_ACCEPTED = 2012015682
    ORDER_REFUSED = 466113267
    SIM_REFUSED_TO_CARRY_OUT_ORDER = 3913276823
    SS_ABDUCTION_CHOOSE_INTERACTION = 1854482898
    SS_ABDUCTION_CHOOSE_INTERACTION_TO_PERFORM = 2092483933
    SS_ABDUCTION_NO_INTERACTIONS_FOUND = 896196871
    DISCLAIMER_NAME = 3865364704
    SS_ABDUCTION_DISCLAIMER = 285047481

    OBJECT_IS_IN_USE = 2127003382
    SS_ABDUCTION_HOSTAGES_ARE_NOW_ALLOWED_THERE = 3615443219

    SIM_RELEASED = 3527089551
    # Tokens: {0.SimFirstName} {0.SimLastName}
    SIM_HAS_BEEN_RELEASED_PLEASE_WAIT = 4083959082
