"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random

from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.slavery.settings.setting_utils import SSSlaverySettingUtils
from sims.sim_info import SimInfo
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'ss_attempt_to_enslave_score')


class SSEnslaveAttemptSuccessChanceOperation:
    """ Use to calculate the chance of an abduction being successful."""

    @classmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=0)
    def calculate_success_chance(cls, sim_info: SimInfo, target_sim_info: SimInfo) -> int:
        """ Calculate the success chance of the Sim abducting the target. """
        log.debug('Calculating abduction attempt score.')
        min_chance = 0
        max_chance = 100
        # Successful interaction is 50 or above
        result = random.randint(min_chance, max_chance)
        log.format_with_message('Calculated Abduction score (Successful is a result above {})'.format(SSSlaverySettingUtils().main.get_chance_to_succeed()), result=result, min_chance_of_success=min_chance, max_chance_of_success=max_chance)
        return result
