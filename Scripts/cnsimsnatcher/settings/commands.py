"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.modinfo import ModInfo
from sims4.commands import Command, CommandType, CheatOutput
from ssutilities.commonlib.data_management.common_persisted_data_manager import CommonPersistedDataManager


@Command('ss.clear_data', command_type=CommandType.Live)
def _ss_command_clear_data(*args, _connection: int=None):
    output = CheatOutput(_connection)
    from ssutilities.commonlib.data_management.data_manager_registry import CommonDataManagerRegistry
    data_managers = CommonDataManagerRegistry.get().get_data_managers(ModInfo.get_identity())
    data_manager_names = []
    for data_manager in data_managers:
        if not hasattr(data_manager, 'remove'):
            continue
        data_manager_names.append(data_manager.name)
    if len(args) <= 0:
        output('Missing arguments, valid arguments:')
        output('ss.clear_data <{}>'.format('/'.join(data_manager_names)))
        return
    data_manager_name = args[0].lower()
    data_manager = CommonDataManagerRegistry.get().locate_data_manager(ModInfo.get_identity(), data_manager_name)
    if data_manager is None or not hasattr(data_manager, 'remove'):
        output('Data with name \'{}\' does not exist.'.format(data_manager_name))
        output('Valid names:')
        output('ss.clear_data <{}>'.format('/'.join(data_manager_names)))
        return
    data_manager: CommonPersistedDataManager = data_manager
    data_manager.remove()
    output('!!! PLEASE READ !!!')
    output('Data with name \'{}\' has been cleared, but saving the game will recreate it.'.format(data_manager_name))
    output('To properly reset the data you must exit the game RIGHT NOW WITHOUT SAVING!')
    output('!!!!!!!!!!!!!!!!!!!')
