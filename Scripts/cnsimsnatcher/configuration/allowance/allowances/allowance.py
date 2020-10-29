"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Set

from sims.sim_info import SimInfo
from sims4communitylib.enums.tags_enum import CommonGameTag


class SSAllowanceData:
    """ Data for an allowance. """

    @property
    def title(self) -> int:
        """ The title of the allowance. """
        return 0

    @property
    def description(self) -> int:
        """ The description of the allowance. """
        return 0

    @property
    def appropriateness_tags(self) -> Set[CommonGameTag]:
        """ The appropriateness tags associated with the allowance. """
        raise NotImplementedError()

    def toggle_allowance(self, sim_info: SimInfo) -> bool:
        """ Toggle an allowance for the specified Sim. """
        if self.has_allowance(sim_info):
            return self.remove_allowance(sim_info)
        return self.add_allowance(sim_info)

    def has_allowance(self, sim_info: SimInfo) -> bool:
        """ Determine if a Sim is allowed to do this action. """
        from cnsimsnatcher.persistence.ss_sim_data import SSSimData
        data_store = SSSimData(sim_info)
        for tag in self.appropriateness_tags:
            if tag not in data_store.allowances:
                return False
        return True

    def add_allowance(self, sim_info: SimInfo) -> bool:
        """ Add this allowance to the Sim. """
        from cnsimsnatcher.persistence.ss_sim_data import SSSimData
        data_store = SSSimData(sim_info)
        new_allowances = list(data_store.allowances)
        for tag in self.appropriateness_tags:
            if tag not in new_allowances:
                new_allowances.append(tag)
        data_store.allowances = tuple(new_allowances)
        return True

    def remove_allowance(self, sim_info: SimInfo) -> bool:
        """ Remove this allowance from the Sim. """
        from cnsimsnatcher.persistence.ss_sim_data import SSSimData
        data_store = SSSimData(sim_info)
        new_allowances = list(data_store.allowances)
        for tag in self.appropriateness_tags:
            if tag in new_allowances:
                new_allowances.remove(tag)
        data_store.allowances = tuple(new_allowances)
        return True
