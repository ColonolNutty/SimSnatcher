"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.operations.abduction_score import SSAbductionSuccessChanceOperation
from cnsimsnatcher.utils.abduction_state_utils import SSAbductionStateUtils
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'ss_start_abduction')


class SSAbductionAttemptToAbductSuccessInteraction(CommonImmediateSuperInteraction):
    """ Handles the success outcome of an attempt to abduct. """

    # noinspection PyMissingOrEmptyDocstring
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        log.debug('Abduction Attempt was Successful!')
        # The one abducting.
        captor_sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        # The one being abducted.
        captive_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        SSAbductionStateUtils.add_abduction_data(captor_sim_info, captive_sim_info)
        SSAbductionSuccessChanceOperation.remove_abduction_success_statistic(captor_sim_info)
        SSAbductionSuccessChanceOperation.remove_abduction_success_statistic(captive_sim_info)
        return True


class SSAbductionAttemptToAbductFailureInteraction(CommonImmediateSuperInteraction):
    """ Handles the failure outcome of an attempt to abduct. """

    # noinspection PyMissingOrEmptyDocstring
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        log.debug('Abduction Attempt Failed!')
        # TODO: Add more logic surrounding a failed abduction attempt. Call cops, reduce Fame, etc.
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        SSAbductionSuccessChanceOperation.remove_abduction_success_statistic(sim_info)
        SSAbductionSuccessChanceOperation.remove_abduction_success_statistic(target_sim_info)
        log.debug('Finished failing abduction.')
        return True
