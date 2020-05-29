"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable

from cnsimsnatcher.abduction.enums.string_ids import SSAbductionStringId
from cnsimsnatcher.abduction.settings.dialog import SSAbductionSettingsDialog
from cnsimsnatcher.configuration.allowance.dialogs.allowance_config_dialog import SSAllowanceConfigDialog
from cnsimsnatcher.configuration.allowance.enums.string_ids import SSAllowanceStringId
from cnsimsnatcher.enums.string_ids import SSStringId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.order_to.enums.string_ids import SSOrderToStringId
from cnsimsnatcher.order_to.settings.dialog import SSOrderToSettingsDialog
from cnsimsnatcher.slavery.enums.string_ids import SSSlaveryStringId
from cnsimsnatcher.slavery.settings.dialog import SSSlaverySettingsDialog
from sims.sim_info import SimInfo
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
    def open(self, target_sim_info: SimInfo) -> None:
        """ Open SS Settings. """
        self.log.debug('Opening SS Settings.')
        self._settings(target_sim_info).show(sim_info=target_sim_info)

    def _settings(self, target_sim_info: SimInfo) -> CommonChooseObjectOptionDialog:
        self.log.debug('Building SS Settings.')

        def _on_close() -> None:
            self.log.debug('Saving SS Settings.')
            self._settings_manager.save()
            if self._on_close is not None:
                self._on_close()

        def _reopen(*_, **__) -> None:
            self.log.debug('Reopening SS Settings.')
            self.open(target_sim_info)

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

        from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
        from cnsimsnatcher.abduction.utils.abduction_state_utils import SSAbductionStateUtils
        allowances_enabled = False
        if allowances_enabled and (SSSlaveryStateUtils().has_masters(target_sim_info) or SSAbductionStateUtils().has_captors(target_sim_info)):
            option_dialog.add_option(
                CommonDialogActionOption(
                    CommonDialogOptionContext(
                        SSAllowanceStringId.CHANGE_ALLOWANCE_NAME,
                        SSAllowanceStringId.CHANGE_ALLOWANCE_DESCRIPTION,
                    ),
                    on_chosen=lambda *_, **__: SSAllowanceConfigDialog(on_close=_reopen).open(target_sim_info)
                )
            )

        return option_dialog
