"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable
from cnsimsnatcher.enums.string_ids import SSStringId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.order_to.enums.string_ids import SSOrderToStringId
from cnsimsnatcher.order_to.settings.settings import SSOrderToSetting
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_branch_option import CommonDialogOpenDialogOption
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_toggle_option import CommonDialogToggleOption
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class SSOrderToSettingsDialog(HasLog):
    """ Settings for the SS Order To Settings. """

    def __init__(self, on_close: Callable[..., Any]=CommonFunctionUtils.noop):
        super().__init__()
        self._on_close = on_close
        from cnsimsnatcher.data_management.data_manager_utils import SSDataManagerUtils
        self._settings_manager = SSDataManagerUtils().get_order_to_mod_settings_manager()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'sso_settings_dialog'

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def open(self) -> None:
        """ Open SS Order To Settings. """
        self.log.debug('Opening SS Order To Settings.')
        self._settings().show()

    def _settings(self) -> CommonChooseObjectOptionDialog:
        self.log.debug('Building SS Order To Settings.')

        def _on_close() -> None:
            self.log.debug('Saving SS Order To Settings.')
            self._settings_manager.save()
            if self._on_close is not None:
                self._on_close()

        option_dialog = CommonChooseObjectOptionDialog(
            SSOrderToStringId.ORDER_TO_SETTINGS_NAME,
            SSOrderToStringId.ORDER_TO_SETTINGS_DESCRIPTION,
            on_close=_on_close
        )

        option_dialog.add_option(
            CommonDialogOpenDialogOption(
                self._cheat_settings,
                CommonDialogOptionContext(
                    SSStringId.CHEAT_SETTINGS_NAME,
                    SSStringId.CHEAT_SETTINGS_DESCRIPTION
                )
            )
        )
        return option_dialog

    def _cheat_settings(self) -> CommonChooseObjectOptionDialog:
        self.log.debug('Building SS Order To Cheat Settings.')

        def _on_close() -> None:
            self.log.debug('SS Order To Cheat Settings closed.')
            self.open()

        def _reopen(*_, **__) -> None:
            self.log.debug('Reopening SS Order To Cheat Settings.')
            self._cheat_settings().show()

        option_dialog = CommonChooseObjectOptionDialog(
            SSStringId.CHEAT_SETTINGS_NAME,
            SSStringId.CHEAT_SETTINGS_DESCRIPTION,
            on_close=_on_close
        )

        def _on_setting_changed(setting_name: str, setting_value: bool):
            if setting_value is not None:
                self.log.debug('Updating Order To Cheat setting \'{}\' with value {}'.format(setting_name, str(setting_value)))
                self._settings_manager.set_setting(setting_name, setting_value)
            _reopen()

        option_dialog.add_option(
            CommonDialogToggleOption(
                SSOrderToSetting.SHOW_DEBUG_INTERACTIONS_FOR_PERFORM_INTERACTION_ORDER,
                self._settings_manager.get_setting(
                    SSOrderToSetting.SHOW_DEBUG_INTERACTIONS_FOR_PERFORM_INTERACTION_ORDER,
                    variable_type=bool
                ),
                CommonDialogOptionContext(
                    SSOrderToStringId.SHOW_DEBUG_INTERACTIONS_IN_PERFORM_INTERACTION_DIALOG_NAME,
                    SSOrderToStringId.SHOW_DEBUG_INTERACTIONS_IN_PERFORM_INTERACTION_DIALOG_DESCRIPTION
                ),
                on_chosen=_on_setting_changed
            )
        )

        return option_dialog
