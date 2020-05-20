"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.order_to.settings.data.manager import SSOrderToSettingsManager
from ssutilities.commonlib.data_management.data_manager_registry import CommonDataManagerRegistry


CommonDataManagerRegistry.register_data_manager(SSOrderToSettingsManager())