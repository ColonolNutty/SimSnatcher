"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cnsimsnatcher.modinfo import ModInfo
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.data_management.common_data_manager import CommonDataManager
from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
from sims4communitylib.persistence.persistence_services.common_persistence_service import CommonPersistenceService


@CommonDataManagerRegistry.common_data_manager()
class SSDataManager(CommonDataManager):
    """ Manage a storage of data. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_data_manager'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def persistence_services(self) -> Tuple[CommonPersistenceService]:
        from sims4communitylib.persistence.persistence_services.common_file_persistence_service import \
            CommonFilePersistenceService
        result: Tuple[CommonPersistenceService] = (
            CommonFilePersistenceService(),
        )
        return result
