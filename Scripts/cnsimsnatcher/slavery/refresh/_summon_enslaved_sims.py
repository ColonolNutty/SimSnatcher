"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
from sims.sim_info import SimInfo
from sims.sim_spawner import SimSpawner
from sims4communitylib.classes.math.common_location import CommonLocation
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from zone import Zone


class _SSSlaverySummonSlaves(HasLog):
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
        return 'sss_summon_slaves'

    def _summon_slaves(self, zone: Zone, household_id: int) -> bool:
        self.log.debug('Attempting to summon slave Sims to active lot.')
        master_sim_info_list = self._get_masters()
        self.log.format_with_message('Found master Sims.', master_sims=CommonSimNameUtils.get_full_names(master_sim_info_list))
        for master_sim_info in master_sim_info_list:
            master_sim_name = CommonSimNameUtils.get_full_name(master_sim_info)
            self.log.debug('Attempting to auto summon slave Sims enslaved by \'{}\''.format(master_sim_name))
            if CommonLocationUtils.get_zone_id(zone) != CommonHouseholdUtils.get_household_home_zone_id(CommonHouseholdUtils.get_household(master_sim_info)):
                self.log.format_with_message('Failed, \'{}\' does not own the currently loaded household.'.format(master_sim_name), household_id=household_id, master_household_id=CommonHouseholdUtils.get_household_id(master_sim_info))
                continue
            self._summon_slaves_for(master_sim_info)
        self.log.debug('Done summoning slaves.')
        return True

    def _summon_slaves_for(self, master_sim_info: SimInfo) -> bool:
        master_sim_name = CommonSimNameUtils.get_full_name(master_sim_info)
        self.log.debug('Attempting to summon slaves for \'{}\'.'.format(master_sim_name))
        master_position = CommonSimLocationUtils.get_position(master_sim_info)
        master_location = CommonSimLocationUtils.get_location(master_sim_info)
        slave_sim_info_list = self._get_slaves(master_sim_info)
        self.log.format_with_message('Found slaves.', slaves=CommonSimNameUtils.get_full_names(slave_sim_info_list))
        for slave_sim_info in slave_sim_info_list:
            slave_sim_name = CommonSimNameUtils.get_full_name(slave_sim_info)
            self.log.debug('Checking if \'{}\' needs to be summoned.'.format(slave_sim_name))
            # If Sim has been summoned and they are on the current lot, ignore summoning them again.
            if CommonSimUtils.get_sim_instance(slave_sim_info) is not None:
                self.log.debug('\'{}\' has already been summoned, skipping the summoning of them.'.format(slave_sim_name))
                continue
            if CommonSimLocationUtils.is_on_current_lot(slave_sim_info):
                self.log.debug('\'{}\' is already on the current lot, skipping the summoning of them.'.format(slave_sim_name))
                continue
            if self._summon_slave(slave_sim_info, master_position, master_location):
                self.log.debug('Successfully summoned \'{}\' to the current lot.'.format(slave_sim_name))
            else:
                self.log.debug('Failed to summon \'{}\' to the current lot.'.format(slave_sim_name))

        self.log.debug('Done summoning slaves captured by \'{}\''.format(master_sim_name))
        return True

    def _summon_slave(self, slave_sim_info: SimInfo, position: CommonVector3, location: CommonLocation) -> bool:
        slave_sim_name = CommonSimNameUtils.get_full_name(slave_sim_info)
        try:
            self.log.format_with_message('Summoning Sim to the current lot.', sim=slave_sim_name)
            SimSpawner.spawn_sim(slave_sim_info, sim_position=position, sim_location=location)
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Problem occurred when attempting to summon \'{}\'.'.format(slave_sim_name), exception=ex)
        return False

    def _get_masters(self) -> Tuple[SimInfo]:
        return self._state_utils.get_all_masters(include_sim_callback=CommonHouseholdUtils.is_part_of_active_household, instanced_only=True)

    def _get_slaves(self, master_sim_info: SimInfo) -> Tuple[SimInfo]:
        return self._state_utils.get_slaves(master_sim_info, instanced_only=False)

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _summon_slaves_on_zone_load(event_data: S4CLZoneLateLoadEvent) -> bool:
        return _SSSlaverySummonSlaves()._summon_slaves(event_data.zone, event_data.household_id)
