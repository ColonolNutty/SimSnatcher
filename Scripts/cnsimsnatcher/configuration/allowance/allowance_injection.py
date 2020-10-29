"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.bindings.enums.binding_body_location import SSBindingBodyLocation
from cnsimsnatcher.bindings.enums.body_side import SSBodySide
from cnsimsnatcher.enums.string_ids import SSStringId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.persistence.ss_sim_data import SSSimData
from distributor.shared_messages import IconInfoData
from interactions.base.interaction import Interaction
from sims.sim_info import SimInfo
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.interaction.events.interaction_queued import S4CLInteractionQueuedEvent
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_state_utils import CommonSimStateUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'ss_allowance_injection')


class _SSInteractionAllowance:
    _ALLOWANCES_PREVENTED_BY_LOCATION = {
        SSBindingBodyLocation.EYES.name: {
            SSBodySide.BOTH: (
                CommonGameTag.APPROPRIATENESS_READ_BOOKS,
                CommonGameTag.APPROPRIATENESS_TV_WATCHING,
                CommonGameTag.APPROPRIATENESS_VIEW,
                CommonGameTag.APPROPRIATENESS_CLEANING,
                CommonGameTag.APPROPRIATENESS_CAKE,
                CommonGameTag.APPROPRIATENESS_COOKING,
                CommonGameTag.APPROPRIATENESS_PHONE_GAME,
                CommonGameTag.APPROPRIATENESS_PHONE,
                CommonGameTag.APPROPRIATENESS_COMPUTER,
                CommonGameTag.APPROPRIATENESS_PLAYING
            ),
        },
        SSBindingBodyLocation.MOUTH.name: {
            SSBodySide.BOTH: (
                CommonGameTag.APPROPRIATENESS_EATING,
                CommonGameTag.APPROPRIATENESS_CALL_TO_MEAL,
                CommonGameTag.APPROPRIATENESS_PHONE,
                CommonGameTag.APPROPRIATENESS_FRONT_DESK,
                CommonGameTag.APPROPRIATENESS_SINGING,
                CommonGameTag.APPROPRIATENESS_SOCIAL_PICKER,
                CommonGameTag.APPROPRIATENESS_HOST,
                CommonGameTag.SOCIAL_FLIRTY,
                CommonGameTag.INTERACTION_SOCIAL_ALL,
                CommonGameTag.INTERACTION_CHAT
            ),
        },
        SSBindingBodyLocation.WRISTS.name: {
            SSBodySide.BOTH: (
                CommonGameTag.APPROPRIATENESS_WORKOUT,
                CommonGameTag.APPROPRIATENESS_BARTENDING,
                CommonGameTag.APPROPRIATENESS_READ_BOOKS,
                CommonGameTag.APPROPRIATENESS_CLEANING,
                CommonGameTag.APPROPRIATENESS_CAKE,
                CommonGameTag.APPROPRIATENESS_COOKING,
                CommonGameTag.APPROPRIATENESS_PHONE_GAME,
                CommonGameTag.APPROPRIATENESS_PHONE,
                CommonGameTag.APPROPRIATENESS_PLAYING,
                CommonGameTag.APPROPRIATENESS_EATING,
                CommonGameTag.APPROPRIATENESS_COMPUTER,
                CommonGameTag.APPROPRIATENESS_GRAB_SNACK,
                CommonGameTag.APPROPRIATENESS_PLAY_INSTRUMENT,
                CommonGameTag.APPROPRIATENESS_TOUCHING,
                CommonGameTag.APPROPRIATENESS_TRASH,
                CommonGameTag.APPROPRIATENESS_TIP,
                CommonGameTag.INTERACTION_SOCIAL_TOUCHING
            ),
        },
        SSBindingBodyLocation.ARMS.name: {
            SSBodySide.BOTH: (
                CommonGameTag.APPROPRIATENESS_WORKOUT,
                CommonGameTag.APPROPRIATENESS_BARTENDING,
                CommonGameTag.APPROPRIATENESS_READ_BOOKS,
                CommonGameTag.APPROPRIATENESS_CLEANING,
                CommonGameTag.APPROPRIATENESS_CAKE,
                CommonGameTag.APPROPRIATENESS_COOKING,
                CommonGameTag.APPROPRIATENESS_PHONE_GAME,
                CommonGameTag.APPROPRIATENESS_PHONE,
                CommonGameTag.APPROPRIATENESS_PLAYING,
                CommonGameTag.APPROPRIATENESS_EATING,
                CommonGameTag.APPROPRIATENESS_COMPUTER,
                CommonGameTag.APPROPRIATENESS_GRAB_SNACK,
                CommonGameTag.APPROPRIATENESS_PLAY_INSTRUMENT,
                CommonGameTag.APPROPRIATENESS_TOUCHING,
                CommonGameTag.APPROPRIATENESS_TRASH,
                CommonGameTag.APPROPRIATENESS_TIP,
                CommonGameTag.INTERACTION_SOCIAL_TOUCHING
            ),
        },
        SSBindingBodyLocation.LEGS.name: {
            SSBodySide.BOTH: (
                CommonGameTag.APPROPRIATENESS_DANCING,
                CommonGameTag.APPROPRIATENESS_WORKOUT
            ),
        },
        SSBindingBodyLocation.ANKLES.name: {
            SSBodySide.BOTH: (
                CommonGameTag.APPROPRIATENESS_DANCING,
                CommonGameTag.APPROPRIATENESS_WORKOUT
            ),
        },
        SSBindingBodyLocation.FEET.name: {
            SSBodySide.BOTH: (
                CommonGameTag.APPROPRIATENESS_DANCING,
                CommonGameTag.APPROPRIATENESS_WORKOUT
            ),
        }
    }

    @staticmethod
    def _is_interaction_allowed(sim_info: SimInfo, interaction: Interaction):
        try:
            tags = interaction.appropriateness_tags
            if not tags:
                return True
            sim_data = SSSimData(sim_info)
            if not sim_data.is_slave_or_captive:
                return True
            if CommonSimStateUtils.is_dying(sim_info):
                return True
            log.format_with_message('Checking if Sim is allowed to perform interaction.', sim=CommonSimNameUtils.get_full_name(sim_info), interaction=CommonInteractionUtils.get_interaction_short_name(interaction))
            allowed = True
            if not sim_data.allowances:
                allowed = False
            else:
                for tag in tags:
                    if tag not in sim_data.allowances:
                        allowed = False
                        break
            if allowed and sim_data.restrained_body_parts:
                for (restrained_body_location, body_side) in sim_data.restrained_body_parts.items():
                    if not allowed:
                        break
                    if body_side == SSBodySide.NONE:
                        continue
                    if restrained_body_location not in _SSInteractionAllowance._ALLOWANCES_PREVENTED_BY_LOCATION:
                        continue
                    body_sides = _SSInteractionAllowance._ALLOWANCES_PREVENTED_BY_LOCATION[restrained_body_location]
                    if body_side not in body_sides:
                        continue
                    allowance_tags = body_sides[body_side]
                    if not allowance_tags:
                        continue
                    for tag in tags:
                        if tag in allowance_tags:
                            allowed = False
                            break
                    if not allowed:
                        if sim_info is CommonSimUtils.get_active_sim_info() and interaction.is_user_directed and not interaction.is_autonomous and not interaction.is_autonomous_picker_interaction:
                            CommonBasicNotification(
                                SSStringId.RESTRAINED,
                                SSStringId.YOUR_BINDINGS_ARE_PREVENTING_THAT_ACTION,
                            ).show(icon=IconInfoData(obj_instance=sim_info))
                        return False
            if not allowed:
                log.format_with_message('Not allowed.', allowance_tags=sim_data.allowances, tags_of_interaction=tags)
                if sim_info is CommonSimUtils.get_active_sim_info() and interaction.is_user_directed and not interaction.is_autonomous and not interaction.is_autonomous_picker_interaction:
                    if sim_data.is_slave:
                        description = SSStringId.YOUR_MASTER_HAS_FORBIDDEN_THAT_INTERACTION
                    else:
                        description = SSStringId.YOUR_CAPTOR_HAS_FORBIDDEN_THAT_INTERACTION
                    CommonBasicNotification(
                        SSStringId.NOT_ALLOWED,
                        description,
                    ).show(icon=IconInfoData(obj_instance=sim_info))
                return False
            log.format_with_message('Allowed.', allowance_tags=sim_data.allowances, tags_of_interaction=tags)
        except Exception as ex:
            log.error('Error occurred while checking interaction allowance.', exception=ex)
        return True


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _ss_prevent_non_allowed_interactions(event_data: S4CLInteractionQueuedEvent) -> bool:
    interaction = event_data.interaction
    owning_sim_info = CommonSimUtils.get_sim_info(interaction.sim)
    if owning_sim_info is None:
        return True
    return _SSInteractionAllowance._is_interaction_allowed(owning_sim_info, interaction)
