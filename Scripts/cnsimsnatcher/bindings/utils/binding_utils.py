"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Tuple, Iterator, Union, Dict

from cnsimsnatcher.bindings.enums.body_side import SSBodySide
from cnsimsnatcher.cas_parts.cas_part_type import SSCASPartType
from cnsimsnatcher.cas_parts.query.cas_part_query_utils import SSCASPartQueryUtils
from cnsimsnatcher.cas_parts.tag_filters.binding_body_location_filter import SSBindingBodyLocationCASPartFilter
from cnsimsnatcher.cas_parts.tag_filters.binding_body_side_filter import SSBindingBodySideCASPartFilter
from cnsimsnatcher.cas_parts.tag_filters.body_type_filter import SSBodyTypeCASPartFilter
from cnsimsnatcher.cas_parts.tag_filters.cas_part_tag_filter import SSCASPartTagFilter
from cnsimsnatcher.dtos.cas_parts.binding_cas_part import SSBindingCASPart
from cnsimsnatcher.dtos.cas_parts.body_cas_part import SSBodyCASPart
from cnsimsnatcher.dtos.cas_parts.cas_part import SSCASPart
from cnsimsnatcher.bindings.enums.binding_body_location import SSBindingBodyLocation
from sims4communitylib.services.sim.cas.common_sim_outfit_io import CommonSimOutfitIO
from sims.occult.occult_enums import OccultType
from sims.outfits.outfit_enums import OutfitCategory, BodyType
from sims.outfits.outfit_utils import get_maximum_outfits_for_category
from sims.sim_info import SimInfo
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.sims.common_occult_utils import CommonOccultUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from cnsimsnatcher.modinfo import ModInfo


class SSBindingUtils(HasLog):
    """ Utilities for applying and removing Bindings. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_binding'

    def has_binding(self, sim_info: SimInfo, binding_cas_part: SSBindingCASPart) -> bool:
        """has_binding(sim_info, binding_cas_part)

        Determine if a Sim has a Binding.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param binding_cas_part: The binding cas part.
        :type binding_cas_part: SSBindingCASPart
        :return: True, if the Sim has the binding on their current outfit. False, if not.
        :rtype: bool
        """
        body_type = self._get_body_type(binding_cas_part.part_id)
        return CommonCASUtils.has_cas_part_attached(sim_info, binding_cas_part.part_id, body_type=body_type)

    def get_bindings(self, sim_info: SimInfo, body_location: SSBindingBodyLocation=None, body_side: SSBodySide=None, additional_filters: Iterator[SSCASPartTagFilter]=()) -> Tuple[SSBindingCASPart]:
        """get_bindings(sim_info, body_location=None, additional_filters=())

        Retrieve bindings for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param body_location: A body location. If set, only bindings matching the body location will be returned. If None, all bindings will be returned. Default is None.
        :type body_location: SSBindingBodyLocation, optional
        :param body_side: A body location. If set, only bindings matching the body side will be returned. If None, all bindings will be returned. Default is None.
        :type body_side: SSBodySide, optional
        :param additional_filters: Additional filters for filtering bindings. Default is an empty collection.
        :type additional_filters: Iterator[SSCASPartTagFilter], optional
        :return: A collection of Binding CAS Parts matching the criteria.
        :rtype: Tuple[SSBindingCASPart]
        """
        additional_filters = tuple(additional_filters)
        if body_location is not None:
            additional_filters = (
                *additional_filters,
                SSBindingBodyLocationCASPartFilter(body_location),
            )
        if body_side is not None:
            additional_filters = (
                *additional_filters,
                SSBindingBodySideCASPartFilter(body_side)
            )
        result: Tuple[SSBindingCASPart] = SSCASPartQueryUtils().get_cas_parts_for_sim(
            sim_info,
            SSCASPartType.BINDING,
            additional_filters=additional_filters
        )
        return result

    def add_bindings(self, sim_info: SimInfo, body_locations: Tuple[SSBindingBodyLocation], body_side: SSBodySide=None) -> bool:
        """add_bindings(sim_info, body_location, body_side=None)

        Add Bindings to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param body_locations: A collection of binding body locations to add.
        :type body_locations: Tuple[SSBindingBodyLocation]
        :param body_side: The side to add bindings to. If set to None, all sides will be considered. Default is None.
        :type body_side: SSBodySide, optional
        :return: True, if the Bindings were added successfully. False, if not.
        :rtype: bool
        """
        sim_name = CommonSimNameUtils.get_full_name(sim_info)
        self.log.debug('Attempting to add Binding. Location: {} to Sim {}'.format(body_locations, sim_name))
        current_outfit = CommonOutfitUtils.get_current_outfit(sim_info)
        has_added = False
        for body_location in body_locations:
            self.log.debug('Checking body location {}'.format(body_location))
            if body_location == SSBindingBodyLocation.NONE:
                self.log.debug('binding is disabled or None, skipping.')
                continue
            binding_cas_parts = self.get_bindings(sim_info, body_location=body_location, body_side=body_side)
            if not binding_cas_parts:
                self.log.debug('No binding parts found for {} Location: {}'.format(sim_name, body_location))
                continue

            has_cas_part = False
            for binding_cas_part in binding_cas_parts:
                if not CommonOutfitUtils.has_cas_part_attached(sim_info, binding_cas_part.part_id):
                    self.log.debug('{} does not have binding cas part {} attached already.'.format(sim_name, binding_cas_part.unique_identifier))
                    continue
                self.log.debug('{} has binding cas part {} attached already.'.format(sim_name, binding_cas_part.unique_identifier))
                has_cas_part = True
                break
            if not has_cas_part:
                self.log.debug('\'{}\' has no binding cas parts attached for binding {}. Attaching one now.'.format(sim_name, body_location))
                random_binding_cas_part: SSCASPart = random.choice(binding_cas_parts)
                if self._attach_binding_to_every_outfit(sim_info, (random_binding_cas_part.part_id, *random_binding_cas_part.additional_part_ids), resend_outfits=False):
                    has_added = True
        if has_added:
            self.log.debug('At least one binding was applied, applying the changes.')
            CommonOutfitUtils.set_outfit_dirty(sim_info, CommonOutfitUtils.get_current_outfit_category(sim_info))
            CommonOutfitUtils.set_current_outfit(sim_info, current_outfit)
        else:
            self.log.debug('No Bindings were applied.')
        self.log.debug('Done attempting to apply Bindings.')
        return has_added

    def add_binding(self, sim_info: SimInfo, binding_cas_part: SSBindingCASPart) -> bool:
        """add_binding(sim_info, binding_cas_part)

        Add a Binding to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param binding_cas_part: The binding cas parts to add.
        :type binding_cas_part: SSBindingCASPart
        :return: True, if the Binding was added successfully. False, if not.
        :rtype: bool
        """
        sim_name = CommonSimNameUtils.get_full_name(sim_info)
        self.log.debug('Attempting to add Binding to Sim {}: {}'.format(sim_name, binding_cas_part))
        return self._attach_binding_to_every_outfit(sim_info, (binding_cas_part.part_id, *binding_cas_part.additional_part_ids))

    def remove_bindings(self, sim_info: SimInfo, body_locations: Iterator[SSBindingBodyLocation]=(), body_side: SSBodySide=None) -> bool:
        """remove_bindings(sim_info, body_locations=(), body_side=None)

        Remove Bindings from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param body_locations: A collection of Body Locations to Remove. If empty, all Body Locations will be removed. Default is an empty collection.
        :type body_locations: Iterator[SSBindingBodyLocation], optional
        :param body_side: The side to remove bindings from. If set to None, all sides will be removed. Default is None.
        :type body_side: SSBodySide, optional
        :return: True, if the Body Locations were removed. False, if not.
        :rtype: bool
        """
        sim_name = CommonSimNameUtils.get_full_name(sim_info)
        self.log.format_with_message('Removing Bindings from \'{}\'.'.format(sim_name), binding_body_locations=body_locations)
        current_outfit = CommonOutfitUtils.get_current_outfit(sim_info)
        has_removed = False
        if not body_locations:
            body_locations = SSBindingBodyLocation.get_all()
        # noinspection PyTypeChecker
        for body_location in body_locations:
            self.log.debug('Checking binding body location {}'.format(body_location))
            if body_location == SSBindingBodyLocation.NONE:
                self.log.debug('Binding body location was None')
                continue
            binding_cas_parts = self.get_bindings(sim_info, body_location=body_location, body_side=body_side)
            for binding_cas_part in binding_cas_parts:
                self.log.debug('Removing binding {} for cas part {}'.format(body_location, binding_cas_part.unique_identifier))
                if not CommonOutfitUtils.has_cas_part_attached(sim_info, binding_cas_part.part_id):
                    self.log.debug('Binding CAS Part was not attached {}.'.format(binding_cas_part.unique_identifier))
                    continue
                if not self._detach_binding_from_every_outfit(sim_info, (binding_cas_part.part_id, *binding_cas_part.additional_part_ids), resend_outfits=False):
                    self.log.debug('Binding CAS Part failed to be removed {}.'.format(binding_cas_part.unique_identifier))
                    continue
                has_removed = True
        if has_removed:
            self.log.debug('At least one binding was removed, refreshing the outfit of \'{}\''.format(sim_name))
            CommonOutfitUtils.set_outfit_dirty(sim_info, CommonOutfitUtils.get_current_outfit_category(sim_info))
            CommonOutfitUtils.set_current_outfit(sim_info, current_outfit)
            return True
        else:
            self.log.debug('No bindings were removed from \'{}\'.'.format(sim_name))
        self.log.debug('Done Removing Bindings.')
        return False

    def remove_binding(self, sim_info: SimInfo, binding_cas_part: SSBindingCASPart) -> bool:
        """remove_binding(sim_info, binding_cas_part)

        Remove a Binding from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param binding_cas_part: The binding cas parts to add.
        :type binding_cas_part: SSBindingCASPart
        :return: True, if the Binding was added successfully. False, if not.
        :rtype: bool
        """
        sim_name = CommonSimNameUtils.get_full_name(sim_info)
        self.log.debug('Attempting to add Binding to Sim {}: {}'.format(sim_name, binding_cas_part))
        return self._detach_binding_from_every_outfit(sim_info, (binding_cas_part.part_id, *binding_cas_part.additional_part_ids))

    def _attach_binding_to_every_outfit(self, sim_info: SimInfo, binding_cas_part_ids: Iterator[int], resend_outfits: bool=True) -> bool:
        from sims.outfits.outfit_utils import get_maximum_outfits_for_category
        binding_cas_part_ids = tuple(binding_cas_part_ids)
        current_outfit = CommonOutfitUtils.get_current_outfit(sim_info)
        result = False

        for occult_base_sim_info in CommonOccultUtils.get_sim_info_for_all_occults_gen(sim_info, (OccultType.MERMAID,)):
            for outfit_category in CommonOutfitUtils.get_all_outfit_categories():
                for outfit_index in range(get_maximum_outfits_for_category(outfit_category)):
                    if not CommonOutfitUtils.has_outfit(occult_base_sim_info, (outfit_category, outfit_index)):
                        continue
                    for binding_cas_part_id in binding_cas_part_ids:
                        if binding_cas_part_id == -1:
                            self.log.debug('No binding cas part id.')
                            continue

                        body_type = self._get_body_type(binding_cas_part_id)

                        if CommonCASUtils.attach_cas_part_to_sim(occult_base_sim_info, binding_cas_part_id, body_type=body_type, outfit_category_and_index=(outfit_category, outfit_index)):
                            result = True
        if result and resend_outfits:
            self.log.debug('Bindings {} were successfully attached.'.format(binding_cas_part_ids))
            CommonOutfitUtils.set_outfit_dirty(sim_info, CommonOutfitUtils.get_current_outfit_category(sim_info))
            CommonOutfitUtils.set_current_outfit(sim_info, current_outfit)
        return result

    def _detach_binding_from_every_outfit(self, sim_info: SimInfo, binding_cas_part_ids: Iterator[int], resend_outfits: bool=True) -> bool:
        binding_cas_part_ids = tuple(binding_cas_part_ids)
        result = False
        for occult_base_sim_info in CommonOccultUtils.get_sim_info_for_all_occults_gen(sim_info, (OccultType.MERMAID,)):
            for outfit_category in CommonOutfitUtils.get_all_outfit_categories():
                for outfit_index in range(get_maximum_outfits_for_category(outfit_category)):
                    if not CommonOutfitUtils.has_outfit(occult_base_sim_info, (outfit_category, outfit_index)):
                        continue
                    for binding_cas_part_id in binding_cas_part_ids:
                        if binding_cas_part_id == -1:
                            self.log.debug('No binding cas part id.')
                            return False

                        body_type = self._get_body_type(binding_cas_part_id)

                        native_body_part = self._locate_native_body_part_if_exists(sim_info, body_type)

                        if CommonCASUtils.detach_cas_part_from_sim(occult_base_sim_info, binding_cas_part_id, body_type=body_type, outfit_category_and_index=(outfit_category, outfit_index)):
                            result = True
                            if native_body_part is not None:
                                CommonCASUtils.attach_cas_part_to_sim(occult_base_sim_info, native_body_part.part_id, body_type=body_type, outfit_category_and_index=(outfit_category, outfit_index))

        if result and resend_outfits:
            self.log.debug('Bindings {} were successfully detached.'.format(binding_cas_part_ids))
            CommonOutfitUtils.resend_outfits(sim_info)
        return result

    def _get_body_type(self, cas_part_id: int) -> BodyType:
        body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        if body_type == BodyType.SHOES:
            body_type = BodyType.SOCKS
        return body_type

    def _create_outfit_io_if_none(self, sim_info: SimInfo, outfit_io: Union[CommonSimOutfitIO, None]=None, outfit_category_and_index: Tuple[OutfitCategory, int]=None, override_outfit_parts: Dict[BodyType, int]=None) -> (CommonSimOutfitIO, bool):
        """ Create an outfit editor if the one provided is None, else return the one provided. """
        if outfit_io is not None:
            return outfit_io, True
        try:
            outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=outfit_category_and_index, initial_outfit_parts=override_outfit_parts)
        except RuntimeError:
            outfit_io = None
        return outfit_io, False

    def _locate_native_body_part_if_exists(self, sim_info: SimInfo, body_type: Union[int, BodyType]) -> Union[SSBodyCASPart, None]:
        body_cas_parts = SSCASPartQueryUtils().get_cas_parts_for_sim(sim_info, SSCASPartType.BODY, additional_filters=(
            SSBodyTypeCASPartFilter(body_type),
        ))
        if not body_cas_parts:
            return None
        return random.choice(body_cas_parts)
