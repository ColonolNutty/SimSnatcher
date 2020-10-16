"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.commands
from cnsimsnatcher.abduction.enums.skill_ids import SSAbductionSkillId
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_sim_skill_utils import CommonSimSkillUtils


@sims4.commands.Command('ss.set_abduction_skill', command_type=sims4.commands.CommandType.Live)
def _ss_abduction_command_set_sim_abduction_skill_level(*args, _connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_info = CommonSimUtils.get_active_sim_info()
    if len(args) < 1:
        output('ss.set_abduction_skill <level>')
        return
    try:
        level = int(args[0])
    except ValueError:
        output('Incorrect <level> variable!')
        return
    if level > 0:
        CommonSimSkillUtils.set_current_skill_level(sim_info, SSAbductionSkillId.ABDUCTION, level)
    else:
        CommonSimSkillUtils.remove_skill(sim_info, SSAbductionSkillId.ABDUCTION)
    output('Sim Abduction skill has been set to level {}.'.format(level))
