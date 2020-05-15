"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.abduction.utils.abduction_state_utils import SSAbductionStateUtils
from protocolbuffers.Math_pb2 import Vector3
from routing import Location
from sims.sim_info import SimInfo
from sims.sim_spawner import SimSpawner
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


class _SSAbductionSummonCaptives(HasLog):
    def __init__(self) -> None:
        super().__init__()
        self._state_utils = SSAbductionStateUtils()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ssa_summon_captives'

    def _summon_captives(self, zone: Zone, household_id: int) -> bool:
        self.log.debug('Attempting to summon captive Sims to active lot.')
        captor_sim_info_list = self._get_captors()
        self.log.format_with_message('Found captor Sims.', captor_sims=CommonSimNameUtils.get_full_names(captor_sim_info_list))
        for captor_sim_info in captor_sim_info_list:
            captor_sim_name = CommonSimNameUtils.get_full_name(captor_sim_info)
            self.log.debug('Attempting to summon captive Sims captured by \'{}\''.format(captor_sim_name))
            if CommonLocationUtils.get_zone_id(zone) != CommonHouseholdUtils.get_household_lot_id(captor_sim_info):
                self.log.format_with_message('Failed, \'{}\' does not own the currently loaded household.'.format(captor_sim_name), household_id=household_id, captor_household_id=CommonHouseholdUtils.get_household_id(captor_sim_info))
                continue
            self.log.debug('Attempting to locate captives for \'{}\'.'.format(captor_sim_name))
            captor_position = CommonSimLocationUtils.get_position(captor_sim_info)
            captor_location = CommonSimLocationUtils.get_location(captor_sim_info)
            captive_sim_info_list = self._get_captives(captor_sim_info)
            self.log.format_with_message('Found captives.', captives=CommonSimNameUtils.get_full_names(captive_sim_info_list))
            for captive_sim_info in captive_sim_info_list:
                captive_sim_name = CommonSimNameUtils.get_full_name(captive_sim_info)
                self.log.debug('Checking if \'{}\' needs to be summoned.'.format(captive_sim_name))
                # If Sim has been summoned and they are on the current lot, ignore summoning them again.
                if CommonSimUtils.get_sim_instance(captive_sim_info) is not None:
                    self.log.debug('\'{}\' has already been summoned, skipping the summoning of them.'.format(captive_sim_name))
                    continue
                if CommonSimLocationUtils.is_on_current_lot(captive_sim_info):
                    self.log.debug('\'{}\' is already on the current lot, skipping the summoning of them.'.format(captive_sim_name))
                    continue
                if self._summon_captive(captive_sim_info, captor_position, captor_location):
                    self.log.debug('Successfully summoned \'{}\' to the current lot.'.format(captive_sim_name))
                else:
                    self.log.debug('Failed to summon \'{}\' to the current lot.'.format(captive_sim_name))

            self.log.debug('Done summoning captives captured by \'{}\''.format(captor_sim_name))
        self.log.debug('Done summoning captives.')
        return True

    def _summon_captive(self, captive_sim_info: SimInfo, position: Vector3, location: Location) -> bool:
        captive_sim_name = CommonSimNameUtils.get_full_name(captive_sim_info)
        try:
            self.log.debug('Summoning \'{}\' to the current lot.'.format(captive_sim_name))
            SimSpawner.spawn_sim(captive_sim_info, sim_position=position, sim_location=location)
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Problem occurred when attempting to summon \'{}\'.'.format(captive_sim_name), exception=ex)
        return False

    def _get_captors(self) -> Tuple[SimInfo]:
        return self._state_utils.get_all_captors(include_sim_callback=CommonHouseholdUtils.is_part_of_active_household, instanced_only=True)

    def _get_captives(self, captor_sim_info: SimInfo) -> Tuple[SimInfo]:
        return self._state_utils.get_captives(captor_sim_info, instanced_only=False)

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _summon_captives_on_zone_load(event_data: S4CLZoneLateLoadEvent) -> bool:
        if not event_data.game_loaded:
            return False
        return _SSAbductionSummonCaptives()._summon_captives(event_data.zone, event_data.household_id)
