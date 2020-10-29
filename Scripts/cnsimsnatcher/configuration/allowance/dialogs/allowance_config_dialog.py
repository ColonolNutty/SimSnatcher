"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable
from cnsimsnatcher.configuration.allowance.allowances.allowance import SSAllowanceData
from cnsimsnatcher.configuration.allowance.enums.string_ids import SSAllowanceStringId
from cnsimsnatcher.configuration.allowance.utils.allowance_utils import SSAllowanceUtils
from cnsimsnatcher.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


class SSAllowanceConfigDialog(HasLog):
    """ A dialog for configuring what a Slave or Captive Sim is or is not allowed to do. """

    def __init__(self, on_close: Callable[..., Any]=CommonFunctionUtils.noop):
        super().__init__()
        self._on_close = on_close

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_allowance_config_dialog'

    def open(self, target_sim_info: SimInfo, page: int=1) -> None:
        """ Open Dialog. """
        try:
            self.log.debug('Opening Dialog.')
            self._settings(target_sim_info).show(sim_info=target_sim_info, page=page)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Problem occurred when opening dialog for \'{}\'.'.format(CommonSimNameUtils.get_full_name(target_sim_info)), exception=ex)

    def _settings(self, target_sim_info: SimInfo) -> CommonChooseObjectOptionDialog:
        self.log.debug('Building Dialog.')

        def _on_close() -> None:
            self.log.debug('Dialog closed.')
            if self._on_close is not None:
                self._on_close()

        def _reopen(*_, **__) -> None:
            self.log.debug('Reopening Dialog.')
            self.open(target_sim_info, page=option_dialog.current_page)

        option_dialog = CommonChooseObjectOptionDialog(
            SSAllowanceStringId.CHANGE_ALLOWANCE_NAME,
            SSAllowanceStringId.CHANGE_ALLOWANCE_DESCRIPTION,
            on_close=_on_close,
            mod_identity=self.mod_identity
        )

        def _on_allowance_chosen(_: str, chosen_allowance: SSAllowanceData):
            if _ is None or chosen_allowance is None:
                _on_close()
                return
            result = chosen_allowance.toggle_allowance(target_sim_info)
            _reopen()
            return result

        allowances = SSAllowanceUtils().get_allowance_data()

        def _on_allow_everything() -> None:
            SSAllowanceUtils().set_allow_all(target_sim_info)
            _reopen()

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    SSAllowanceStringId.ALLOW_EVERYTHING,
                    0,
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_on_allow_everything
            )
        )

        def _on_allow_nothing() -> None:
            SSAllowanceUtils().set_disallow_all(target_sim_info)
            _reopen()

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    SSAllowanceStringId.ALLOW_NOTHING,
                    0,
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_on_allow_nothing
            )
        )

        for allowance in allowances:
            icon = CommonIconUtils.load_checked_square_icon() if allowance.has_allowance(target_sim_info) else CommonIconUtils.load_unchecked_square_icon()
            option_dialog.add_option(
                CommonDialogSelectOption(
                    str(allowance.title),
                    allowance,
                    CommonDialogOptionContext(
                        allowance.title,
                        allowance.description,
                        description_tokens=(target_sim_info,),
                        icon=icon
                    ),
                    on_chosen=_on_allowance_chosen
                )
            )

        return option_dialog
