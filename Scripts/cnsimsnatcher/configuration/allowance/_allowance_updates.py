"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.modinfo import ModInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from cnsimsnatcher.configuration.allowance.utils.allowance_utils import SSAllowanceUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class _SSAllowanceUpdates:
    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _ss_update_allowance_on_zone_load(event_data: S4CLZoneLateLoadEvent) -> bool:
        if not event_data.game_loaded:
            return False
        allowance_utils = SSAllowanceUtils()
        for sim_info in CommonSimUtils.get_instanced_sim_info_for_all_sims_generator():
            allowance_utils.update_appropriateness_tags(sim_info)
