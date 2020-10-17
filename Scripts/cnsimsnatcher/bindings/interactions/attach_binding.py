"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cnsimsnatcher.bindings.enums.binding_type import SSBindingType
from cnsimsnatcher.persistence.ss_sim_data_storage import SSSimDataStore
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from cnsimsnatcher.slavery.settings.setting_utils import SSSlaverySettingUtils
from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
from event_testing.results import TestResult
from interactions.context import InteractionContext
from cnsimsnatcher.modinfo import ModInfo
from sims.sim import Sim
from sims4.tuning.tunable import TunableEnumSet
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class SSBindingAttachBindingInteraction(CommonImmediateSuperInteraction):
    """ Handle the interaction. """
    INSTANCE_TUNABLES = {
        'binding_type': TunableEnumSet(enum_type=SSBindingType)
    }

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ssb_attach_binding'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context, kwargles=kwargs)
        if not SSSlaverySettingUtils().interactions_are_enabled():
            cls.get_log().debug('Failed, Slavery interactions are disabled.')
            return TestResult.NONE
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            cls.get_log().debug('Failed, Target is invalid.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if sim_info is target_sim_info:
            cls.get_log().debug('Failed, Active Sim is the Target Sim.')
            return TestResult.NONE
        if not SSSettingUtils().is_enabled_for_interactions(sim_info) or not SSSettingUtils().is_enabled_for_interactions(target_sim_info):
            cls.get_log().debug('Failed, Active Sim or Target Sim are not enabled for interactions.')
            return TestResult.NONE
        target_sim_data = SSSimDataStore(target_sim_info)
        if not target_sim_data.is_slave and not target_sim_data.is_captive:
            cls.get_log().debug('Failed, Target Sim is not captured.')
            return TestResult.NONE
        cls.get_log().debug('Success, showing detach binding interaction on target.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.format_with_message('Running \'{}\' on_started.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        if interaction_target is None or not CommonTypeUtils.is_sim_instance(interaction_target):
            self.log.debug('Failed, no Target or they were not a Sim.')
            return False
        source_sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        self.log.format_with_message('Attempting to force enslave Sim.', sim=CommonSimNameUtils.get_full_name(target_sim_info))
        from cnsimsnatcher.abduction.utils.abduction_state_utils import SSAbductionStateUtils
        SSAbductionStateUtils().release_captive(target_sim_info)
        SSSlaveryStateUtils().release_slave(target_sim_infoy)
        SSSlaveryStateUtils().release_slaves_of(target_sim_info)
        SSAbductionStateUtils().release_captives_of(target_sim_info)
        result, reason = SSSlaveryStateUtils().create_slave(target_sim_info, source_sim_info)
        if not result:
            self.log.error('Failed to enslave \'{}\' with \'{}\' because {}'.format(CommonSimNameUtils.get_full_name(target_sim_info), CommonSimNameUtils.get_full_name(source_sim_info), reason))
        else:
            self.log.debug('Done forcing enslave.')
        return result
