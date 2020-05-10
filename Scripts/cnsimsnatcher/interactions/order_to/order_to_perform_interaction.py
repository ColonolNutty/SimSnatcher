"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
from distributor.shared_messages import IconInfoData
from event_testing.results import TestResult
from interactions.base.interaction import Interaction
from interactions.context import InteractionContext
from cnsimsnatcher.dialog.order_hostage_to_dialog import SSOrderToDialog
from cnsimsnatcher.enums.string_ids import SSStringId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from cnsimsnatcher.utils.abduction_state_utils import SSAbductionStateUtils
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.dialogs.common_ok_dialog import CommonOkDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.objects.common_object_interaction_utils import CommonObjectInteractionUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_state_utils import CommonSimStateUtils
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ssutilities.commonlib.utils.commonterrainutils import CommonTerrainUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class SSOrderToPerformInteractionInteraction(CommonImmediateSuperInteraction):
    """ Handles the Order To... Perform Interaction interaction. """

    # noinspection SpellCheckingInspection
    _EXCLUDED_INTERACTION_NAME_SNIPPETS = {
        'terrain-create',
        'sim-stand',
        'dog_stand',
        'cat_stand',
        'cheat',
        'setuplot',
        'gohere',
        'terrain-teleport',
        'proxy',
        'debug',
        'forcemarriage',
        'socialpickersi',
        'solo_moveaway',
        'hospitalexambed',
        'generic_toilet',
        'generic_shower',
        'generic_bath',
        'generic_bubblebath',
        'generic_relaxingbath',
        'generic_bedundercovers',
        'generic_sittogether',
        'generic_sitintimate',
        'generic_watchintimate',
        'generic_bed_sleep',
        'generic_cook',
        'bed_getnear_fromsocial',
        'eat_to_clean_from_sit',
        'fridge_grabsnack_autotest',
        'simsnatcher',
        ModInfo.get_identity().base_namespace.lower()
    }

    # noinspection SpellCheckingInspection
    _EXCLUDED_DEBUG_INTERACTION_NAME_SNIPPETS = {
        'picker_relbit',
        'picker_trait',
        'picker_buff',
        'picker_grounding',
        'simray_frozen',
        'si_grimreaper',
        'si_sim_energyfailure',
        'ensembleinteractions',
        'goingoutsocials',
        'simpicker',
        'changeoutfitpicker_targetsim',
        'tobirthdaycake',
        'purchase_holidaytraditions',
        'aggregatesi_gohome',
        'autonomous',
        'death_',
        'solo_skeleton_add',
        'npc_choose_to_leave',
        'terrain_setup_garden',
        'piemenu',
        'object_hirenpc',
        'simsnatcher',
        ModInfo.get_identity().base_namespace.lower()
    }

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_order_to_perform_interaction'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=TestResult.NONE)
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context, kwargles=kwargs)
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        if not SSSettingUtils().is_enabled_for_interactions(sim_info):
            cls.get_log().debug('Failed, Active Sim is not enabled for interactions.')
            return TestResult.NONE
        if not SSAbductionStateUtils().has_captives(sim_info) and not SSSlaveryStateUtils().has_slaves(sim_info):
            cls.get_log().debug('Failed, Active Sim has not abducted sims.')
            return TestResult.NONE
        if interaction_target is None:
            cls.get_log().debug('Failed, Target invalid.')
            return TestResult.NONE

        if CommonSimStateUtils.is_dying(sim_info):
            cls.get_log().debug('Failed, Active Sim is dying.')
            return cls.create_test_result(False, reason='Dying Sims cannot order Sims around. The Active Sim is currently dying.')
        if CommonTypeUtils.is_terrain(interaction_target) or CommonTypeUtils.is_ocean(interaction_target) or CommonTypeUtils.is_swimming_pool(interaction_target):
            cls.get_log().debug('Target is terrain, ocean, or a swimming pool.')
            if not CommonTerrainUtils.is_safe_route_surface_position(interaction_target, interaction_context):
                cls.get_log().debug('Failed, target is not a safe route surface.')
                return TestResult.NONE
        elif CommonTypeUtils.is_game_object(interaction_target):
            cls.get_log().debug('Target is an object.')

            def _get_top_level_object(target) -> bool:
                while target.parent is not None:
                    target = target.parent
                return target

            interaction_target = _get_top_level_object(interaction_target) or interaction_target
            cls.get_log().format(top_level_object=interaction_target)
            cls.get_log().debug('Checking if object is in use.')
            if hasattr(interaction_target, 'get_users'):
                current_obj_users = interaction_target.get_users(sims_only=True)
                if len(current_obj_users) > 1:
                    cls.get_log().debug('Failed, Location is reserved by more than one sim.')
                    return cls.create_test_result(False, reason='Object is reserved.', tooltip=CommonLocalizationUtils.create_localized_tooltip(SSStringId.OBJECT_IS_IN_USE))
                if len(current_obj_users) == 1:
                    cls.get_log().debug('Failed, Location is reserved already.')
                    return cls.create_test_result(False, reason='The object is currently in use.', tooltip=CommonLocalizationUtils.create_localized_tooltip(SSStringId.OBJECT_IS_IN_USE))
        else:
            cls.get_log().debug('Failed, Target was not valid.')
            return TestResult.NONE
        cls.get_log().debug('Success.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.format_with_message('Running \'{}\' on_started.'.format(self), interaction_sim=interaction_sim, interaction_target=interaction_target)
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)

        def _interaction_with_name(interaction: Interaction) -> bool:
            interaction_short_name = CommonInteractionUtils.get_interaction_short_name(interaction)
            self.log.format_with_message('Checking interaction with short name: ', interaction_short_name=interaction_short_name)
            for exclude in SSOrderToPerformInteractionInteraction._EXCLUDED_INTERACTION_NAME_SNIPPETS:
                if exclude in interaction_short_name.lower():
                    self.log.debug('Failed, Interaction is invalid.')
                    return False
            self.log.debug('Success, Interaction is valid.')
            return True

        def _debug_interaction_with_name(interaction: Interaction) -> bool:
            if SSSettingUtils().cheats.should_show_debug_interactions_for_perform_interaction():
                return True
            interaction_short_name = CommonInteractionUtils.get_interaction_short_name(interaction)
            self.log.format_with_message('Checking interaction with short name: ', interaction_short_name=interaction_short_name)
            for exclude in SSOrderToPerformInteractionInteraction._EXCLUDED_DEBUG_INTERACTION_NAME_SNIPPETS:
                if exclude in interaction_short_name.lower():
                    self.log.debug('Failed, Interaction is invalid.')
                    return False
            self.log.debug('Success, Interaction is valid.')
            return True

        def _on_hostage_chosen(hostage_sim_info: SimInfo):
            self.log.format_with_message('Hostage chosen, choosing interaction.', hostage_sim=hostage_sim_info)

            hostage_sim_instance = CommonSimUtils.get_sim_instance(hostage_sim_info)
            interactions_list = CommonObjectInteractionUtils.get_all_interactions_registered_to_object_gen(interaction_target, include_interaction_callback=CommonFunctionUtils.run_predicates_as_one((_interaction_with_name, _debug_interaction_with_name)))
            self.log.format_with_message('Found interactions', interactions=interactions_list)
            hostage_interaction_context: InteractionContext = self.context.clone_for_sim(hostage_sim_instance)
            option_dialog = CommonChooseObjectOptionDialog(
                SSStringId.CHOOSE_INTERACTION,
                SSStringId.CHOOSE_INTERACTION_TO_PERFORM,
                mod_identity=ModInfo.get_identity()
            )

            def _on_interaction_chosen(option_identifier: str, chosen_interaction_id: int):
                self.log.format_with_message('Chose interaction \'{}\' with id \'{}\'.'.format(option_identifier, chosen_interaction_id))
                if CommonSimInteractionUtils.queue_interaction(
                    hostage_sim_info,
                    chosen_interaction_id,
                    target=interaction_target
                ):
                    self.log.debug('Success, Sim will do the interaction!')
                    CommonBasicNotification(
                        SSStringId.ORDER_ACCEPTED,
                        SSStringId.SIM_WILL_CARRY_OUT_ORDER,
                        description_tokens=(hostage_sim_info, )
                    ).show(icon=IconInfoData(obj_instance=hostage_sim_info))
                else:
                    self.log.debug('Failed, could not tell Sim will do the interaction!')
                    CommonBasicNotification(
                        SSStringId.ORDER_REFUSED,
                        SSStringId.SIM_REFUSED_TO_CARRY_OUT_ORDER,
                        description_tokens=(hostage_sim_info, )
                    ).show(icon=IconInfoData(obj_instance=hostage_sim_info))

            for interaction in interactions_list:
                # noinspection PyBroadException
                try:
                    interaction_name = CommonInteractionUtils.get_interaction_display_name(interaction, tokens=(hostage_sim_instance, interaction_target))
                    interaction_short_name = CommonInteractionUtils.get_interaction_short_name(interaction)
                    if not SSOrderToDialog().can_perform_interaction(
                        interaction,
                        self.super_affordance,
                        hostage_interaction_context,
                        hostage_sim_instance,
                        interaction_target
                    ):
                        self.log.format_with_message('Interaction could not be performed', interaction_name=interaction_short_name)
                        continue
                except Exception:
                    # If the interaction explodes here, then it is probably something we couldn't run anyways.
                    continue
                self.log.format(interaction=interaction, class_name=interaction.__name__, interaction_name=interaction_name)
                if not interaction_name or not interaction_short_name:
                    continue
                interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
                if interaction_id is None:
                    continue
                option_dialog.add_option(
                    CommonDialogSelectOption(
                        interaction_short_name,
                        interaction_id,
                        context=CommonDialogOptionContext(
                            interaction_name,
                            interaction_short_name
                        ),
                        on_chosen=_on_interaction_chosen
                    )
                )

            if not option_dialog.has_options():
                self.log.debug('No interactions found.')
                CommonOkDialog(
                    SSStringId.NO_INTERACTIONS_FOUND,
                    0
                ).show()
                return

            if SSSettingUtils().disclaimer_has_been_shown():
                self.log.debug('Showing interaction dialog.')
                option_dialog.show(sim_info=hostage_sim_info)
            else:
                def _on_acknowledged(_: Any) -> None:
                    self.log.debug('Showing interaction dialog.')
                    option_dialog.show(sim_info=hostage_sim_info)
                    SSSettingUtils().flag_disclaimer_as_shown()

                CommonOkDialog(
                    SSStringId.DISCLAIMER_NAME,
                    SSStringId.SS_ABDUCTION_DISCLAIMER
                ).show(on_acknowledged=_on_acknowledged)

        self.log.debug('Opening dialog.')
        SSOrderToDialog().open_pick_captive_or_slave_dialog(sim_info, on_sim_chosen=_on_hostage_chosen)
        return True
