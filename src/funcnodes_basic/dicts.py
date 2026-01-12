"""
work with python dictionaries
"""

import funcnodes_core as fn
from typing import Any, List, Tuple, Annotated, Literal


class DictGetNode(fn.Node):
    node_id = "dict_get"
    node_name = "Dict Get"
    dictionary = fn.NodeInput(id="dictionary", type=dict)
    key = fn.NodeInput(id="key", type=str)
    value = fn.NodeOutput(id="value", type=Any)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._keymap = {}
        self.get_input("dictionary").on("after_set_value", self._update_keys)

    def _update_keys(self, **kwargs):
        try:
            d = self.get_input("dictionary").value
            keys = list(d.keys())
        except KeyError:
            return
        keymap = dict({str(i): k for i, k in enumerate(keys)})
        reversed_keymap = {v: k for k, v in keymap.items()}
        self.get_input("key").update_value_options(options=reversed_keymap)
        self._keymap = keymap

    async def func(self, dictionary: dict, key: str) -> None:
        try:
            v = dictionary[self._keymap[key]]
        except KeyError:
            try:
                v = dictionary[key]
            except KeyError:
                v = fn.NoValue
        self.outputs["value"].value = v
        return v


@fn.NodeDecorator(
    id="dict_keys",
    name="Dict Keys",
)
def dict_keys(dictionary: dict) -> List[Any]:
    return list(dictionary.keys())


@fn.NodeDecorator(
    id="dict_values",
    name="Dict Values",
)
def dict_values(dictionary: dict) -> List[Any]:
    return list(dictionary.values())


@fn.NodeDecorator(
    id="dict_items",
    name="Dict Items",
)
def dict_items(dictionary: dict) -> List[tuple]:
    return list(dictionary.items())


@fn.NodeDecorator(
    id="dict_from_items",
    name="Dict From Items",
)
def dict_from_items(items: List[tuple]) -> dict:
    return dict(items)


@fn.NodeDecorator(
    id="dict_from_keys_values",
    name="Dict From Keys Values",
)
def dict_from_keys_values(keys: List[Any], values: List[Any]) -> dict:
    return dict(zip(keys, values))


@fn.NodeDecorator(
    id="dict_to_lists",
    name="Dict to List",
    outputs=[
        {"name": "keys"},
        {
            "name": "values",
        },
    ],
)
def dict_to_list(dictionary: dict) -> Tuple[List[Any], List[Any]]:
    keys, values = zip(*dictionary.items())
    return list(keys), list(values)


@fn.NodeDecorator(
    id="dict_set_default",
    name="Dict Set Default",
)
def dict_set_default(dictionary: dict, key: Any, value: Any) -> dict:
    result = dict(dictionary)
    if key not in result:
        result[key] = value
    return result


@fn.NodeDecorator(
    id="dict_set_key",
    name="Dict Set Key",
)
def dict_set_key(dictionary: dict, key: Any, value: Any) -> dict:
    result = dict(dictionary)
    result[key] = value
    return result


@fn.NodeDecorator(
    id="dict_merge",
    name="Dict Merge",
)
def dict_merge(
    a: dict,
    b: dict,
    prefer: Annotated[Literal["a", "b"], fn.InputMeta(hidden=True)] = "b",
) -> dict:
    if prefer == "a":
        return {**b, **a}
    return {**a, **b}


@fn.NodeDecorator(
    id="dict_select_keys",
    name="Dict Select Keys",
)
def dict_select_keys(
    dictionary: Annotated[
        dict,
        fn.InputMeta(
            on={
                "after_set_value": fn.decorator.update_other_io_options(
                    "keys", lambda x: list(x.keys())
                )
            }
        ),
    ],
    keys: List[Any],
    ignore_missing: bool = True,
) -> dict:
    selected: dict = {}
    for key in keys:
        if key in dictionary:
            selected[key] = dictionary[key]
        elif not ignore_missing:
            raise KeyError(key)
    return selected


@fn.NodeDecorator(
    id="dict_rename_key",
    name="Dict Rename Key",
)
def dict_rename_key(
    dictionary: Annotated[
        dict,
        fn.InputMeta(
            on={
                "after_set_value": fn.decorator.update_other_io_options(
                    "old_key", lambda x: list(x.keys())
                )
            }
        ),
    ],
    old_key: Any,
    new_key: Any,
    overwrite: bool = False,
) -> dict:
    if old_key == new_key:
        return dict(dictionary)

    result = dict(dictionary)
    if old_key not in result:
        raise KeyError(old_key)
    if new_key in result and not overwrite:
        raise KeyError(new_key)

    result[new_key] = result.pop(old_key)
    return result


@fn.NodeDecorator(
    id="dict_delete_key",
    name="Dict Delete Key",
)
def dict_delete_key(
    dictionary: Annotated[
        dict,
        fn.InputMeta(
            on={
                "after_set_value": fn.decorator.update_other_io_options(
                    "key", lambda x: list(x.keys())
                )
            }
        ),
    ],
    key: Any,
    ignore_missing: bool = True,
) -> dict:
    result = dict(dictionary)
    if key in result:
        del result[key]
    elif not ignore_missing:
        raise KeyError(key)
    return result


@fn.NodeDecorator(
    id="dict_pop",
    name="Dict Pop",
    outputs=[
        {"name": "new_dict"},
        {"name": "value"},
    ],
)
def dict_pop(
    dictionary: Annotated[
        dict,
        fn.InputMeta(
            on={
                "after_set_value": fn.decorator.update_other_io_options(
                    "key", lambda x: list(x.keys())
                )
            }
        ),
    ],
    key: Any,
    default: Any = fn.NoValue,
) -> Tuple[dict, Any]:
    result = dict(dictionary)
    if key in result:
        value = result.pop(key)
        return result, value
    if default is fn.NoValue or default == str(fn.NoValue):
        raise KeyError(key)
    return result, default


@fn.NodeDecorator(
    id="dict_deep_get",
    name="Dict Deep Get",
)
def dict_deep_get(obj: Any, path: List[Any]) -> Any:
    current = obj
    for key in path:
        if isinstance(current, dict):
            if key in current:
                current = current[key]
            else:
                return fn.NoValue
        elif isinstance(current, (list, tuple)):
            if isinstance(key, int):
                index = key
            elif isinstance(key, str) and key.lstrip("-").isdigit():
                index = int(key)
            else:
                return fn.NoValue
            if -len(current) <= index < len(current):
                current = current[index]
            else:
                return fn.NoValue
        else:
            return fn.NoValue
    return current


@fn.NodeDecorator(
    id="dict_deep_set",
    name="Dict Deep Set",
)
def dict_deep_set(
    dictionary: dict,
    path: List[Any],
    value: Any,
    create_missing: bool = True,
) -> dict:
    if not path:
        raise ValueError("path must not be empty")

    if not isinstance(dictionary, dict):
        raise TypeError("dictionary must be a dict")

    result = dict(dictionary)
    current = result

    for key in path[:-1]:
        if key in current:
            next_value = current[key]
            if not isinstance(next_value, dict):
                raise TypeError(
                    f"Expected dict at path segment '{key}', got {type(next_value)}"
                )
            next_dict = dict(next_value)
        else:
            if not create_missing:
                raise KeyError(key)
            next_dict = {}

        current[key] = next_dict
        current = next_dict

    current[path[-1]] = value
    return result


NODE_SHELF = fn.Shelf(
    nodes=[
        DictGetNode,
        dict_keys,
        dict_values,
        dict_items,
        dict_from_items,
        dict_from_keys_values,
        dict_to_list,
        dict_set_default,
        dict_set_key,
        dict_merge,
        dict_select_keys,
        dict_rename_key,
        dict_delete_key,
        dict_pop,
        dict_deep_get,
        dict_deep_set,
    ],
    name="Dicts",
    description="Work with dictionaries",
    subshelves=[],
)
