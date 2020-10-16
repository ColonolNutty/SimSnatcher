"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Set

from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.persistence.ss_sim_data_storage import SSSimDataStore
from distributor.shared_messages import IconInfoData
from objects.components.buff_component import BuffComponent
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.interaction.events.interaction_queued import S4CLInteractionQueuedEvent
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'ss_allowance_injection')


class _SSVanillaBuffComponent:
    @staticmethod
    def _is_appropriate(original_self: BuffComponent, tags: Set[CommonGameTag]) -> bool:
        if not tags:
            return True
        owning_sim_info = CommonSimUtils.get_sim_info(original_self.owner)
        if owning_sim_info is None:
            return True
        sim_data = SSSimDataStore(owning_sim_info)
        if not sim_data.is_captive and not sim_data.is_slave:
            return True
        log.format_with_message('Checking if Sim is allowed.', sim=CommonSimNameUtils.get_full_name(owning_sim_info))
        allowed = True
        if not sim_data.allowances:
            allowed = False
        else:
            for tag in tags:
                if tag not in sim_data.allowances:
                    allowed = False
                    break
        if not allowed:
            log.format_with_message('Not allowed.', allowance_tags=sim_data.allowances, tags=tags)
            return False
        log.format_with_message('Allowed.', allowance_tags=sim_data.allowances, tags=tags)
        return True


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), BuffComponent, BuffComponent.is_appropriate.__name__)
def _ss_allowances_get_appropriateness(original, self, tags: Set[CommonGameTag]) -> bool:
    return _SSVanillaBuffComponent._is_appropriate(self, tags) and original(self, tags)


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _ss_prevent_non_allowed_interactions(event_data: S4CLInteractionQueuedEvent) -> bool:
    interaction = event_data.interaction
    tags = interaction.appropriateness_tags
    if not tags:
        return True
    owning_sim_info = CommonSimUtils.get_sim_info(interaction.sim)
    if owning_sim_info is None:
        return True
    sim_data = SSSimDataStore(owning_sim_info)
    if not sim_data.is_captive and not sim_data.is_slave:
        return True
    log.format_with_message('Checking if Sim is allowed.', sim=CommonSimNameUtils.get_full_name(owning_sim_info))
    allowed = True
    if not sim_data.allowances:
        allowed = False
    else:
        for tag in tags:
            if tag not in sim_data.allowances:
                allowed = False
                break
    if not allowed:
        log.format_with_message('Not allowed.', allowance_tags=sim_data.allowances, tags=tags)
        if owning_sim_info is CommonSimUtils.get_active_sim_info() and interaction.is_user_directed and not interaction.is_autonomous and not interaction.is_autonomous_picker_interaction:
            CommonBasicNotification(
                'Not Allowed',
                'Your Master has forbidden that type of interaction.',
            ).show(icon=IconInfoData(obj_instance=owning_sim_info))
        return False
    log.format_with_message('Allowed.', allowance_tags=sim_data.allowances, tags=tags)
    return True
