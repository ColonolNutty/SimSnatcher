from cnsimsnatcher.configuration.allowance.allowances.allowance import SSAllowanceData
from cnsimsnatcher.configuration.allowance.enums.string_ids import SSAllowanceStringId
from cnsimsnatcher.configuration.allowance.enums.trait_ids import SSAllowanceTraitId


class SSAllowedPhone(SSAllowanceData):
    """ Data for an allowance. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def title(self) -> int:
        return SSAllowanceStringId.ALLOWED_PHONE

    # noinspection PyMissingOrEmptyDocstring
    @property
    def trait_id(self) -> int:
        return SSAllowanceTraitId.ALLOWED_PHONE
