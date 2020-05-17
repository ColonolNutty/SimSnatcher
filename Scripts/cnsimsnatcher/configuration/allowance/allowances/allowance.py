from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


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
    def trait_id(self) -> int:
        """ The trait that allows/disallows something. """
        raise NotImplementedError()

    def toggle_allowance(self, sim_info: SimInfo) -> bool:
        """ Toggle an allowance for the specified Sim. """
        if self.has_allowance(sim_info):
            return self.remove_allowance(sim_info)
        return self.add_allowance(sim_info)

    def has_allowance(self, sim_info: SimInfo) -> bool:
        """ Determine if a Sim is allowed to do this action. """
        return CommonTraitUtils.has_trait(sim_info, self.trait_id)

    def add_allowance(self, sim_info: SimInfo) -> bool:
        """ Add this allowance to the Sim. """
        return CommonTraitUtils.add_trait(sim_info, self.trait_id)

    def remove_allowance(self, sim_info: SimInfo) -> bool:
        """ Remove this allowance from the Sim. """
        return CommonTraitUtils.remove_trait(sim_info, self.trait_id)