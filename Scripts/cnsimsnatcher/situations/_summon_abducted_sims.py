"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.utils.abduction_state_utils import SSAbductionStateUtils
from sims.sim_spawner import SimSpawner
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'ss_abduction_summon_hostages')


class _SSAbductionSummonHostages:
    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _summon_hostages_on_zone_load(event_data: S4CLZoneLateLoadEvent) -> bool:
        log.debug('Attempting to summon sims.')
        _has_hostages = CommonFunctionUtils.run_predicates_as_one((CommonHouseholdUtils.is_part_of_active_household, CommonFunctionUtils.run_with_arguments(SSAbductionStateUtils.has_abducted_sims, instanced_only=False)))

        captor_sim_info_list = tuple(CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=_has_hostages))
        log.format_with_message('Found captor sims.', captor_sims=CommonSimNameUtils.get_full_names(captor_sim_info_list))
        for captor_sim_info in captor_sim_info_list:
            log.format_with_message('Attempting to locate hostages for Sim.', sim=CommonSimNameUtils.get_full_name(captor_sim_info))
            if CommonLocationUtils.get_zone_id(event_data.zone) != CommonHouseholdUtils.get_household_lot_id(captor_sim_info):
                log.format_with_message('Household was not correct.', household_id=event_data.household_id, captor_household_id=CommonHouseholdUtils.get_household_id(captor_sim_info))
                continue
            log.debug('Household is correct.')
            captor_position = CommonSimLocationUtils.get_position(captor_sim_info)
            captor_location = CommonSimLocationUtils.get_location(captor_sim_info)
            hostage_sim_info_list = SSAbductionStateUtils.get_sim_info_of_hostages(captor_sim_info, instanced_only=False)
            log.format_with_message('Found hostages.', hostages=CommonSimNameUtils.get_full_names(hostage_sim_info_list))
            for hostage_sim_info in hostage_sim_info_list:
                # If Sim has spawned and they are on the current lot, ignore spawning them.
                if CommonSimUtils.get_sim_instance(hostage_sim_info) is not None:
                    continue
                if CommonSimLocationUtils.is_on_current_lot(hostage_sim_info):
                    log.debug('Hostage is already on the current lot. \'{}\''.format(CommonSimNameUtils.get_full_name(hostage_sim_info)))
                    continue
                log.format_with_message('Spawning hostage.', sim=CommonSimNameUtils.get_full_name(hostage_sim_info))
                SimSpawner.spawn_sim(hostage_sim_info, sim_position=captor_position, sim_location=captor_location)
        log.debug('Done spawning hostages.')
        return True
