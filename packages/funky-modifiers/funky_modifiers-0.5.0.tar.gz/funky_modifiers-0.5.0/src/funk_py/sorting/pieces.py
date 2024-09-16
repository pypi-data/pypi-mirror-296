import json
from copy import deepcopy
from enum import Enum
from typing import Mapping, Any, Literal, Union, List, Tuple, Optional, Iterator, Generator, \
    Callable
from urllib.parse import parse_qs

import yaml

from funk_py.modularity.decoration.enums import converts_enums
from funk_py.modularity.logging import make_logger
from funk_py.sorting.converters import csv_to_json, xml_to_json, wonky_json_to_json, jsonl_to_json
from funk_py.sorting.dict_manip import convert_tuplish_dict, get_subset_values, get_subset

main_logger = make_logger('pieces', 'PIECES_LOG_LEVEL', default_level='warning')

main_logger.info('Setting up simple types...')
OutputMapSpecifier = Literal['json', 'jsonl', 'json\'',
                             'xml', 'xml-sa',
                             'e-list', 'list',
                             'csv',
                             'yaml',
                             'tuple-dict',
                             'form-urlencoded',
                             'combinatorial', 'tandem', 'reduce', 'accumulate']
PickProcessFunc = Callable[[list, list, dict], None]
PickFinalFunc = Callable[[list, dict], None]


class PickType(Enum):
    """``PickType`` is an enum containing the valid pick types for :func:`pick`."""
    COMBINATORIAL = 'combinatorial'
    TANDEM = 'tandem'
    REDUCE = 'reduce'
    ACCUMULATE = 'accumulate'


class PickInstruction(Enum):
    JSON = 'json'
    JSONL = 'jsonl'
    JSON_SINGLE_QUOTE = 'json\''
    XML = 'xml'
    XMLSA = 'xml-sa'
    ELIST = 'e-list'
    LIST = 'list'
    CSV = 'csv'
    YAML = 'yaml'
    TUPLE_DICT = 'tuple-dict'
    FORM = 'form-urlencoded'

    COMBINATORIAL = 'combinatorial'
    TANDEM = 'tandem'
    REDUCE = 'reduce'
    ACCUMULATE = 'accumulate'


OutputMapType = Union[Mapping[str, Union[str, Mapping, PickInstruction]],
                      List[Union[str, Mapping, PickInstruction]]]


main_logger.info('Finished setting up simple types.')


def _com_tan_start_and_list_func(ans: list, builder: list, static_builder: dict) -> None:
    builder.extend(ans)


def _acc_start_list_and_iter_func(ans: list, builder: list, static_builder: dict) -> None:
    if not len(builder):
        builder.extend(ans)

    else:
        for _ans in ans:
            for k, v in _ans.items():
                if k in builder[0]:
                    if isinstance(v, list):
                        builder[0][k].extend(v)

                    else:
                        builder[0][k].append(v)

                elif isinstance(v, list):
                    builder[0][k] = v

                else:
                    builder[0][k] = [v]


def _com_iter_func(ans: list, builder: list, static_builder: dict) -> None:
    if (t := len(ans)) >= 1:
        for i in range(len(builder)):
            for _ans in ans[1:]:
                copier = builder[i].copy()
                copier.update(_ans)
                builder.append(copier)

            builder[i].update(ans[0])

    elif t == 1:
        for source in builder:
            source.update(ans[0])


def _tan_iter_func(ans: list, builder: list, static_builder: dict) -> None:
    if len(ans) == 0:
        return

    if len(builder) >= len(ans):
        for i in range(len(ans)):
            builder[i].update(ans[i])

    else:
        for i in range(len(builder)):
            builder[i].update(ans[i])

        for i in range(len(builder), len(ans)):
            builder.append(ans[i])


def _com_tan_final_func(builder: list, static_builder: dict) -> None:
    for result in builder:
        result.update(static_builder)


def _acc_final_func(builder: list, static_builder: dict) -> None:
    if not len(builder):
        builder.append(static_builder)

    else:
        for k, v in static_builder.items():
            if k in builder[0]:
                if isinstance(v, list):
                    builder[0][k].extend(v)

                else:
                    builder[0][k].append(v)

            elif isinstance(v, list):
                builder[0][k] = v

            else:
                builder[0][k] = [v]


_PICK_TYPE_DEFS = {
    PickType.COMBINATORIAL: (
        _com_tan_start_and_list_func,
        _com_tan_start_and_list_func,
        _com_iter_func,
        _com_tan_final_func,
    ),
    PickType.TANDEM: (
        _com_tan_start_and_list_func,
        _com_tan_start_and_list_func,
        _tan_iter_func,
        _com_tan_final_func,
    ),
    PickType.REDUCE: (
        _com_tan_start_and_list_func,
        _tan_iter_func,
        _com_iter_func,
        _com_tan_final_func,
    ),
    PickType.ACCUMULATE: (
        _acc_start_list_and_iter_func,
        _acc_start_list_and_iter_func,
        _acc_start_list_and_iter_func,
        _acc_final_func,
    ),
}
_PICK_TYPE_NAMES = {
    'combinatorial': _PICK_TYPE_DEFS[PickType.COMBINATORIAL],
    'tandem': _PICK_TYPE_DEFS[PickType.TANDEM],
    'reduce': _PICK_TYPE_DEFS[PickType.REDUCE],
    'accumulate': _PICK_TYPE_DEFS[PickType.ACCUMULATE],
}


def pick(
        output_map: OutputMapType,
        _input: Any,
        list_handling_method: PickType = PickType.COMBINATORIAL
) -> list:
    return _pick(output_map, _input, *_PICK_TYPE_DEFS[list_handling_method])


def _pick_setup(
        output_map: OutputMapType,
        _input: Any
) -> Tuple[Optional[OutputMapType], Any, list, bool, Optional[PickType]]:
    if isinstance(output_map, list):
        # If the output_map is a list, that should mean the user specified a type of conversion to
        # enact on the input (as long as their output_map is valid).
        if isinstance(_input, list) and output_map[0] != 'e-list':
            # In the case that _input is a list, we should first check if the user specified e-list
            # since that means "expected list". If they did specify that, we'll want to consume it,
            # so this branch won't execute, and we'll move over to the next step. If they didn't, we
            # continue on our mary way, and don't move forward on the output_map yet. We want to
            # pass the non-mutated _input as well since there's no mutation to be performed on it.
            return output_map, _input, [], False, None

        else:
            # In the case that _input is not a list, we will just attempt to parse as the user
            # expected.
            try:
                if (t := output_map[0]) in _PICK_TYPE_NAMES:
                    # This should handle cases where the user specifies changing modes during
                    # parsing.
                    return output_map[-1], _input, [], False, _PICK_TYPE_NAMES[t]

                worker = parse_type_as(output_map[0], _input, output_map[1:-1])

            except Exception as e:
                main_logger.warning(f'User\'s expected parsing method failed. Exception raised: '
                                    f'{e}')
                return None, None, [], True, None

            return output_map[-1], worker, [], False, None

    elif isinstance(output_map, str):
        # Theoretically, we should never get here, but just in case, this line should catch
        # instances where a key is immediately requested. Who knows, maybe a change down the line
        # will cause this code to be needed.
        return None, None, [{output_map: _input}], False, None

    # If nothing caught, just pass everything back as-is.
    return output_map, _input, [], False, None


def _find_and_follow_first_path_in_pick(
        output_map_iter: Iterator,
        worker: Any,
        builder: list,
        static_builder: dict
) -> Tuple[Optional[OutputMapType], Any, bool]:
    while True:
        try:
            path, instruction = next(output_map_iter)
            if not isinstance(worker, dict):
                main_logger.warning(f'An unexpected value was encountered in pick attempt. a path '
                                    f'has now been skipped. value = {worker}')
                return None, None, True

            if path in worker:
                if isinstance(instruction, str):
                    static_builder[instruction] = worker[path]
                    builder.append({})
                    # The caller doesn't need to call anything, we did everything needed for the
                    # first key.
                    return None, None, False

                else:
                    # Rather than recursively calling a function from inside of this function, we
                    # pass back the values that the caller needs to use to call the function itself.
                    # This is done this way to limit how deep we go on the stack. It also means the
                    # caller can decide which function to call on the values.
                    if isinstance(worker, dict):
                        return instruction, worker[path], False

                    main_logger.warning(f'Path ended early. {repr(worker)} does not have keys.')

        except StopIteration:
            # Welp, the caller will have to return immediately, none of the paths requested were
            # present.
            return None, None, True


def _pick_iter(
        output_map_iter: Iterator,
        worker: Any,
        builder: list,
        static_builder: dict,
        func: Callable[[list, list, dict], None]
) -> Generator[Tuple[Optional[OutputMapType], Any, bool], list, None]:
    """
    Finishes iterating after the first path was successfully followed. Expects the result of an
    external function call to be sent to it if it yields an instruction.
    """
    if type(worker) is dict:
        for path, instruction in output_map_iter:
            if path in worker:
                if isinstance(instruction, str):
                    static_builder[instruction] = worker[path]

                else:
                    # Rather than recursively calling a function from inside of this function, we
                    # pass back the values that the caller needs to use to call the function itself.
                    # This is done this way to limit how deep we go on the stack. It also means the
                    # caller can decide which function to call on the values.
                    # The caller should send the result of the function back to us here so that we
                    # can call func on it.
                    result = yield instruction, worker[path], False
                    try:
                        func(result, builder, static_builder)

                    except Exception as e:
                        main_logger.warning(f'There was an error when attempting to process a '
                                            f'result. Exception raised: {e}')

    else:
        main_logger.warning(f'Cannot follow a path in a non-dict. ({worker})')

    yield None, None, True


def _pick(
        output_map: OutputMapType,
        _input: Any,
        start_func: PickProcessFunc,
        list_func: PickProcessFunc,
        iter_func: PickProcessFunc,
        final_func: PickFinalFunc
) -> list:
    """
    The core of :func:`pick`. All pick types run through this method.

    :param output_map: The map which describes how incoming data should be parsed.
    :param _input: The incoming data.
    :param start_func: The function that should be used when parsing a list of results for ingestion
        into the list being built.
    :param iter_func: The function that should be used to parse a list of results during iteration
        over the ``output_map``.
    :param final_func: The function which should be called to finalize the result at the end of
        retrieving all possible data.
    :return:
    """
    static_builder = {}
    output_map, worker, builder, fail, new_mode = _pick_setup(output_map, _input)
    if fail or len(builder):
        return builder

    elif new_mode is not None:
        start_func, list_func, iter_func, final_func = new_mode

    __pick = lambda o_map, w: _pick(o_map, w, start_func, list_func, iter_func, final_func)  # noqa

    if isinstance(worker, list):
        for item in worker:
            list_func(__pick(output_map, item), builder, static_builder)

    else:
        output_map_iter = iter(output_map.items())
        *instruction, return_now = _find_and_follow_first_path_in_pick(
            output_map_iter, worker, builder, static_builder)
        if return_now:
            return builder

        elif instruction[0] is not None:
            # If instructions were given by _find_and_follow_first_path_in_pick, then we need to
            # recursively call this function with the results.
            start_func(__pick(*instruction), builder, static_builder)

        pick_iter = _pick_iter(output_map_iter, worker, builder, static_builder, iter_func)

        for *instruction, return_now in pick_iter:
            if instruction[0] is not None:
                # If instructions were given by pick_iter, then we need to recursively call this
                # function and pass the results back to pick_iter.
                pick_iter.send(__pick(*instruction))

        final_func(builder, static_builder)

    return builder


@converts_enums
def parse_type_as(_type: PickInstruction, data: Any, args: list) -> Union[dict, list]:
    switch = {
        PickInstruction.JSON: lambda x: json.loads(x),
        PickInstruction.JSONL: jsonl_to_json,
        PickInstruction.JSON_SINGLE_QUOTE: wonky_json_to_json,
        PickInstruction.XML: xml_to_json,
        PickInstruction.XMLSA: lambda x: xml_to_json(x, True),
        PickInstruction.ELIST: lambda x: x if isinstance(x, list) else [x],
        PickInstruction.CSV: csv_to_json,
        PickInstruction.LIST: lambda x: x.split(','),
        PickInstruction.YAML: yaml.safe_load,
        PickInstruction.FORM: parse_qs,
    }

    arg_switch = {
        PickInstruction.TUPLE_DICT: _parse_and_execute_tuplish,
    }

    if _type in switch:
        return switch[_type](data)

    elif _type in arg_switch:
        return arg_switch[_type](data, args)

    raise ValueError('Invalid type specified.')


def _parse_and_execute_tuplish(data: Union[dict, list], args: list) -> dict:
    if len(args):
        args = args[0]
        if isinstance(args, dict):
            return convert_tuplish_dict(data, args.get('pair_name'),
                                        args.get('key_name'), args.get('val_name'))

        else:
            raise ValueError('TUPLE_DICT given an invalid argument format.')

    else:
        return convert_tuplish_dict(data)


def fracture(
        data: List[dict],
        *keys: str,
        inplace: bool = True
) -> Generator[Tuple[dict, List[dict]], None, None]:
    """
    Separates a list of dictionaries into sets based on the values of a subset of keys and returns
    each set one at a time.

    :param data: The List to fracture.
    :type data: List[dict]
    :param keys: The subset of keys which should be used to differentiate between items in ``data``.
    :type keys: str
    :param inplace: Whether values returned should literally be the original values from the list or
        should be copies of those values, set to ``False`` if you wish to avoid mutating the
        original values in ``data``.
    :type inplace: bool
    :return: A ``Generator`` which iterates through each subset of ``data`` one at a time, basing
        the subsets off of ``keys``.
    """
    # Choose the function we use to append values based on inplace.
    # Choose it early since checking inplace inside the loop adds up on time.
    if inplace:
        def app_func(builder: List[dict], val: dict):
            return builder.append(val)

    else:
        def app_func(builder: List[dict], val: dict):
            return builder.append(deepcopy(val))

    # Then just generate.
    for subset in _iter_fracture(data, keys, app_func):
        yield subset


def _iter_fracture(
        data: List[dict],
        keys: Tuple[str, ...],
        app_func: Callable[[List[dict], dict], None]
) -> Generator[Tuple[dict, List[dict]], None, None]:
    # The following two objects will be used to reduce repetitive calculations.
    calc = [None] * len(data)
    done = [False] * len(data)
    for i, val in enumerate(data):
        # Quite simply, don't generate a new list for something already included in a list.
        if not done[i]:
            builder = []
            def1 = get_subset_values(val, *keys) if calc[i] is None else calc[i]
            mark = get_subset(val, *keys)
            app_func(builder, val)
            for j, _val in enumerate(data)[i + 1:]:
                if calc[j] is None:
                    def2 = get_subset_values(_val, *keys) if calc[j] is None else calc[j]
                    calc[j] = def2

                else:
                    def2 = calc[j]

                if def1 == def2:
                    app_func(builder, val)
                    done[j] = True

            yield mark, builder


def translate(data: List[dict], translators: Mapping[Any, Callable[[dict], Any]],
              default: Any = ..., inplace: bool = True) -> List[dict]:
    """
    Translate values in data based on given translators.

    :param data: Dictionaries to translate.
    :type data: List[dict]
    :param translators: A dictionary of keys and functions used to translate values at those keys.
    :type translators: Mapping[Any, Callable[[dict], Any]]
    :param default: A default value to use for keys that don't exist. If this is not specified,
        missing keys will simply be ignored.
    :type default: Any
    :param inplace: Whether to mutate ``data`` or not. Defaults to ``True``.
    :type inplace: bool
    :return: A list of the dictionaries in ``data`` mutated based on the functions in
        ``translators``.
    """
    # Much more efficient to check inplace outside the loop.
    if inplace:
        for v in data:
            for k, trans in translators.items():
                if k in v:
                    v[k] = trans(v[k])

                elif default is not ...:
                    v[k] = default

        return data

    output = []
    for v in data:
        output.append(builder := deepcopy(v))
        for k, trans in translators.items():
            if k in v:
                builder[k] = trans(v[k])

            elif default is not ...:
                builder[k] = default

    return output
