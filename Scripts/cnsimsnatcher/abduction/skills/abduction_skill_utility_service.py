"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict

from cnsimsnatcher.abduction.enums.skill_ids import SSAbductionSkillId
from cnsimsnatcher.abduction.enums.statistic_ids import SSAbductionStatisticId
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from sims.sim_info import SimInfo
from ssutilities.commonlib.services.skillutility_service import CommonSkillUtilityService, CommonSkillIncreaseReason, CommonSkillDecreaseReason
from sims4communitylib.utils.sims.common_mood_utils import CommonMoodUtils
from sims4communitylib.utils.sims.common_sim_skill_utils import CommonSimSkillUtils
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


class SSAbductionAbductionSkillIncreaseReason(CommonSkillIncreaseReason):
    """ Reasons for the Abduction Skill to increase. """
    ABDUCTING_A_SIM = 1
    CONFIDENCE_BONUS = 2
    SHAMELESS_BONUS = 3
    LONER_BONUS = 4


class SSAbductionAbductionSkillDecreaseReason(CommonSkillDecreaseReason):
    """ Reasons for the Abduction Skill to decrease. """
    GOT_CAUGHT = 5


class SSAbductionAbductionSkillUtilityService(CommonSkillUtilityService):
    """ A service used to manage experience gain/loss for the Abduction Skill of a Sim. """

    ABDUCTION_SKILL_EXP_MODIFIERS: Dict[int, float] = {
        SSAbductionAbductionSkillIncreaseReason.ABDUCTING_A_SIM: 6.7,
        SSAbductionAbductionSkillIncreaseReason.CONFIDENCE_BONUS: 0.1,
        SSAbductionAbductionSkillIncreaseReason.SHAMELESS_BONUS: 0.1,
        SSAbductionAbductionSkillIncreaseReason.LONER_BONUS: 0.1,
        SSAbductionAbductionSkillDecreaseReason.GOT_CAUGHT: 3.0
    }

    # noinspection PyMissingOrEmptyDocstring
    @property
    def skill_identifier(self) -> int:
        return SSAbductionSkillId.ABDUCTION

    # noinspection PyMissingOrEmptyDocstring
    @property
    def skill_commodity(self) -> int:
        return SSAbductionStatisticId.SKILL_ABDUCTION_LEVEL

    # noinspection PyMissingOrEmptyDocstring
    @property
    def skill_experience_modifiers(self) -> Dict[int, float]:
        return SSAbductionAbductionSkillUtilityService.ABDUCTION_SKILL_EXP_MODIFIERS

    # noinspection PyMissingOrEmptyDocstring
    def increase_skill(self, sim_info: SimInfo, amount: float=1.0, reason: int=SSAbductionAbductionSkillIncreaseReason.NONE) -> bool:
        if amount <= 0.0:
            return False
        if not SSSettingUtils().is_enabled_for_interactions(sim_info):
            return False
        if reason == SSAbductionAbductionSkillIncreaseReason.ABDUCTING_A_SIM:
            if CommonTraitUtils.is_shameless(sim_info):
                amount += self.get_skill_points_modifier(SSAbductionAbductionSkillIncreaseReason.SHAMELESS_BONUS)
            if CommonMoodUtils.is_confident(sim_info) or CommonTraitUtils.is_self_assured(sim_info):
                amount += self.get_skill_points_modifier(SSAbductionAbductionSkillIncreaseReason.CONFIDENCE_BONUS)
        elif CommonTraitUtils.is_loner(sim_info):
            amount += self.get_skill_points_modifier(SSAbductionAbductionSkillIncreaseReason.LONER_BONUS)
        skill_level = self.get_current_skill_level(sim_info)
        amount *= 1.1 - 0.1 * skill_level
        CommonSimSkillUtils.change_progress_toward_next_skill_level(sim_info, self.get_skill_type(sim_info), amount, add=True)
        result = CommonSimStatisticUtils.set_statistic_value(sim_info, self.get_skill_commodity(sim_info), self.get_current_skill_level(sim_info))
        return result

    # noinspection PyMissingOrEmptyDocstring
    def decrease_skill(self, sim_info: SimInfo, amount: float=1.0, reason: Any=CommonSkillDecreaseReason.NONE) -> bool:
        if amount <= 0.0:
            return False
        if not SSSettingUtils().is_enabled_for_interactions(sim_info):
            return False
        amount += self.get_skill_points_modifier(reason)
        CommonSimSkillUtils.change_progress_toward_next_skill_level(sim_info, self.get_skill_type(sim_info), -amount)
        return CommonSimStatisticUtils.set_statistic_value(sim_info, self.get_skill_commodity(sim_info), self.get_current_skill_level(sim_info))
