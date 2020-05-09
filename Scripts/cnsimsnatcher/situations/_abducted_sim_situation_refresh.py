"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from cnsimsnatcher.enums.interaction_identifiers import SSInteractionId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.utils.abduction_state_utils import SSAbductionStateUtils
from sims.sim_info import SimInfo
from sims4communitylib.events.interval.common_interval_event_service import CommonIntervalEventRegistry
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'ss_refresh_situation')


class _SSAbductionRefreshSituation:
    @staticmethod
    def _refresh_abducted_sim_situations(*_, **__) -> bool:
        sims_needing_refresh = CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=SSAbductionStateUtils.has_invalid_abduction_state)
        for sim_info in sims_needing_refresh:
            log.format_with_message('Attempting to refresh abduction status of sim.', sim=sim_info)
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
        if sim_instance is None:
            return False
        captor_sim_info_list = SSAbductionStateUtils.get_captors(captive_sim_info, instanced_only=True)
        for captor_sim_info in captor_sim_info_list:
            if not CommonHouseholdUtils.is_part_of_active_household(captor_sim_info):
                log.debug('Failed, the captor sim is not a part of the active household.')
                continue
            log.debug('Refreshing abduction status of \'{}\' for their captor \'{}\'.'.format(CommonSimNameUtils.get_full_name(captive_sim_info), CommonSimNameUtils.get_full_name(captor_sim_info)))
            CommonSimInteractionUtils.queue_interaction(
                captor_sim_info,
                SSInteractionId.SS_ABDUCTION_ATTEMPT_TO_ABDUCT_HUMAN_SUCCESS_OUTCOME,
                target=sim_instance
            )
        return True


@CommonIntervalEventRegistry.run_every(ModInfo.get_identity())
def _ss_abduction_refresh_abducted_sim_situations_on_game_update(*_, **__) -> Any:
    return _SSAbductionRefreshSituation._refresh_abducted_sim_situations(*_, **__)
