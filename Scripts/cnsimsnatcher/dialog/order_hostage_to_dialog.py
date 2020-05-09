"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import routing
import objects.terrain
import sims4.math
from typing import Any, Callable
from cnsimsnatcher.enums.string_identifiers import SSStringId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.utils.abduction_state_utils import SSAbductionStateUtils
from interactions.base.interaction import Interaction
from interactions.context import InteractionContext
from server.pick_info import PickType
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_ok_dialog import CommonOkDialog
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.dialogs.option_dialogs.common_choose_sim_option_dialog import CommonChooseSimOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option import CommonDialogSimOption
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option_context import CommonDialogSimOptionContext
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ssutilities.commonlib.utils.commonterrainutils import CommonTerrainUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'ss_order_hostage_to_dialog')


class SSAbductionOrderHostageToDialog:
    """ A dialog for choosing which sims to do an order."""

    @staticmethod
    def open_pick_hostage_dialog(requester_sim_info: SimInfo, on_sim_chosen: Callable[[SimInfo], Any]):
        """ Choose captive sims to carry out an order. """

        def _on_close() -> bool:
            log.debug('Dialog closed.')
            return True

        @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
        def _on_chosen(chosen_sim_info: SimInfo) -> bool:
            if chosen_sim_info is None:
                log.format_with_message('None chosen.', chosen_sim_info=chosen_sim_info)
                _on_close()
                return False
            log.debug('Sim chosen, carrying out the order.')
            on_sim_chosen(chosen_sim_info)
            return True

        hostage_sim_info_list = SSAbductionStateUtils.get_hostages(requester_sim_info)

        option_dialog = CommonChooseSimOptionDialog(
            SSStringId.SS_ABDUCTION_CHOOSE_A_SIM_FOR_ORDER,
            0,
            on_close=_on_close
        )
        for sim_id in hostage_sim_info_list:
            sim_info = CommonSimUtils.get_sim_info(sim_id)
            option_dialog.add_option(
                CommonDialogSimOption(
                    sim_info,
                    CommonDialogSimOptionContext(
                        is_selected=False,
                        is_enabled=True
                    ),
                    on_chosen=_on_chosen
                )
            )

        if not option_dialog.has_options():
            log.debug('No hostages found.')
            CommonOkDialog(
                SSStringId.SS_ABDUCTION_NO_HOSTAGES,
                SSStringId.SS_ABDUCTION_NO_HOSTAGES_FOUND_ON_ACTIVE_LOT,
                description_tokens=('', requester_sim_info)
            ).show()
            _on_close()
            return
        log.debug('Hostages found.')
        log.format(hostage_sims=CommonSimNameUtils.get_full_names(hostage_sim_info_list))
        option_dialog.show(sim_info=requester_sim_info)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def can_perform_interaction(
        interaction: Interaction,
        super_interaction: Interaction,
        interaction_context: InteractionContext,
        interaction_sim: Sim,
        interaction_target: Any
    ) -> bool:
        """ Determine if the interaction can be performed. """
        if interaction_target is not None and (CommonTypeUtils.is_terrain(interaction_target) or CommonTypeUtils.is_ocean(interaction_target) or CommonTypeUtils.is_swimming_pool(interaction_target)):
            from server_commands.sim_commands import _build_terrain_interaction_target_and_context
            location_position = CommonTerrainUtils.get_route_surface_position_from_interaction_context(interaction_context) or CommonTerrainUtils.get_route_surface_position(interaction_target)
            location_level = CommonTerrainUtils.get_route_surface_level_from_interaction_context(interaction_context) or CommonTerrainUtils.get_route_surface_level(interaction_target)
            # noinspection PyUnresolvedReferences
            pos = sims4.math.Vector3(location_position.x, location_position.y, location_position.z)
            routing_surface = routing.SurfaceIdentifier(CommonLocationUtils.get_current_zone_id(), location_level, routing.SurfaceType.SURFACETYPE_WORLD)
            (target, context) = _build_terrain_interaction_target_and_context(interaction_sim, pos, routing_surface, PickType.PICK_TERRAIN, objects.terrain.TerrainPoint)
            return interaction_sim.test_super_affordance(interaction, target, context)
        else:
            return CommonSimInteractionUtils.test_interaction(
                CommonSimUtils.get_sim_info(interaction_sim),
                CommonInteractionUtils.get_interaction_id(interaction),
                social_super_interaction_id=CommonInteractionUtils.get_interaction_id(super_interaction),
                target=interaction_target,
                interaction_context=interaction_context
            ).result
