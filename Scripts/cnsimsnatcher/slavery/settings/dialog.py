"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable

from cnsimsnatcher.enums.string_ids import SSStringId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.slavery.enums.string_ids import SSSlaveryStringId
from cnsimsnatcher.slavery.settings.settings import SSSlaverySetting
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_branch_option import \
    CommonDialogOpenDialogOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_input_option import \
    CommonDialogInputFloatOption
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_toggle_option import CommonDialogToggleOption
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class SSSlaverySettingsDialog(HasLog):
    """ Settings for SS Slavery. """

    def __init__(self, on_close: Callable[..., Any]=CommonFunctionUtils.noop):
        super().__init__()
        self._on_close = on_close
        from cnsimsnatcher.persistence.ss_data_manager_utils import SSDataManagerUtils
        self._data_store = SSDataManagerUtils().get_slavery_mod_settings_data_store()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_slavery_settings_dialog'

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def open(self) -> None:
        """ Open SS Slavery Settings. """
        self.log.debug('Opening Slavery Settings.')
        self._settings().show()

    def _settings(self) -> CommonChooseObjectOptionDialog:
        self.log.debug('Building Slavery Settings.')

        def _reopen() -> None:
            self.open()

        def _on_close() -> None:
            if self._on_close is not None:
                self._on_close()

        option_dialog = CommonChooseObjectOptionDialog(
            SSSlaveryStringId.SLAVERY_SETTINGS_NAME,
            SSSlaveryStringId.SLAVERY_SETTINGS_DESCRIPTION,
            on_close=_on_close,
            mod_identity=self.mod_identity
        )

        def _on_setting_changed(setting_name: str, setting_value: bool):
            if setting_value is not None:
                self._data_store.set_value_by_key(setting_name, setting_value)
            _reopen()

        option_dialog.add_option(
            CommonDialogToggleOption(
                SSSlaverySetting.SLAVERY_INTERACTIONS_SWITCH,
                self._data_store.get_value_by_key(
                    SSSlaverySetting.SLAVERY_INTERACTIONS_SWITCH
                ),
                CommonDialogOptionContext(
                    SSSlaveryStringId.ENABLE_SLAVERY_INTERACTIONS_NAME,
                    SSSlaveryStringId.ENABLE_SLAVERY_INTERACTIONS_DESCRIPTION
                ),
                on_chosen=_on_setting_changed
            )
        )

        def _on_input_setting_changed(setting_name: str, setting_value: float, outcome: CommonChoiceOutcome):
            if setting_value is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                _reopen()
                return
            self._data_store.set_value_by_key(setting_name, setting_value)
            _reopen()

        option_dialog.add_option(
            CommonDialogInputFloatOption(
                SSSlaverySetting.ATTEMPT_TO_ENSLAVE_SUCCESS_CHANCE,
                self._data_store.get_value_by_key(
                    SSSlaverySetting.ATTEMPT_TO_ENSLAVE_SUCCESS_CHANCE
                ),
                CommonDialogOptionContext(
                    SSSlaveryStringId.ATTEMPT_TO_ENSLAVE_SUCCESS_CHANCE_NAME,
                    SSSlaveryStringId.ATTEMPT_TO_ENSLAVE_SUCCESS_CHANCE_DESCRIPTION,
                    description_tokens=(
                        self._data_store.get_default_value_by_key(SSSlaverySetting.ATTEMPT_TO_ENSLAVE_SUCCESS_CHANCE),
                    )
                ),
                min_value=0.0,
                max_value=100.0,
                on_chosen=_on_input_setting_changed
            )
        )

        option_dialog.add_option(
            CommonDialogOpenDialogOption(
                lambda *_, **__: self._cheat_settings(on_close=_reopen),
                CommonDialogOptionContext(
                    SSStringId.CHEAT_SETTINGS_NAME,
                    SSStringId.CHEAT_SETTINGS_DESCRIPTION
                )
            )
        )
        return option_dialog

    def _cheat_settings(self, on_close: Callable[[], Any]=None) -> CommonChooseObjectOptionDialog:
        self.log.debug('Building SS Slavery Cheat Settings.')

        def _reopen() -> None:
            self._cheat_settings(on_close=on_close).show()

        def _on_close() -> None:
            self.log.debug('SS Slavery Cheat Settings closed.')
            if on_close is not None:
                on_close()

        option_dialog = CommonChooseObjectOptionDialog(
            SSStringId.CHEAT_SETTINGS_NAME,
            SSStringId.CHEAT_SETTINGS_DESCRIPTION,
            on_close=_on_close,
            mod_identity=self.mod_identity
        )

        def _on_setting_changed(setting_name: str, setting_value: bool):
            if setting_value is not None:
                self.log.debug('Updating Slavery Cheat setting \'{}\' with value {}'.format(setting_name, str(setting_value)))
                self._data_store.set_value_by_key(setting_name, setting_value)
            _reopen()

        option_dialog.add_option(
            CommonDialogToggleOption(
                SSSlaverySetting.ATTEMPT_TO_ENSLAVE_ALWAYS_SUCCESSFUL,
                self._data_store.get_value_by_key(
                    SSSlaverySetting.ATTEMPT_TO_ENSLAVE_ALWAYS_SUCCESSFUL
                ),
                CommonDialogOptionContext(
                    SSSlaveryStringId.ATTEMPT_TO_ENSLAVE_ALWAYS_SUCCESSFUL_NAME,
                    SSSlaveryStringId.ATTEMPT_TO_ENSLAVE_ALWAYS_SUCCESSFUL_DESCRIPTION
                ),
                on_chosen=_on_setting_changed
            )
        )

        return option_dialog
