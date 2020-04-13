"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any

from cnsimsnatcher.enums.string_identifiers import SSStringId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.settings.data.manager import SSSettingsManager
from cnsimsnatcher.settings.settings import SSSetting
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_branch_option import CommonDialogOpenDialogOption
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_toggle_option import CommonDialogToggleOption
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog


class SSSettingsDialog:
    """ Settings for the SS Abduction mod. """
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def open() -> None:
        """ Open Abduction settings. """
        SSSettingsDialog._settings().show()

    @staticmethod
    def _settings() -> CommonChooseObjectOptionDialog:
        def _on_close() -> None:
            SSSettingsDialog._get_mod_settings_manager().save()

        option_dialog = CommonChooseObjectOptionDialog(
            SSStringId.SIM_SNATCHER_SETTINGS_NAME,
            SSStringId.SIM_SNATCHER_SETTINGS_DESCRIPTION,
            on_close=_on_close
        )

        def _on_setting_changed(setting_name: str, setting_value: bool):
            if setting_value is not None:
                SSSettingsDialog._get_mod_settings_manager().set_setting(setting_name, setting_value)
            SSSettingsDialog._settings().show()

        option_dialog.add_option(
            CommonDialogToggleOption(
                SSSetting.ABDUCTION_INTERACTIONS_SWITCH,
                SSSettingsDialog._get_mod_settings_manager().get_setting(
                    SSSetting.ABDUCTION_INTERACTIONS_SWITCH,
                    variable_type=bool
                ),
                CommonDialogOptionContext(
                    SSStringId.ABDUCTION_INTERACTIONS_SWITCH_NAME,
                    SSStringId.ABDUCTION_INTERACTIONS_SWITCH_DESCRIPTION,
                ),
                on_chosen=_on_setting_changed
            )
        )

        option_dialog.add_option(
            CommonDialogOpenDialogOption(
                SSSettingsDialog._cheat_settings,
                CommonDialogOptionContext(
                    SSStringId.SS_CHEATS_NAME,
                    SSStringId.SS_CHEATS_DESCRIPTION
                )
            )
        )
        return option_dialog

    @staticmethod
    def _cheat_settings() -> CommonChooseObjectOptionDialog:
        def _on_close() -> None:
            SSSettingsDialog._settings().show()

        option_dialog = CommonChooseObjectOptionDialog(
            SSStringId.SS_CHEATS_NAME,
            SSStringId.SS_CHEATS_DESCRIPTION,
            on_close=_on_close
        )

        def _on_setting_changed(setting_name: str, setting_value: bool):
            if setting_value is not None:
                SSSettingsDialog._get_mod_settings_manager().set_setting(setting_name, setting_value)
            SSSettingsDialog._cheat_settings().show()

        option_dialog.add_option(
            CommonDialogToggleOption(
                SSSetting.ABDUCTION_ALWAYS_SUCCESSFUL_SWITCH,
                SSSettingsDialog._get_mod_settings_manager().get_setting(
                    SSSetting.ABDUCTION_ALWAYS_SUCCESSFUL_SWITCH,
                    variable_type=bool
                ),
                CommonDialogOptionContext(
                    SSStringId.ABDUCTION_ALWAYS_SUCCESSFUL_SWITCH_NAME,
                    SSStringId.ABDUCTION_ALWAYS_SUCCESSFUL_SWITCH_DESCRIPTION
                ),
                on_chosen=_on_setting_changed
            )
        )

        option_dialog.add_option(
            CommonDialogToggleOption(
                SSSetting.SHOW_DEBUG_INTERACTIONS_FOR_PERFORM_INTERACTION_ORDER,
                SSSettingsDialog._get_mod_settings_manager().get_setting(
                    SSSetting.SHOW_DEBUG_INTERACTIONS_FOR_PERFORM_INTERACTION_ORDER,
                    variable_type=bool
                ),
                CommonDialogOptionContext(
                    SSStringId.SHOW_DEBUG_INTERACTIONS_IN_PERFORM_INTERACTION_DIALOG_NAME,
                    SSStringId.SHOW_DEBUG_INTERACTIONS_IN_PERFORM_INTERACTION_DIALOG_DESCRIPTION
                ),
                on_chosen=_on_setting_changed
            )
        )

        return option_dialog

    @staticmethod
    def _get_data() -> Dict[str, Any]:
        return SSSettingsDialog._get_mod_settings_manager().settings

    @staticmethod
    def _get_mod_settings_manager() -> SSSettingsManager:
        from cnsimsnatcher.data_management.data_manager_utils import SSDataManagerUtils
        return SSDataManagerUtils.get_mod_settings_manager()
