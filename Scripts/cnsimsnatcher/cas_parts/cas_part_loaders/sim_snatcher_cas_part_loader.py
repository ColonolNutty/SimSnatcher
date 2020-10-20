"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cnsimsnatcher.cas_parts.cas_part_loaders.base_cas_part_loader import SSBaseCASPartLoader
from cnsimsnatcher.cas_parts.cas_part_tuning import SimSnatcherCASPartPackage
from cnsimsnatcher.dtos.cas_parts.binding_cas_part import SSBindingCASPart
from cnsimsnatcher.dtos.cas_parts.body_cas_part import SSBodyCASPart
from cnsimsnatcher.dtos.cas_parts.cas_part import SSCASPart


class SSSimSnatcherCASPartLoader(SSBaseCASPartLoader):
    """ Loads Sim Snatcher CAS Parts. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_cas_part_loader'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def snippet_names(self) -> Tuple[str]:
        result: Tuple[str] = (
            'has_sim_snatcher_cas_parts',
        )
        return result

    def _load(self, package_cas_parts: SimSnatcherCASPartPackage) -> Tuple[SSCASPart]:
        cas_parts: Tuple[SSCASPart] = (
            *tuple([SSBindingCASPart.load_from_package(package_cas_part, self.log) for package_cas_part in getattr(package_cas_parts, 'binding_cas_parts_list', tuple())]),
            *tuple([SSBodyCASPart.load_from_package(package_cas_part, self.log) for package_cas_part in getattr(package_cas_parts, 'body_cas_parts_list', tuple())]),
        )
        return cas_parts
