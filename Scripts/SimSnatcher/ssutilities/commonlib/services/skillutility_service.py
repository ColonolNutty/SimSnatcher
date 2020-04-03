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

from typing import Union, Any, Dict

from sims.sim_info import SimInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.sims.common_sim_skill_utils import CommonSimSkillUtils


class CommonSkillIncreaseReason(Int):
    """ Reasons for a skill to increase. """
    NONE = 0


class CommonSkillDecreaseReason(Int):
    """ Reasons for a skill to decrease. """
    NONE = 0


class CommonSkillUtilityService(CommonService):
    """ Manage experience gain/loss for the skill of a Sim. """
    @property
    def skill_identifier(self) -> int:
        """ Retrieve an identifier of the skill being managed. """
        raise NotImplementedError('\'{}\' not implemented.'.format(self.__class__.skill_identifier.__name__))

    @property
    def skill_commodity(self) -> int:
        """ Retrieve an identifier of the commodity of the skill being managed. """
        raise NotImplementedError('\'{}\' not implemented.'.format(self.__class__.skill_commodity.__name__))

    @property
    def skill_experience_modifiers(self) -> Dict[int, float]:
        """ Retrieve skill experience modifiers. """
        raise NotImplementedError('\'{}\' not implemented.'.format(self.__class__.skill_experience_modifiers.__name__))

    # noinspection PyUnusedLocal
    def get_skill_type(self, sim_info: SimInfo) -> int:
        """ Retrieve the type of skill being managed. """
        return self.skill_identifier

    # noinspection PyUnusedLocal
    def get_skill_commodity(self, sim_info: SimInfo) -> int:
        """ Retrieve the commodity of skill being managed. """
        return self.skill_commodity

    def get_skill_points_modifier(self, skill_increase_reason: Any) -> float:
        """ Retrieve skill point modifiers. """
        return self.skill_experience_modifiers.get(skill_increase_reason, 0.0)

    def remove_skill(self, sim_info: SimInfo) -> bool:
        """ Remove a skill from the sim. """
        return CommonSimSkillUtils.remove_skill(sim_info, self.skill_identifier)

    def set_skill_level(self, sim_info: SimInfo, level: Union[int, float]) -> bool:
        """ Set the skill level of the managed skill for the specified Sim. """
        return CommonSimSkillUtils.set_current_skill_level(sim_info, self.skill_identifier, level)

    def increase_skill(self, sim_info: SimInfo, amount: float=1.0, reason: CommonSkillIncreaseReason=CommonSkillIncreaseReason.NONE) -> bool:
        """ Increase the skill level of the managed skill for the specified Sim. """
        raise NotImplementedError

    def decrease_skill(self, sim_info: SimInfo, amount: float=1.0, reason: CommonSkillDecreaseReason=CommonSkillDecreaseReason.NONE) -> bool:
        """ Decrease the skill level of the managed skill for the specified Sim. """
        raise NotImplementedError

    def get_current_skill_level(self, sim_info: SimInfo) -> float:
        """ Get the current skill level of the managed skill for the specified Sim. """
        return CommonSimSkillUtils.get_current_skill_level(sim_info, self.skill_identifier)

    def get_skill_progress_toward_next_level(self, sim_info: SimInfo) -> float:
        """ Get the current progress towards the next level of the managed skill for the specified Sim. """
        return CommonSimSkillUtils.get_progress_toward_next_skill_level(sim_info, self.skill_identifier)

    def has_reached_max_skill_level(self, sim_info: SimInfo) -> bool:
        """ Determine if a Sim has reached the maximum level of the managed skill. """
        return CommonSimSkillUtils.is_at_max_skill_level(sim_info, self.skill_identifier)
