"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Tuple

from cnsimsnatcher.enums.skill_identifiers import SSSkillId
from cnsimsnatcher.enums.statistic_identifiers import SSStatisticId
from cnsimsnatcher.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.enums.skills_enum import CommonSkillId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'ss_attempt_to_abduct_score')


class SSAbductionSuccessChanceOperation:
    """ Use to calculate the chance of an abduction being successful."""
    ABDUCTION_SUCCESS_THRESHOLD = 50

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=0)
    def calculate_success_chance(sim_info: SimInfo, target_sim_info: SimInfo) -> int:
        """ Calculate the success chance of the Sim abducting the target. """
        log.debug('Calculating abduction attempt score.')
        min_chance = 0
        max_chance = 100
        modifier = 0
        # Sim skills
        min_chance += SSAbductionSuccessChanceOperation._calculate_skill_chance(sim_info, SSSkillId.SS_ABDUCTION)
        # Target skills
        max_chance -= SSAbductionSuccessChanceOperation._calculate_skill_chance(target_sim_info, SSSkillId.SS_ABDUCTION)

        min_fitness_chance, max_fitness_chance = SSAbductionSuccessChanceOperation._calculate_fitness_chance(sim_info, target_sim_info)
        min_chance += min_fitness_chance
        max_chance += max_fitness_chance
        min_chance = min_chance + modifier
        min_chance = max(0, min_chance)
        min_chance = min(100, min_chance)
        max_chance = max(0, max_chance)
        max_chance = min(100, max_chance)
        if min_chance > max_chance:
            min_chance = max_chance
        log.format(
            min_chance_of_success=min_chance,
            max_chance_of_success=max_chance,
            min_fitness_chance=min_fitness_chance,
            max_fitness_chance=max_fitness_chance
        )
        # Successful interaction is 50 or above
        result = random.randint(min_chance, max_chance)
        log.format_with_message('Calculated Abduction score (Successful is a result above {})'.format(SSAbductionSuccessChanceOperation.ABDUCTION_SUCCESS_THRESHOLD), result=result, min_chance_of_success=min_chance, max_chance_of_success=max_chance)
        return result

    @staticmethod
    def _calculate_fitness_chance(sim_info: SimInfo, target_sim_info: SimInfo) -> Tuple[int, int]:
        sim_fitness_level = CommonSimStatisticUtils.get_statistic_level(sim_info, CommonSkillId.FITNESS)
        target_fitness_level = CommonSimStatisticUtils.get_statistic_level(target_sim_info, CommonSkillId.FITNESS)
        min_chance = 0
        max_chance = 0
        log.format_with_message('Considering fitness levels', sim_fitness_level=sim_fitness_level, target_fitness_level=target_fitness_level)
        # Sim with 7 and Target with 3, will result in 40 min and 100 max, which is a 40% increase chance of interaction being successful, so essentially 90% chance of interaction success
        if sim_fitness_level > target_fitness_level:
            log.debug('The Sim has a higher fitness level than the target sim.')
            min_chance += (sim_fitness_level - target_fitness_level) * 10
        # Sim with 3 and Target with 7, will result in 0 min and 60 max, which is a 40% decrease chance of interaction being successful, so essentially 10% chance of interaction success
        if target_fitness_level > sim_fitness_level:
            log.debug('The Target Sim has a higher fitness level than the current sim.')
            max_chance -= (target_fitness_level - sim_fitness_level) * 10
        return min_chance, max_chance

    @staticmethod
    def _calculate_skill_chance(sim_info: SimInfo, skill_id: int) -> float:
        return 5.0 * CommonSimStatisticUtils.get_statistic_level(sim_info, skill_id)

    @staticmethod
    def abduction_is_successful(sim_info: SimInfo) -> bool:
        """ Determine if the abduction was successful. """
        return CommonSimStatisticUtils.get_statistic_value(sim_info, SSStatisticId.SS_ABDUCTION_COMMODITY_WAS_SUCCESS) == 1

    @staticmethod
    def abduction_is_failure(sim_info: SimInfo) -> bool:
        """ Determine if the abduction was a failure. """
        if not CommonSimStatisticUtils.has_statistic(sim_info, SSStatisticId.SS_ABDUCTION_COMMODITY_WAS_SUCCESS):
            return False
        return CommonSimStatisticUtils.get_statistic_value(sim_info, SSStatisticId.SS_ABDUCTION_COMMODITY_WAS_SUCCESS) != 1

    @staticmethod
    def remove_abduction_success_statistic(sim_info: SimInfo):
        """ Reset the abduction success statistic. """
        CommonSimStatisticUtils.remove_statistic(sim_info, SSStatisticId.SS_ABDUCTION_COMMODITY_WAS_SUCCESS)
