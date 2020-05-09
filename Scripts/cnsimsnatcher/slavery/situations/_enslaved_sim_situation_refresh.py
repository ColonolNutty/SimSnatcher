"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.slavery.enums.interaction_ids import SSSlaveryInteractionId
from cnsimsnatcher.slavery.utils.slave_state_utils import SSSlaveryStateUtils
from sims.sim_info import SimInfo
from sims4communitylib.events.interval.common_interval_event_service import CommonIntervalEventRegistry
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class _SSSlaveryRefreshSituation(CommonService, HasLog):
    def __init__(self) -> None:
        super().__init__()
        self._state_utils = SSSlaveryStateUtils()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'sss_refresh_situation'

    def _refresh_sim_situations(self, *_, **__) -> bool:
        sims_needing_refresh = CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=self._state_utils.has_invalid_enslaved_state)
        for sim_info in sims_needing_refresh:
            self.log.format_with_message('Attempting to refresh enslaved status of sim.', sim=sim_info)
            result = self.refresh_enslaved_status_of_sim(sim_info)
            if result:
                self.log.debug('Successfully refreshed enslaved status of sim.')
            else:
                self.log.debug('Failed to refresh enslaved status of sim.')
        return True

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def refresh_enslaved_status_of_sim(self, slave_sim_info: SimInfo) -> bool:
        """ Refresh the abduction status of a sim and reapply the abducted situation. """
        slave_sim_name = CommonSimNameUtils.get_full_name(slave_sim_info)
        try:
            self.log.format_with_message('Attempting to refresh enslaved status of \'{}\'.'.format(slave_sim_name))
            sim_instance = CommonSimUtils.get_sim_instance(slave_sim_info)
            if sim_instance is None:
                self.log.debug('Failed, \'{}\' has not been summoned.'.format(slave_sim_name))
                return False
            master_sim_info_list = self._state_utils.get_masters(slave_sim_info)
            if not master_sim_info_list:
                self.log.debug('Failed, no masters found.')
                return False
            master_sim_info_list = self._state_utils.get_masters(slave_sim_info, instanced_only=True)
            for master_sim_info in master_sim_info_list:
                if not CommonHouseholdUtils.is_part_of_active_household(master_sim_info):
                    self.log.debug('Failed, the Master sim is not a part of the active household.')
                    continue
                self.log.debug('Refreshing the enslaved status of \'{}\' with their Master \'{}\'.'.format(CommonSimNameUtils.get_full_name(slave_sim_info), CommonSimNameUtils.get_full_name(master_sim_info)))
                CommonSimInteractionUtils.queue_interaction(
                    master_sim_info,
                    SSSlaveryInteractionId.ATTEMPT_TO_ENSLAVE_HUMAN_SUCCESS_OUTCOME,
                    target=sim_instance
                )
            self.log.debug('Done refreshing enslaved status.')
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'A problem occurred while attempting to refresh enslaved status of \'{}\''.format(slave_sim_name), exception=ex)


@CommonIntervalEventRegistry.run_every(ModInfo.get_identity())
def _ss_slavery_refresh_enslaved_sim_situations_on_game_update(*_, **__) -> Any:
    return _SSSlaveryRefreshSituation()._refresh_sim_situations(*_, **__)
