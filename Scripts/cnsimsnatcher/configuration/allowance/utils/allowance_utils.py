from typing import Tuple
from cnsimsnatcher.configuration.allowance.allowances.allowed_bartending import SSAllowedBartending
from cnsimsnatcher.configuration.allowance.allowances.allowed_bathing import SSAllowedBathing
from cnsimsnatcher.configuration.allowance.allowances.allowed_cleaning import SSAllowedCleaning
from cnsimsnatcher.configuration.allowance.allowances.allowed_computer import SSAllowedComputer
from cnsimsnatcher.configuration.allowance.allowances.allowed_cooking import SSAllowedCooking
from cnsimsnatcher.configuration.allowance.allowances.allowed_dancing import SSAllowedDancing
from cnsimsnatcher.configuration.allowance.allowances.allowed_eating import SSAllowedEating
from cnsimsnatcher.configuration.allowance.allowances.allowed_grab_snack import SSAllowedGrabSnack
from cnsimsnatcher.configuration.allowance.allowances.allowed_guest import SSAllowedGuest
from cnsimsnatcher.configuration.allowance.allowances.allowed_hired_worker import SSAllowedHiredWorker
from cnsimsnatcher.configuration.allowance.allowances.allowed_host import SSAllowedHost
from cnsimsnatcher.configuration.allowance.allowances.allowed_phone import SSAllowedPhone
from cnsimsnatcher.configuration.allowance.allowances.allowed_playing import SSAllowedPlaying
from cnsimsnatcher.configuration.allowance.allowances.allowed_playing_instruments import SSAllowedPlayingInstruments
from cnsimsnatcher.configuration.allowance.allowances.allowed_read_book import SSAllowedReadBook
from cnsimsnatcher.configuration.allowance.allowances.allowed_singing import SSAllowedSinging
from cnsimsnatcher.configuration.allowance.allowances.allowed_sleeping import SSAllowedSleeping
from cnsimsnatcher.configuration.allowance.allowances.allowed_social import SSAllowedSocial
from cnsimsnatcher.configuration.allowance.allowances.allowed_stereo import SSAllowedStereo
from cnsimsnatcher.configuration.allowance.allowances.allowed_tip import SSAllowedTip
from cnsimsnatcher.configuration.allowance.allowances.allowed_tv_watching import SSAllowedTvWatching
from cnsimsnatcher.configuration.allowance.allowances.allowed_view import SSAllowedView
from cnsimsnatcher.configuration.allowance.allowances.allowed_work import SSAllowedWork
from cnsimsnatcher.configuration.allowance.allowances.allowed_workout import SSAllowedWorkout
from cnsimsnatcher.configuration.allowance.allowances.allowance import SSAllowanceData
from sims.sim_info import SimInfo


class SSAllowanceUtils:
    """ Utilities for allowances. """

    def add_allowance_traits(self, sim_info: SimInfo) -> bool:
        """ Remove all allowance traits from a Sim. """
        for allowance in self.get_allowance_data():
            allowance.add_allowance(sim_info)
        return True

    def remove_allowance_traits(self, sim_info: SimInfo) -> bool:
        """ Remove all allowance traits from a Sim. """
        for allowance in self.get_allowance_data():
            allowance.remove_allowance(sim_info)
        return True

    def get_allowance_data(self) -> Tuple[SSAllowanceData]:
        """ Retrieve a collection of allowance data. """
        result: Tuple[SSAllowanceData] = tuple([
            SSAllowedBartending(),
            SSAllowedBathing(),
            SSAllowedCleaning(),
            SSAllowedComputer(),
            SSAllowedCooking(),
            SSAllowedDancing(),
            SSAllowedEating(),
            SSAllowedGrabSnack(),
            SSAllowedGuest(),
            SSAllowedHiredWorker(),
            SSAllowedHost(),
            SSAllowedPhone(),
            SSAllowedPlaying(),
            SSAllowedPlayingInstruments(),
            SSAllowedReadBook(),
            SSAllowedSinging(),
            SSAllowedSleeping(),
            SSAllowedSocial(),
            SSAllowedStereo(),
            SSAllowedTip(),
            SSAllowedTvWatching(),
            SSAllowedView(),
            SSAllowedWork(),
            SSAllowedWorkout()
        ])
        return result
