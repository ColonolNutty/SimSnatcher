"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple
from cnsimsnatcher.configuration.allowance.allowances.allowed_bartending import SSAllowedBartending
from cnsimsnatcher.configuration.allowance.allowances.allowed_bathing import SSAllowedBathing
from cnsimsnatcher.configuration.allowance.allowances.allowed_cake import SSAllowedCake
from cnsimsnatcher.configuration.allowance.allowances.allowed_call_to_meal import SSAllowedCallToMeal
from cnsimsnatcher.configuration.allowance.allowances.allowed_cleaning import SSAllowedCleaning
from cnsimsnatcher.configuration.allowance.allowances.allowed_computer import SSAllowedComputer
from cnsimsnatcher.configuration.allowance.allowances.allowed_cooking import SSAllowedCooking
from cnsimsnatcher.configuration.allowance.allowances.allowed_dancing import SSAllowedDancing
from cnsimsnatcher.configuration.allowance.allowances.allowed_eating import SSAllowedEating
from cnsimsnatcher.configuration.allowance.allowances.allowed_front_desk import SSAllowedFrontDesk
from cnsimsnatcher.configuration.allowance.allowances.allowed_grab_snack import SSAllowedGrabSnack
from cnsimsnatcher.configuration.allowance.allowances.allowed_guest import SSAllowedGuest
from cnsimsnatcher.configuration.allowance.allowances.allowed_hired_worker import SSAllowedHiredWorker
from cnsimsnatcher.configuration.allowance.allowances.allowed_host import SSAllowedHost
from cnsimsnatcher.configuration.allowance.allowances.allowed_not_during_work import SSAllowedNotDuringWork
from cnsimsnatcher.configuration.allowance.allowances.allowed_not_during_work_lunch import SSAllowedNotDuringWorkLunch
from cnsimsnatcher.configuration.allowance.allowances.allowed_phone import SSAllowedPhone
from cnsimsnatcher.configuration.allowance.allowances.allowed_phone_games import SSAllowedPhoneGames
from cnsimsnatcher.configuration.allowance.allowances.allowed_playing import SSAllowedPlaying
from cnsimsnatcher.configuration.allowance.allowances.allowed_playing_instruments import SSAllowedPlayingInstruments
from cnsimsnatcher.configuration.allowance.allowances.allowed_read_book import SSAllowedReadBook
from cnsimsnatcher.configuration.allowance.allowances.allowed_service_npc import SSAllowedServiceNpc
from cnsimsnatcher.configuration.allowance.allowances.allowed_shower import SSAllowedShower
from cnsimsnatcher.configuration.allowance.allowances.allowed_singing import SSAllowedSinging
from cnsimsnatcher.configuration.allowance.allowances.allowed_sleeping import SSAllowedSleeping
from cnsimsnatcher.configuration.allowance.allowances.allowed_social import SSAllowedSocial
from cnsimsnatcher.configuration.allowance.allowances.allowed_stereo import SSAllowedStereo
from cnsimsnatcher.configuration.allowance.allowances.allowed_tip import SSAllowedTip
from cnsimsnatcher.configuration.allowance.allowances.allowed_touching import SSAllowedTouching
from cnsimsnatcher.configuration.allowance.allowances.allowed_trash import SSAllowedTrash
from cnsimsnatcher.configuration.allowance.allowances.allowed_tv_watching import SSAllowedTvWatching
from cnsimsnatcher.configuration.allowance.allowances.allowed_view import SSAllowedView
from cnsimsnatcher.configuration.allowance.allowances.allowed_visitor import SSAllowedVisitor
from cnsimsnatcher.configuration.allowance.allowances.allowed_work import SSAllowedWork
from cnsimsnatcher.configuration.allowance.allowances.allowed_workout import SSAllowedWorkout
from cnsimsnatcher.configuration.allowance.allowances.allowance import SSAllowanceData
from cnsimsnatcher.persistence.ss_sim_data import SSSimData
from sims.sim_info import SimInfo


class SSAllowanceUtils:
    """ Utilities for allowances. """

    def is_allowed_everything(self, sim_info: SimInfo) -> bool:
        """ Determine if the Sim is allowed to perform everything. """
        data_store = SSSimData(sim_info)
        return len(data_store.allowances) == len(self.get_allowance_data())

    def set_allow_all(self, sim_info: SimInfo):
        """ Allow a Sim to perform all tasks. Typically done when they are not being controlled. """
        for allowance in self.get_allowance_data():
            allowance.add_allowance(sim_info)

    def set_disallow_all(self, sim_info: SimInfo):
        """ Disallow a Sim to perform all tasks. """
        data_store = SSSimData(sim_info)
        data_store.allowances = tuple()

    def get_allowance_data(self) -> Tuple[SSAllowanceData]:
        """ Retrieve a collection of allowance data. """
        result: Tuple[SSAllowanceData] = tuple([
            SSAllowedBartending(),
            SSAllowedBathing(),
            SSAllowedCake(),
            SSAllowedCallToMeal(),
            SSAllowedCleaning(),
            SSAllowedComputer(),
            SSAllowedCooking(),
            SSAllowedDancing(),
            SSAllowedEating(),
            SSAllowedFrontDesk(),
            SSAllowedGrabSnack(),
            SSAllowedGuest(),
            SSAllowedHiredWorker(),
            SSAllowedHost(),
            SSAllowedNotDuringWork(),
            SSAllowedNotDuringWorkLunch(),
            SSAllowedPhone(),
            SSAllowedPhoneGames(),
            SSAllowedPlaying(),
            SSAllowedPlayingInstruments(),
            SSAllowedReadBook(),
            SSAllowedServiceNpc(),
            SSAllowedShower(),
            SSAllowedSinging(),
            SSAllowedSleeping(),
            SSAllowedSocial(),
            SSAllowedStereo(),
            SSAllowedTip(),
            SSAllowedTouching(),
            SSAllowedTrash(),
            SSAllowedTvWatching(),
            SSAllowedView(),
            SSAllowedVisitor(),
            SSAllowedWork(),
            SSAllowedWorkout()
        ])
        return result
