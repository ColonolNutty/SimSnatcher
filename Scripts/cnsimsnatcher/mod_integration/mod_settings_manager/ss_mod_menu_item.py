"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
from cnsimsnatcher.enums.image_ids import SSImageId
from sims4.resources import Types
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils

try:
    from cnsimsnatcher.enums.string_identifiers import SSStringId
    from cnsimsnatcher.modinfo import ModInfo
    from cnsimsnatcher.settings.dialog import SSSettingsDialog
    from cnsimsnatcher.settings.open_settings import SSOpenSettingsInteraction
    from typing import Callable, Any, Union
    from sims.sim_info import SimInfo
    from sims4communitylib.mod_support.mod_identity import CommonModIdentity
    from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
    from sims4communitylib.utils.common_type_utils import CommonTypeUtils
    from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
    from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
    from sims4modsettingsmenu.registration.mod_settings_menu_item import S4MSMMenuItem
    from sims4modsettingsmenu.registration.mod_settings_registry import S4MSMModSettingsRegistry
    from event_testing.results import TestResult
    from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
    from sims4communitylib.utils.common_log_registry import CommonLogRegistry
    from protocolbuffers.Localization_pb2 import LocalizedString
    from cnsimsnatcher.settings.setting_utils import SSSettingUtils


    class _SSMSMMenuItem(S4MSMMenuItem):
        # noinspection PyMissingOrEmptyDocstring
        @property
        def mod_identity(self) -> CommonModIdentity:
            return ModInfo.get_identity()

        # noinspection PyMissingOrEmptyDocstring
        @property
        def title(self) -> Union[int, str, LocalizedString, None]:
            return SSStringId.SIM_SNATCHER_SETTINGS_NAME

        # noinspection PyMissingOrEmptyDocstring
        @property
        def tooltip_text(self) -> LocalizedString:
            return SSStringId.SIM_SNATCHER_SETTINGS_DESCRIPTION

        # noinspection PyMissingOrEmptyDocstring
        @property
        def icon(self) -> Any:
            return CommonResourceUtils.get_resource_key(Types.PNG, SSImageId.MAIN_ICON)

        # noinspection PyMissingOrEmptyDocstring
        @property
        def log_identifier(self) -> str:
            return 'ss_msm_menu_item'

        # noinspection PyMissingOrEmptyDocstring
        def is_available_for(self, source_sim_info: SimInfo, target: Any=None) -> bool:
            self.log.debug('Checking if SS Settings are available for \'{}\' and Target \'{}\'.'.format(CommonSimNameUtils.get_full_name(source_sim_info), target))
            if target is None or not CommonTypeUtils.is_sim_or_sim_info(target):
                self.log.debug('Failed, Target is not a Sim.')
                return False
            if not SSSettingUtils.is_enabled_for_interactions(source_sim_info):
                self.log.debug('Failed, Source Sim is not enabled for interactions.')
                return TestResult.NONE
            target_sim_info = CommonSimUtils.get_sim_info(target)
            if not SSSettingUtils.is_enabled_for_interactions(target_sim_info):
                self.log.debug('Failed, Target Sim is not enabled for interactions.')
                return False
            self.log.debug('Menu is available for Source Sim and Target Sim.')
            return True

        # noinspection PyMissingOrEmptyDocstring
        def show(
            self,
            source_sim_info: SimInfo,
            *args,
            target: Any=None,
            on_close: Callable[..., Any]=CommonFunctionUtils.noop,
            **kwargs
        ):
            self.log.debug('Showing SS Settings.')
            SSSettingsDialog(on_close=on_close).open()


    S4MSMModSettingsRegistry().register_menu_item(_SSMSMMenuItem())

    log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'ss_settings')

    # noinspection PyUnusedLocal
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SSOpenSettingsInteraction, SSOpenSettingsInteraction.on_test.__name__)
    def _hide_interaction(original, cls, *_, **__) -> TestResult:
        log.debug('Hiding the SS Open Settings interaction in favor of the Mod Settings Menu.')
        return TestResult.NONE
except:
    pass
