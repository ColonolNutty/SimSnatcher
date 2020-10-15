from typing import Any

from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.order_to.dialogs.order_hostage_to_dialog import SSOrderToDialog
from cnsimsnatcher.order_to.enums.string_ids import SSOrderToStringId
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from cnsimsnatcher.slavery.enums.string_ids import SSSlaveryStringId
from distributor.shared_messages import IconInfoData
from event_testing.results import TestResult
from interactions.context import InteractionContext
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_state_utils import CommonSimStateUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class SSOrderToCookMealFridgeInteraction(CommonImmediateSuperInteraction):
    """ Handles the interaction. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_order_to_cook_meal_fridge'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context)
        if interaction_target is None or CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        if not SSSettingUtils().is_enabled_for_interactions(sim_info):
            cls.get_log().debug('Failed, Active Sim or Target Sim is not available for interactions.')
            return TestResult.NONE
        if CommonSimStateUtils.is_dying(sim_info):
            cls.get_log().debug('Failed, Active Sim is dying.')
            return cls.create_test_result(False, reason='Active Sim is dying.')
        cls.get_log().debug('Success, can order.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.format_with_message('Running \'{}\' on_run.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)

        sim_info = CommonSimUtils.get_sim_info(interaction_sim)

        def _on_chosen(chosen_sim_info: SimInfo):
            self.log.format_with_message('Sim chosen, attempting to queue interaction.', hostage_sim=chosen_sim_info)

            target_interaction = self._get_interaction()
            enqueue_result = CommonSimInteractionUtils.queue_interaction(chosen_sim_info, CommonInteractionUtils.get_interaction_id(target_interaction), target=interaction_target)
            self.log.format(enqueue_result=enqueue_result)
            if enqueue_result:
                self.log.debug('Successfully located and queued an interaction.')
                CommonBasicNotification(
                    SSOrderToStringId.ORDER_ACCEPTED,
                    SSOrderToStringId.SIM_WILL_CARRY_OUT_ORDER,
                    description_tokens=(chosen_sim_info, )
                ).show(icon=IconInfoData(obj_instance=chosen_sim_info))
            else:
                self.log.debug('Failed to locate an interaction.')
                CommonBasicNotification(
                    SSSlaveryStringId.FAILED_TO_PERFORM,
                    SSSlaveryStringId.SIM_FAILED_TO_LOCATE_APPROPRIATE_OBJECT_PLEASE_ENSURE,
                    description_tokens=(chosen_sim_info, )
                ).show(icon=IconInfoData(obj_instance=chosen_sim_info))

        SSOrderToDialog().open_pick_captive_or_slave_dialog(sim_info, on_sim_chosen=_on_chosen)
        self.log.debug('Done doing on_run')
        return True

    def _get_interaction(self) -> int:
        # fridge_Cook
        return 13387
