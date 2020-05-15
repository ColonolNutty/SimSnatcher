"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.slavery.enums.statistic_ids import SSSlaveryStatisticId
from sims.sim_info import SimInfo
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'sss_attempt_to_enslave_score')


class SSEnslaveAttemptSuccessChanceOperation:
    """ Use to calculate the chance of an abduction being successful."""
    ENSLAVE_ATTEMPT_SUCCESS_THRESHOLD = 50

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=0)
    def calculate_success_chance(sim_info: SimInfo, target_sim_info: SimInfo) -> int:
        """ Calculate the success chance of the Sim abducting the target. """
        log.debug('Calculating abduction attempt score.')
        min_chance = 0
        max_chance = 100
        # Successful interaction is 50 or above
        result = max_chance
        log.format_with_message('Calculated Abduction score (Successful is a result above {})'.format(SSEnslaveAttemptSuccessChanceOperation.ENSLAVE_ATTEMPT_SUCCESS_THRESHOLD), result=result, min_chance_of_success=min_chance, max_chance_of_success=max_chance)
        return result

    @staticmethod
    def attempt_is_success(sim_info: SimInfo) -> bool:
        """ Determine if the abduction was successful. """
        return CommonSimStatisticUtils.get_statistic_value(sim_info, SSSlaveryStatisticId.ATTEMPT_TO_ENSLAVE_WAS_SUCCESS) == 1

    @staticmethod
    def attempt_is_failure(sim_info: SimInfo) -> bool:
        """ Determine if the abduction was a failure. """
        if not CommonSimStatisticUtils.has_statistic(sim_info, SSSlaveryStatisticId.ATTEMPT_TO_ENSLAVE_WAS_SUCCESS):
            return False
        return CommonSimStatisticUtils.get_statistic_value(sim_info, SSSlaveryStatisticId.ATTEMPT_TO_ENSLAVE_WAS_SUCCESS) != 1

    @staticmethod
    def remove_attempt_success_statistic(sim_info: SimInfo):
        """ Reset the abduction success statistic. """
        CommonSimStatisticUtils.remove_statistic(sim_info, SSSlaveryStatisticId.ATTEMPT_TO_ENSLAVE_WAS_SUCCESS)
