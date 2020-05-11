"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.abduction.operations.abduction_score import SSAbductionSuccessChanceOperation
from cnsimsnatcher.abduction.utils.abduction_state_utils import SSAbductionStateUtils
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class SSAbductionAttemptToAbductSuccessInteraction(CommonImmediateSuperInteraction):
    """ Handles the success outcome of an attempt to abduct. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ssa_start_abduction'

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.debug('Abduction Attempt was Successful!')
        # The one abducting.
        captor_sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        # The one being abducted.
        captive_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        result, reason = SSAbductionStateUtils().create_captive(captive_sim_info, captor_sim_info)
        if not result:
            self.log.debug(reason)
        SSAbductionSuccessChanceOperation.remove_abduction_success_statistic(captor_sim_info)
        SSAbductionSuccessChanceOperation.remove_abduction_success_statistic(captive_sim_info)
        self.log.debug('Finished succeeding abduction.')
        return True


class SSAbductionAttemptToAbductFailureInteraction(CommonImmediateSuperInteraction):
    """ Handles the failure outcome of an attempt to abduct. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ssa_start_abduction'

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.debug('Abduction Attempt Failed!')
        # TODO: Add more logic surrounding a failed abduction attempt. Call cops, reduce Fame, etc.
        # The one abducting.
        captor_sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        # The one being abducted.
        captive_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        SSAbductionSuccessChanceOperation.remove_abduction_success_statistic(captor_sim_info)
        SSAbductionSuccessChanceOperation.remove_abduction_success_statistic(captive_sim_info)
        self.log.debug('Finished failing abduction.')
        return True
