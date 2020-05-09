"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.utils.abduction_state_utils import SSAbductionStateUtils
from protocolbuffers.Math_pb2 import Vector3
from routing import Location
from sims.sim_info import SimInfo
from sims.sim_spawner import SimSpawner
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from zone import Zone


class _SSAbductionSummonHostages(HasLog):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_abduction_summon_hostages'

    def _summon_hostages(self, zone: Zone, household_id: int) -> bool:
        self.log.debug('Attempting to summon hostage Sims to active lot.')
        captor_sim_info_list = self._get_captors()
        self.log.format_with_message('Found captor Sims.', captor_sims=CommonSimNameUtils.get_full_names(captor_sim_info_list))
        for captor_sim_info in captor_sim_info_list:
            captor_sim_name = CommonSimNameUtils.get_full_name(captor_sim_info)
            self.log.debug('Attempting to summon hostage Sims captured by \'{}\''.format(captor_sim_name))
            if CommonLocationUtils.get_zone_id(zone) != CommonHouseholdUtils.get_household_lot_id(captor_sim_info):
                self.log.format_with_message('Failed, \'{}\' does not own the currently loaded household.'.format(captor_sim_name), household_id=household_id, captor_household_id=CommonHouseholdUtils.get_household_id(captor_sim_info))
                continue
            self.log.debug('Attempting to locate hostages for \'{}\'.'.format(captor_sim_name))
            captor_position = CommonSimLocationUtils.get_position(captor_sim_info)
            captor_location = CommonSimLocationUtils.get_location(captor_sim_info)
            hostage_sim_info_list = self._get_hostages_of(captor_sim_info, instanced_only=False)
            self.log.format_with_message('Found hostages.', hostages=CommonSimNameUtils.get_full_names(hostage_sim_info_list))
            for hostage_sim_info in hostage_sim_info_list:
                hostage_sim_name = CommonSimNameUtils.get_full_name(hostage_sim_info)
                self.log.debug('Checking if \'{}\' needs to be summoned.'.format(hostage_sim_name))
                # If Sim has been summoned and they are on the current lot, ignore summoning them again.
                if CommonSimUtils.get_sim_instance(hostage_sim_info) is not None:
                    self.log.debug('\'{}\' has already been summoned, skipping the summoning of them.'.format(hostage_sim_name))
                    continue
                if CommonSimLocationUtils.is_on_current_lot(hostage_sim_info):
                    self.log.debug('\'{}\' is already on the current lot, skipping the summoning of them.'.format(hostage_sim_name))
                    continue
                if self._summon_hostage(hostage_sim_info, captor_position, captor_location):
                    self.log.debug('Successfully summoned \'{}\' to the current lot.'.format(hostage_sim_name))
                else:
                    self.log.debug('Failed to summon \'{}\' to the current lot.'.format(hostage_sim_name))

            self.log.debug('Done summoning hostages captured by \'{}\''.format(captor_sim_name))
        self.log.debug('Done summoning hostages.')
        return True

    def _summon_hostage(self, hostage_sim_info: SimInfo, position: Vector3, location: Location) -> bool:
        hostage_sim_name = CommonSimNameUtils.get_full_name(hostage_sim_info)
        try:
            self.log.debug('Summoning \'{}\' to the current lot.'.format(hostage_sim_name))
            SimSpawner.spawn_sim(hostage_sim_info, sim_position=position, sim_location=location)
            return True
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Problem occurred when attempting to summon \'{}\'.'.format(hostage_sim_name), exception=ex)
        return False

    def _get_captors(self) -> Tuple[SimInfo]:
        _has_hostages = CommonFunctionUtils.run_predicates_as_one(
            (
                CommonHouseholdUtils.is_part_of_active_household,
                CommonFunctionUtils.run_with_arguments(
                    SSAbductionStateUtils.has_abducted_sims,
                    instanced_only=False
                )
            )
        )
        return tuple(CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=_has_hostages))

    def _get_hostages_of(self, captor_sim_info: SimInfo, instanced_only: bool=False) -> Tuple[SimInfo]:
        return SSAbductionStateUtils.get_sim_info_list_of_hostages(captor_sim_info, instanced_only=instanced_only)

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _listen_for_summon_hostages_on_zone_load(event_data: S4CLZoneLateLoadEvent) -> bool:
        if not event_data.game_loaded:
            return False
        return _SSAbductionSummonHostages()._summon_hostages(event_data.zone, event_data.household_id)
