"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Iterator, Tuple

from sims.sim_info_types import Gender, Age
from sims4communitylib.enums.common_species import CommonSpecies


class DDCASPartAvailableFor:
    """ Holds information for what types of Sims a part is available for. """
    def __init__(
        self,
        genders: Iterator[Gender],
        ages: Iterator[Age],
        species: Iterator[CommonSpecies]
    ):
        self._genders = tuple(genders)
        self._ages = tuple(ages)
        self._species = tuple(species)

    @property
    def genders(self) -> Tuple[Gender]:
        """ Genders the part is available for. """
        return self._genders

    @property
    def ages(self) -> Tuple[Age]:
        """ Ages the part is available for. """
        return self._ages

    @property
    def species(self) -> Tuple[CommonSpecies]:
        """ Species the part is available for. """
        return self._species

    def is_valid(self) -> Tuple[bool, str]:
        """ Determine if the Available For is valid. """
        if len(self.genders) == 0 and len(self.ages) == 0 and len(self.species) == 0:
            return False, 'No Genders, Ages, nor Species were specified!'
        return True, 'Success'

    @staticmethod
    def everything() -> 'DDCASPartAvailableFor':
        """ Create an Available For instance that applies to everything. """
        return DDCASPartAvailableFor((Gender.MALE, Gender.FEMALE), (Age.BABY, Age.TODDLER, Age.CHILD, Age.TEEN, Age.YOUNGADULT, Age.ADULT, Age.ELDER), (CommonSpecies.HUMAN, CommonSpecies.SMALL_DOG, CommonSpecies.LARGE_DOG, CommonSpecies.CAT))

    def __repr__(self) -> str:
        return '<genders:{}, ages:{}, species:{}>'\
            .format(pformat(self.genders), pformat(self.ages), pformat(self.species))

    def __str__(self) -> str:
        return self.__repr__()
