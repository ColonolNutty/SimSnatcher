"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Iterator, Any
from cnsimsnatcher.dtos.cas_parts.cas_part import SSCASPart
from cnsimsnatcher.modinfo import ModInfo
from sims4.resources import Types
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class SSBaseCASPartLoader(CommonService, HasLog):
    """ Loads CAS Parts. """
    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_cas_part_loader'

    @property
    def snippet_names(self) -> Tuple[str]:
        """ The names of snippets containing CAS parts. """
        raise NotImplementedError()

    def load(self) -> Iterator[SSCASPart]:
        """load()

        Loads all CAS parts.

        :return: An iterable of CAS parts.
        :rtype: Iterator[SSCASPart]
        """
        snippet_names: Tuple[str] = self.snippet_names

        for cas_part_package in CommonResourceUtils.load_instances_with_any_tags(Types.SNIPPET, snippet_names):
            try:
                cas_parts: Tuple[SSCASPart] = tuple(self._load(cas_part_package))

                for cas_part in cas_parts:
                    cas_part: SSCASPart = cas_part
                    if cas_part is None:
                        continue
                    (is_valid_result, is_valid_reason) = cas_part.is_valid()
                    if is_valid_result:
                        yield cas_part
                    else:
                        if cas_part.part_id != -1 and not CommonCASUtils.is_cas_part_loaded(cas_part.part_id):
                            continue
                        self.log.error('CAS Part \'{}\' by \'{}\' is not valid. Reason: {}'.format(cas_part.name, cas_part.author, is_valid_reason), throw=False)
            except Exception as ex:
                self.log.format_error('Error while parsing cas parts from \'{}\''.format(cas_part_package), exception=ex)

    def _load(self, package_cas_part: Any) -> Tuple[SSCASPart]:
        raise NotImplementedError()
