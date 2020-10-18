"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict, Set

from cnsimsnatcher.cas_parts.cas_part_query_registry import SSCASPartQueryRegistry
from cnsimsnatcher.dtos.cas_parts.cas_part import SSCASPart
from sims4.commands import Command, CommandType, CheatOutput
from cnsimsnatcher.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'ss_cas_part_query')


@Command('ss.log_cas_part_tags', command_type=CommandType.Live)
def _ss_command_log_cas_part_tags(_connection: int=None):
    output = CheatOutput(_connection)
    output('Logging CAS Part tags, this will take awhile and your game may freeze. Be Patient!')
    try:
        log.enable()
        cas_part_results = []
        for cas_part_tag_value in SSCASPartQueryRegistry()._cas_part_library.keys():
            cas_parts = SSCASPartQueryRegistry()._cas_part_library[cas_part_tag_value]
            count = len(cas_parts)
            cas_part_result = {
                'tag_type': str(cas_part_tag_value),
                'count': count,
            }
            cas_part_results.append(cas_part_result)
        sorted_cas_parts = sorted(cas_part_results, key=lambda res: res['tag_type'])
        log.debug('<CAS Part Tag>: <Count>')
        for cas_part in sorted_cas_parts:
            log.debug('{}: {}'.format(cas_part['tag_type'], cas_part['count']))
        log.disable()
        output('CAS Part Tags logged')
    except Exception as ex:
        log.error('Something happened', exception=ex)
        output('Failed to log CAS Part tags.')


@Command('ss.log_cas_part_counts', command_type=CommandType.Live)
def _ss_command_log_cas_parts_counts(cas_parts_count: int=5, _connection: int=None):
    output = CheatOutput(_connection)
    output('Logging CAS Parts, this will take awhile and your game may freeze. Be Patient!')
    output('Will print pretty printed CAS Parts when the total count of them in a filter is less than {}'.format(cas_parts_count))
    try:
        log.enable()
        cas_part_results = []
        for cas_part_tag_value in SSCASPartQueryRegistry()._cas_part_library.keys():
            cas_parts: Set[SSCASPart] = SSCASPartQueryRegistry()._cas_part_library[cas_part_tag_value]
            count = len(cas_parts)
            cas_part_result = {
                'filter_key': cas_part_tag_value,
                'count': count,
                'cas_parts': tuple()
            }
            if count < cas_parts_count:
                cas_part_result['cas_parts'] = cas_parts
            cas_part_results.append(cas_part_result)
        sorted_cas_parts = sorted(cas_part_results, key=lambda res: res['filter_key'])
        for cas_part in sorted_cas_parts:
            log.format(filter_key=cas_part['filter_key'], count=cas_part['count'], cas_parts=cas_part['cas_parts'])
        log.disable()
        output('CAS Parts logged')
    except Exception as ex:
        log.error('Something happened', exception=ex)
        output('Failed to log.')


@Command('ss.log_cas_parts_for_author', command_type=CommandType.Live)
def _ss_command_log_cas_parts_for_author(author: str=None, _connection: int=None):
    output = CheatOutput(_connection)
    output('Logging CAS Parts, this will take awhile and your game may freeze. Be Patient!')
    if author is None:
        output('Please specify an author to locate CAS Parts for.')
        return
    output('Will print pretty printed CAS Parts when the author is the one specified {} (It wont work for authors with spaces in their names).'.format(author))
    try:
        log.enable()
        cas_parts_to_log: Dict[str, Any] = {}
        for cas_part_tag_value in SSCASPartQueryRegistry()._cas_part_library.keys():
            cas_parts: Set[SSCASPart] = SSCASPartQueryRegistry()._cas_part_library[cas_part_tag_value]
            for cas_part in cas_parts:
                if str(author).lower() != str(cas_part.author).lower():
                    continue
                cas_part_identifier = str(cas_part.unique_identifier)
                if cas_part_identifier in cas_parts_to_log:
                    if cas_part_tag_value in cas_parts_to_log[cas_part_identifier]['filter_keys']:
                        continue
                    cas_parts_to_log[cas_part_identifier]['filter_keys'].append(cas_part_tag_value)
                    continue
                cas_parts_to_log[cas_part_identifier] = {
                    'cas_part': cas_part,
                    'filter_keys': [cas_part_tag_value]
                }
        log.debug('Logging CAS Parts for author {}:'.format(author))
        for (key, val) in cas_parts_to_log.items():
            log.format(cas_part=val['cas_part'], filter_keys=val['filter_keys'])
        log.disable()
        output('CAS Parts logged')
    except Exception as ex:
        log.error('Something happened', exception=ex)
        output('Failed to log.')
