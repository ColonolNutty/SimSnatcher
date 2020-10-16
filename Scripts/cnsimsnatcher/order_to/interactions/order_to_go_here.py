"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cnsimsnatcher.order_to.enums.string_ids import SSOrderToStringId
from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
from distributor.shared_messages import IconInfoData
from event_testing.results import TestResult
from interactions.context import InteractionContext
from cnsimsnatcher.order_to.dialogs.order_hostage_to_dialog import SSOrderToDialog
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from cnsimsnatcher.abduction.utils.abduction_state_utils import SSAbductionStateUtils
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.objects.common_object_location_utils import CommonObjectLocationUtils
from sims4communitylib.utils.sims.common_sim_location_utils import CommonSimLocationUtils
from sims4communitylib.utils.sims.common_sim_state_utils import CommonSimStateUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ssutilities.commonlib.utils.commonterrainutils import SSCommonTerrainUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class SSOrderToGoHereInteraction(CommonImmediateSuperInteraction):
    """ Handles the Order To... Go Here interaction. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_order_to_go_here'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=TestResult.NONE)
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context, kwargles=kwargs)
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        if interaction_target is None or CommonTypeUtils.is_sim_instance(interaction_target):
            cls.get_log().debug('Failed, Target is invalid.')
            return TestResult.NONE
        if not SSSettingUtils().is_enabled_for_interactions(sim_info):
            cls.get_log().debug('Failed, Active Sim are not enabled for interactions.')
            return TestResult.NONE

        if CommonSimStateUtils.is_dying(sim_info):
            cls.get_log().debug('Failed, Active Sim is dying.')
            return cls.create_test_result(False, reason='Dying Sims cannot order Sims around. The Active Sim is currently dying.')
        if CommonTypeUtils.is_terrain(interaction_target) or CommonTypeUtils.is_ocean(interaction_target) or CommonTypeUtils.is_swimming_pool(interaction_target):
            cls.get_log().debug('Target is terrain, ocean, or a swimming pool.')
            if not SSCommonTerrainUtils.is_safe_route_surface_position(interaction_target, interaction_context):
                cls.get_log().debug('Failed, target is not a safe route surface.')
                return TestResult.NONE
        else:
            cls.get_log().debug('Failed, Target was not the ground.')
            return TestResult.NONE
        if not SSAbductionStateUtils().has_captives(sim_info) and not SSSlaveryStateUtils().has_slaves(sim_info):
            cls.get_log().debug('Failed, Active Sim has not abducted sims.')
            return TestResult.NONE
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.format_with_message('Running \'{}\' on_started.'.format(self), interaction_sim=interaction_sim, interaction_target=interaction_target)
        self.log.debug('Running go to residence interaction')
        source_sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        location_position = SSCommonTerrainUtils.get_route_surface_position_from_interaction_context(self.context) or CommonObjectLocationUtils.get_position(interaction_target)
        location_level = SSCommonTerrainUtils.get_route_surface_level_from_interaction_context(self.context) or CommonObjectLocationUtils.get_surface_level(interaction_target)

        def _on_hostage_chosen(hostage_sim_info: SimInfo):
            self.log.debug('Sending hostage sim to go there.')
            if CommonSimLocationUtils.send_to_position(
                hostage_sim_info,
                location_position,
                location_level
            ):
                self.log.debug('Success, hostage will go there!')
                CommonBasicNotification(
                    SSOrderToStringId.ORDER_ACCEPTED,
                    SSOrderToStringId.SIM_WILL_CARRY_OUT_ORDER,
                    description_tokens=(hostage_sim_info, )
                ).show(icon=IconInfoData(obj_instance=hostage_sim_info))
            else:
                self.log.debug('Failed, could not tell hostage to go there!')
                CommonBasicNotification(
                    SSOrderToStringId.ORDER_REFUSED,
                    SSOrderToStringId.SIM_REFUSED_TO_CARRY_OUT_ORDER,
                    description_tokens=(hostage_sim_info, )
                ).show(icon=IconInfoData(obj_instance=hostage_sim_info))

        self.log.debug('Opening dialog.')
        SSOrderToDialog().open_pick_captive_or_slave_dialog(source_sim_info, on_sim_chosen=_on_hostage_chosen)
        return True
