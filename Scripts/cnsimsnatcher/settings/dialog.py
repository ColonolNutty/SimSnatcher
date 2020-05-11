"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable

from cnsimsnatcher.abduction.enums.string_ids import SSAbductionStringId
from cnsimsnatcher.abduction.settings.dialog import SSAbductionSettingsDialog
from cnsimsnatcher.enums.string_ids import SSStringId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.order_to.enums.string_ids import SSOrderToStringId
from cnsimsnatcher.order_to.settings.dialog import SSOrderToSettingsDialog
from cnsimsnatcher.slavery.enums.string_ids import SSSlaveryStringId
from cnsimsnatcher.slavery.settings.dialog import SSSlaverySettingsDialog
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class SSSettingsDialog(HasLog):
    """ Settings for the Sim Snatcher mod. """

    def __init__(self, on_close: Callable[..., Any]=CommonFunctionUtils.noop):
        super().__init__()
        self._on_close = on_close
        from cnsimsnatcher.data_management.data_manager_utils import SSDataManagerUtils
        self._settings_manager = SSDataManagerUtils().get_global_mod_settings_manager()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_settings_dialog'

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def open(self) -> None:
        """ Open SS Settings. """
        self.log.debug('Opening SS Settings.')
        self._settings().show()

    def _settings(self) -> CommonChooseObjectOptionDialog:
        self.log.debug('Building SS Settings.')

        def _on_close() -> None:
            self.log.debug('Saving SS Settings.')
            self._settings_manager.save()
            if self._on_close is not None:
                self._on_close()

        def _reopen(*_, **__) -> None:
            self.log.debug('Reopening SS Settings.')
            self.open()

        option_dialog = CommonChooseObjectOptionDialog(
            SSStringId.SIM_SNATCHER_SETTINGS_NAME,
            SSStringId.SIM_SNATCHER_SETTINGS_DESCRIPTION,
            on_close=_on_close
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    SSAbductionStringId.ABDUCTION_SETTINGS_NAME,
                    SSAbductionStringId.ABDUCTION_SETTINGS_DESCRIPTION,
                ),
                on_chosen=SSAbductionSettingsDialog(on_close=_reopen).open
            )
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    SSSlaveryStringId.SLAVERY_SETTINGS_NAME,
                    SSSlaveryStringId.SLAVERY_SETTINGS_DESCRIPTION,
                ),
                on_chosen=SSSlaverySettingsDialog(on_close=_reopen).open
            )
        )

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    SSOrderToStringId.ORDER_TO_SETTINGS_NAME,
                    SSOrderToStringId.ORDER_TO_SETTINGS_DESCRIPTION,
                ),
                on_chosen=SSOrderToSettingsDialog(on_close=_reopen).open
            )
        )

        return option_dialog
