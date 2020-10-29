"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Any, Tuple

from cnsimsnatcher.bindings.enums.binding_body_location import SSBindingBodyLocation
from cnsimsnatcher.bindings.enums.body_side import SSBodySide
from cnsimsnatcher.bindings.enums.string_ids import SSBindingStringId
from cnsimsnatcher.bindings.utils.binding_utils import SSBindingUtils
from cnsimsnatcher.cas_parts.query.cas_part_query_utils import SSCASPartQueryUtils
from cnsimsnatcher.dtos.cas_parts.binding_cas_part import SSBindingCASPart
from cnsimsnatcher.persistence.ss_sim_data import SSSimData
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_ok_dialog import CommonOkDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.logging.has_log import HasLog
from cnsimsnatcher.modinfo import ModInfo
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils


class SSConfigureBindingsDialog(HasLog):
    """ Dialog for configuring bindings. """

    def __init__(self, target_sim_info: SimInfo, on_close: Callable[..., Any]=None) -> None:
        super().__init__()
        self._target_sim_info = target_sim_info
        self._on_close = on_close
        self._query_utils = SSCASPartQueryUtils()
        self._binding_utils = SSBindingUtils()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_configure_bindings'

    def open(self) -> None:
        """ Open the dialog. """

        def _reopen(*_, **__) -> None:
            self.open()

        def _on_close(*_, **__) -> bool:
            self.log.debug('Dialog closed.')
            if self._on_close is not None:
                self._on_close()
            return False

        @CommonExceptionHandler.catch_exceptions(self.mod_identity, fallback_return=False)
        def _on_chosen(_: str, chosen: SSBindingBodyLocation):
            if chosen is None:
                self.log.format_with_message('No chosen', chosen=chosen)
                return _on_close()
            self.log.format_with_message('Chosen body location', chosen=chosen)
            self._choose_body_side(chosen, on_close=_reopen)
            return True

        option_dialog = CommonChooseObjectOptionDialog(
            SSBindingStringId.BODY_LOCATION,
            0,
            on_close=_on_close
        )

        def _on_detach_all() -> None:
            self._binding_utils.remove_bindings(self._target_sim_info, tuple(SSBindingBodyLocation.values))
            _on_close()

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    SSBindingStringId.DETACH_ALL_BINDINGS,
                    0,
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_on_detach_all
            )
        )

        for body_location in SSBindingBodyLocation.values:
            if body_location == SSBindingBodyLocation.NONE:
                continue
            # noinspection PyTypeChecker
            binding_cas_parts_list = self._binding_utils.get_bindings(self._target_sim_info, body_location=body_location)
            if not binding_cas_parts_list:
                continue
            description = CommonLocalizationUtils.create_localized_string(SSBindingStringId.BINDINGS_COUNT_STRING, tokens=(str(len(binding_cas_parts_list)),))

            option_dialog.add_option(
                CommonDialogSelectOption(
                    str(body_location.name),
                    body_location,
                    CommonDialogOptionContext(
                        body_location.name,
                        description,
                        icon=CommonIconUtils.load_arrow_navigate_into_icon()
                    ),
                    on_chosen=_on_chosen
                )
            )

        if not option_dialog.has_options():
            CommonOkDialog(
                SSBindingStringId.NO_BINDINGS_FOUND,
                0,
                mod_identity=self.mod_identity
            ).show()
            _on_close()
            return

        option_dialog.show(
            sim_info=self._target_sim_info
        )

    def _choose_body_side(self, body_location: SSBindingBodyLocation, page: int=1, on_close: Callable[..., Any]=None):
        def _reopen(*_, **__) -> None:
            self._choose_body_side(body_location, page=option_dialog.current_page, on_close=on_close)

        def _on_close(*_, **__) -> bool:
            self.log.debug('Dialog closed.')
            if on_close is not None:
                on_close()
            return False

        @CommonExceptionHandler.catch_exceptions(self.mod_identity, fallback_return=False)
        def _on_chosen(_: str, chosen: SSBodySide):
            if chosen is None:
                self.log.format_with_message('No chosen', chosen=chosen)
                return _on_close()
            self.log.format_with_message('Chosen body location', chosen=chosen)
            self._choose_binding(body_location, chosen, on_close=_reopen)
            return True

        option_dialog = CommonChooseObjectOptionDialog(
            SSBindingStringId.BODY_SIDE,
            0,
            on_close=_on_close
        )

        def _on_detach_all() -> None:
            self._binding_utils.remove_bindings(self._target_sim_info, tuple(SSBindingBodyLocation.values))
            _reopen()

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    SSBindingStringId.DETACH_ALL_BINDINGS,
                    0,
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_on_detach_all
            )
        )

        for body_side in SSBodySide.values:
            if body_side == SSBindingBodyLocation.NONE:
                continue
            # noinspection PyTypeChecker
            binding_cas_parts_list = self._binding_utils.get_bindings(self._target_sim_info, body_location=body_location, body_side=body_side)
            if not binding_cas_parts_list:
                continue
            description = CommonLocalizationUtils.create_localized_string(SSBindingStringId.BINDINGS_COUNT_STRING, tokens=(str(len(binding_cas_parts_list)),))

            option_dialog.add_option(
                CommonDialogSelectOption(
                    str(body_side.name),
                    body_side,
                    CommonDialogOptionContext(
                        body_side.name,
                        description,
                        icon=CommonIconUtils.load_arrow_navigate_into_icon()
                    ),
                    on_chosen=_on_chosen
                )
            )

        if not option_dialog.has_options():
            CommonOkDialog(
                SSBindingStringId.NO_BINDINGS_FOUND,
                0,
                mod_identity=self.mod_identity
            ).show()
            _on_close()
            return

        option_dialog.show(
            sim_info=self._target_sim_info,
            page=page
        )

    def _choose_binding(self, body_location: SSBindingBodyLocation, body_side: SSBodySide, page: int=1, on_close: Callable[..., Any]=None):
        binding_cas_parts = self._binding_utils.get_bindings(self._target_sim_info, body_location=body_location, body_side=body_side)

        def _reopen(*_, **__) -> None:
            self._choose_binding(body_location, body_side, page=option_dialog.current_page, on_close=on_close)

        def _on_close(*_, **__) -> bool:
            self.log.debug('Dialog closed.')
            if on_close is not None:
                on_close()
            return False

        sim_data = SSSimData(self._target_sim_info)

        @CommonExceptionHandler.catch_exceptions(self.mod_identity, fallback_return=False)
        def _on_chosen(_: str, binding: SSBindingCASPart):
            if binding is None:
                self.log.format_with_message('No chosen', chosen=binding)
                return _on_close()
            self.log.format_with_message('Chosen binding', chosen=binding)
            if binding.body_side == SSBodySide.BOTH:
                self._binding_utils.remove_bindings(self._target_sim_info, body_locations=(binding.body_location, ))
            else:
                if sim_data.has_body_restraint(binding.body_location, SSBodySide.BOTH):
                    self._binding_utils.remove_bindings(self._target_sim_info, body_locations=(binding.body_location, ), body_side=SSBodySide.BOTH)

            if self._binding_utils.has_binding(self._target_sim_info, binding):
                if self._binding_utils.remove_binding(self._target_sim_info, binding):
                    sim_data.remove_body_restraint(binding.body_location, binding.body_side)
            else:
                if self._binding_utils.add_binding(self._target_sim_info, binding):
                    sim_data.apply_body_restraint(binding.body_location, binding.body_side)
            _reopen()
            return True

        option_dialog = CommonChooseObjectOptionDialog(
            CommonLocalizationUtils.create_localized_string(body_location.name),
            0,
            on_close=_on_close
        )

        def _on_detach_all() -> None:
            self._binding_utils.remove_bindings(self._target_sim_info, (body_location, ), body_side=body_side)
            _reopen()

        option_dialog.add_option(
            CommonDialogActionOption(
                CommonDialogOptionContext(
                    SSBindingStringId.DETACH_ALL_BINDINGS,
                    0,
                    icon=CommonIconUtils.load_arrow_right_icon()
                ),
                on_chosen=_on_detach_all
            )
        )

        for binding_cas_part in binding_cas_parts:
            option_dialog.add_option(
                CommonDialogSelectOption(
                    str(binding_cas_part.name),
                    binding_cas_part,
                    CommonDialogOptionContext(
                        binding_cas_part.display_name,
                        0,
                        icon=CommonIconUtils.load_checked_square_icon() if self._binding_utils.has_binding(self._target_sim_info, binding_cas_part) else CommonIconUtils.load_unchecked_square_icon()
                    ),
                    on_chosen=_on_chosen
                )
            )

        if not option_dialog.has_options():
            CommonOkDialog(
                SSBindingStringId.NO_BINDINGS_FOUND,
                0,
                mod_identity=self.mod_identity
            ).show()
            _on_close()
            return

        option_dialog.show(sim_info=self._target_sim_info, page=page)
