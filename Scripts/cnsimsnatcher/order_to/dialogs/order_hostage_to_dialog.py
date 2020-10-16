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
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.order_to.enums.string_ids import SSOrderToStringId
from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
from cnsimsnatcher.abduction.utils.abduction_state_utils import SSAbductionStateUtils
from interactions.base.interaction import Interaction
from interactions.context import InteractionContext
from server.pick_info import PickType
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_ok_dialog import CommonOkDialog
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.objects.common_object_location_utils import CommonObjectLocationUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.dialogs.option_dialogs.common_choose_sim_option_dialog import CommonChooseSimOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option import CommonDialogSimOption
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option_context import CommonDialogSimOptionContext
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ssutilities.commonlib.utils.commonterrainutils import SSCommonTerrainUtils


class SSOrderToDialog(HasLog):
    """ A dialog for choosing which sims to do an order."""
    def __init__(self, on_close: Callable[..., Any]=CommonFunctionUtils.noop):
        super().__init__()
        self._on_close = on_close

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_order_to_dialog'

    def open_pick_slave_dialog(self, requester_sim_info: SimInfo, on_sim_chosen: Callable[[SimInfo], Any]):
        """ Choose slave Sims to carry out an order. """

        def _on_close(*_, **__) -> None:
            self.log.debug('Dialog closed.')
            if self._on_close is not None:
                self._on_close()

        @CommonExceptionHandler.catch_exceptions(self.mod_identity)
        def _on_chosen(chosen_sim_info: SimInfo) -> bool:
            if chosen_sim_info is None:
                self.log.format_with_message('None chosen.', chosen_sim_info=chosen_sim_info)
                _on_close()
                return False
            self.log.debug('Sim chosen, carrying out the order.')
            on_sim_chosen(chosen_sim_info)
            return True

        sim_info_list = tuple(SSSlaveryStateUtils().get_slaves(requester_sim_info))

        option_dialog = CommonChooseSimOptionDialog(
            SSOrderToStringId.CHOOSE_A_SIM_FOR_ORDER,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity
        )
        for sim_id in sim_info_list:
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
            self.log.debug('No slaves found.')
            CommonOkDialog(
                SSOrderToStringId.NO_SLAVES,
                SSOrderToStringId.NO_SLAVES_FOUND_ON_ACTIVE_LOT,
                description_tokens=('', requester_sim_info)
            ).show()
            _on_close()
            return
        self.log.debug('Sims found.')
        self.log.format(hostage_sims=CommonSimNameUtils.get_full_names(sim_info_list))
        option_dialog.show(sim_info=requester_sim_info)

    def open_pick_captive_or_slave_dialog(self, requester_sim_info: SimInfo, on_sim_chosen: Callable[[SimInfo], Any]):
        """ Choose captive or slave Sims to carry out an order. """

        def _on_close(*_, **__) -> None:
            self.log.debug('Dialog closed.')
            if self._on_close is not None:
                self._on_close()

        @CommonExceptionHandler.catch_exceptions(self.mod_identity)
        def _on_chosen(chosen_sim_info: SimInfo) -> bool:
            if chosen_sim_info is None:
                self.log.format_with_message('None chosen.', chosen_sim_info=chosen_sim_info)
                _on_close()
                return False
            self.log.debug('Sim chosen, carrying out the order.')
            on_sim_chosen(chosen_sim_info)
            return True

        sim_info_list = tuple(SSAbductionStateUtils().get_captives(requester_sim_info))
        sim_info_list += tuple(SSSlaveryStateUtils().get_slaves(requester_sim_info))

        option_dialog = CommonChooseSimOptionDialog(
            SSOrderToStringId.CHOOSE_A_SIM_FOR_ORDER,
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity
        )
        for sim_id in sim_info_list:
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
            self.log.debug('No captives or slaves found.')
            CommonOkDialog(
                SSOrderToStringId.NO_CAPTIVES_OR_SLAVES,
                SSOrderToStringId.NO_CAPTIVES_OR_SLAVES_FOUND_ON_ACTIVE_LOT,
                description_tokens=('', requester_sim_info)
            ).show()
            _on_close()
            return
        self.log.debug('Sims found.')
        self.log.format(hostage_sims=CommonSimNameUtils.get_full_names(sim_info_list))
        option_dialog.show(sim_info=requester_sim_info)

    def can_perform_interaction(
        self,
        interaction: Interaction,
        super_interaction: Interaction,
        interaction_context: InteractionContext,
        interaction_sim: Sim,
        interaction_target: Any
    ) -> bool:
        """ Determine if the interaction can be performed. """
        try:
            if interaction_target is not None and (CommonTypeUtils.is_terrain(interaction_target) or CommonTypeUtils.is_ocean(interaction_target) or CommonTypeUtils.is_swimming_pool(interaction_target)):
                from server_commands.sim_commands import _build_terrain_interaction_target_and_context
                location_position = SSCommonTerrainUtils.get_route_surface_position_from_interaction_context(interaction_context) or CommonObjectLocationUtils.get_position(interaction_target)
                location_level = SSCommonTerrainUtils.get_route_surface_level_from_interaction_context(interaction_context) or CommonObjectLocationUtils.get_surface_level(interaction_target)
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
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Problem occurred when checking can_perform_interaction.', exception=ex)
            return False
