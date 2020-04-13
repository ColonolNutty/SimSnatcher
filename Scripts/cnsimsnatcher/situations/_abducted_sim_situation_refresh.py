"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from cnsimsnatcher.enums.interaction_identifiers import SSInteractionId
from cnsimsnatcher.enums.situation_identifiers import SSSituationId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.utils.abduction_state_utils import SSAbductionStateUtils
from sims.sim_info import SimInfo
from sims4communitylib.events.interval.common_interval_event_service import CommonIntervalEventRegistry
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from ssutilities.commonlib.utils.common_situation_utils import CommonSituationUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'ss_refresh_situation')


class _SSAbductionRefreshSituation:
    @staticmethod
    def _refresh_abducted_sim_situations(*_, **__) -> bool:

        def _should_refresh_sim(_sim_info: SimInfo) -> bool:
            return SSAbductionStateUtils.has_been_abducted(_sim_info)\
                   and not CommonSituationUtils.has_situation(_sim_info, SSSituationId.SS_ABDUCTION_PLAYER_ABDUCTED_NPC)\
                   and not CommonSimInteractionUtils.has_interaction_running_or_queued(_sim_info, SSInteractionId.SS_ABDUCTION_ATTEMPT_TO_ABDUCT_HUMAN_SUCCESS_OUTCOME)

        sims_needing_refresh = CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=_should_refresh_sim)
        for sim_info in sims_needing_refresh:
            log.format_with_message('Attempting to abduction status of sim.', sim=sim_info)
            result = _SSAbductionRefreshSituation.refresh_abduction_status_of_sim(sim_info)
            if result:
                log.debug('Successfully refreshed abduction status of sim.')
            else:
                log.debug('Failed to refresh abduction status of sim.')
        return True

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def refresh_abduction_status_of_sim(captive_sim_info: SimInfo) -> bool:
        """ Refresh the abduction status of a sim and reapply the abducted situation. """
        log.format_with_message('Attempting to refresh sim abduction status.', sim=captive_sim_info)
        sim_instance = CommonSimUtils.get_sim_instance(captive_sim_info)
        captor_sim_info = SSAbductionStateUtils.get_sim_info_of_captor(captive_sim_info)
        if sim_instance is None or captor_sim_info is None or not CommonSimUtils.get_sim_instance(captor_sim_info):
            log.debug('Failed, no captor found.')
            return False
        if not CommonHouseholdUtils.is_part_of_active_household(captor_sim_info):
            log.debug('Failed, the captor sim is not a part of the active household.')
            return False
        log.format_with_message('Refreshing abduction status of {}.'.format(CommonSimNameUtils.get_full_name(captive_sim_info)), captor=captor_sim_info)
        if CommonSimUtils.get_sim_instance(captor_sim_info) is None:
            if captor_sim_info is not None:
                SSAbductionStateUtils.clear_abduction_data(captor_sim_info)
            return False
        log.format_with_message('Captor found, refreshing abduction state.', captor_sim=captor_sim_info)
        return CommonSimInteractionUtils.queue_interaction(
            captor_sim_info,
            SSInteractionId.SS_ABDUCTION_ATTEMPT_TO_ABDUCT_HUMAN_SUCCESS_OUTCOME,
            target=sim_instance
        )


@CommonIntervalEventRegistry.run_every(ModInfo.get_identity())
def _ss_abduction_refresh_abducted_sim_situations_on_game_update(*_, **__) -> Any:
    return _SSAbductionRefreshSituation._refresh_abducted_sim_situations(*_, **__)
