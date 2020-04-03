"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from distributor.shared_messages import IconInfoData
from event_testing.results import TestResult
from interactions.context import InteractionContext
from cnsimsnatcher.dialog.order_hostage_to_dialog import SSAbductionOrderHostageToDialog
from cnsimsnatcher.enums.string_identifiers import SSStringId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from cnsimsnatcher.utils.abduction_state_utils import SSAbductionStateUtils
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_sim_state_utils import CommonSimStateUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ssutilities.commonlib.utils.commonterrainutils import CommonTerrainUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'ss_order_to_go_here')


class SSOrderToGoHereInteraction(CommonImmediateSuperInteraction):
    """ Handles the Order To... Go Here interaction. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=TestResult.NONE)
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        log.format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context, kwargles=kwargs)
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        if interaction_target is None or CommonTypeUtils.is_sim_instance(interaction_target):
            log.debug('Failed, Target is invalid.')
            return TestResult.NONE
        if not SSSettingUtils.is_enabled_for_interactions(sim_info):
            log.debug('Failed, Active Sim are not enabled for interactions.')
            return TestResult.NONE

        if CommonSimStateUtils.is_dying(sim_info):
            log.debug('Failed, Active Sim is dying.')
            return cls.create_test_result(False, reason='Dying Sims cannot order Sims around. The Active Sim is currently dying.')
        if CommonTypeUtils.is_terrain(interaction_target) or CommonTypeUtils.is_ocean(interaction_target) or CommonTypeUtils.is_swimming_pool(interaction_target):
            log.debug('Target is terrain, ocean, or a swimming pool.')
            if not CommonTerrainUtils.is_safe_route_surface_position(interaction_target, interaction_context):
                log.debug('Failed, target is not a safe route surface.')
                return TestResult.NONE
        else:
            log.debug('Failed, Target was not the ground.')
            return TestResult.NONE
        if not SSAbductionStateUtils.has_abducted_sims(sim_info):
            log.debug('Failed, Active Sim has not abducted sims.')
            return TestResult.NONE
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        log.debug('Running go to residence interaction')
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        location_position = CommonTerrainUtils.get_route_surface_position_from_interaction_context(self.context) or CommonTerrainUtils.get_route_surface_position(interaction_target)
        location_level = CommonTerrainUtils.get_route_surface_level_from_interaction_context(self.context) or CommonTerrainUtils.get_route_surface_level(interaction_target)

        def _on_hostage_chosen(hostage_sim_info: SimInfo):
            log.debug('Sending hostage sim to go there.')
            if CommonSimLocationUtils.send_to_position(
                hostage_sim_info,
                location_position,
                location_level
            ):
                log.debug('Success, hostage will go there!')
                CommonBasicNotification(
                    SSStringId.ORDER_ACCEPTED,
                    SSStringId.SIM_WILL_CARRY_OUT_ORDER,
                    description_tokens=(hostage_sim_info, )
                ).show(icon=IconInfoData(obj_instance=hostage_sim_info))
            else:
                log.debug('Failed, could not tell hostage to go there!')
                CommonBasicNotification(
                    SSStringId.ORDER_REFUSED,
                    SSStringId.SIM_REFUSED_TO_CARRY_OUT_ORDER,
                    description_tokens=(hostage_sim_info, )
                ).show(icon=IconInfoData(obj_instance=hostage_sim_info))

        log.debug('Opening dialog.')
        SSAbductionOrderHostageToDialog.open_pick_hostage_dialog(sim_info, on_sim_chosen=_on_hostage_chosen)
        return True