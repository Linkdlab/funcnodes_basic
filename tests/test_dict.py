from funcnodes_basic import dicts
import pytest_funcnodes
import pytest
import funcnodes_core as fn
# DictGetNode,
# dict_keys,
# dict_values,
# dict_items,
# dict_from_items,
# dict_from_keys_values,
# dict_to_list,


@pytest_funcnodes.nodetest(dicts.DictGetNode)
async def test_dict_get():
    testdict = {"a": 1, "b": 2, "c": 3}

    node = dicts.DictGetNode()

    node.inputs["dictionary"].value = testdict
    await node

    assert node.inputs["key"].value_options["options"] == {"a": "0", "b": "1", "c": "2"}

    node.inputs["key"].value = "0"
    await node

    assert node.outputs["value"].value == 1


@pytest_funcnodes.nodetest(dicts.dict_keys)
async def test_dict_keys():
    testdict = {"a": 1, "b": 2, "c": 3}

    node = dicts.dict_keys()

    node.inputs["dictionary"].value = testdict
    await node

    assert node.outputs["out"].value == ["a", "b", "c"]


@pytest_funcnodes.nodetest(dicts.dict_values)
async def test_dict_values():
    testdict = {"a": 1, "b": 2, "c": 3}

    node = dicts.dict_values()

    node.inputs["dictionary"].value = testdict
    await node

    assert node.outputs["out"].value == [1, 2, 3]


@pytest_funcnodes.nodetest(dicts.dict_items)
async def test_dict_items():
    testdict = {"a": 1, "b": 2, "c": 3}

    node = dicts.dict_items()

    node.inputs["dictionary"].value = testdict
    await node

    assert node.outputs["out"].value == [("a", 1), ("b", 2), ("c", 3)]


@pytest_funcnodes.nodetest(dicts.dict_from_items)
async def test_dict_from_items():
    testitems = [("a", 1), ("b", 2), ("c", 3)]

    node = dicts.dict_from_items()

    node.inputs["items"].value = testitems
    await node

    assert node.outputs["out"].value == {"a": 1, "b": 2, "c": 3}


@pytest_funcnodes.nodetest(dicts.dict_from_keys_values)
async def test_dict_from_keys_values():
    testkeys = ["a", "b", "c"]
    testvalues = [1, 2, 3]

    node = dicts.dict_from_keys_values()

    node.inputs["keys"].value = testkeys
    node.inputs["values"].value = testvalues
    await node

    assert node.outputs["out"].value == {"a": 1, "b": 2, "c": 3}


@pytest_funcnodes.nodetest(dicts.dict_to_list)
async def test_dict_to_list():
    testdict = {"a": 1, "b": 2, "c": 3}

    node = dicts.dict_to_list()

    node.inputs["dictionary"].value = testdict
    await node

    assert node.outputs["keys"].value == ["a", "b", "c"]
    assert node.outputs["values"].value == [1, 2, 3]


@pytest_funcnodes.nodetest(dicts.dict_set_default)
async def test_dict_set_default_missing_key():
    testdict = {"a": 1}

    node = dicts.dict_set_default()

    node.inputs["dictionary"].value = testdict
    node.inputs["key"].value = "b"
    node.inputs["value"].value = 2
    await node

    assert node.outputs["out"].value == {"a": 1, "b": 2}


@pytest_funcnodes.nodetest(dicts.dict_set_default)
async def test_dict_set_default_existing_key():
    testdict = {"a": 1}

    node = dicts.dict_set_default()

    node.inputs["dictionary"].value = testdict
    node.inputs["key"].value = "a"
    node.inputs["value"].value = 2
    await node

    assert node.outputs["out"].value == {"a": 1}


@pytest_funcnodes.nodetest(dicts.dict_set_key)
async def test_dict_set_key_overwrite():
    testdict = {"a": 1}

    node = dicts.dict_set_key()

    node.inputs["dictionary"].value = testdict
    node.inputs["key"].value = "a"
    node.inputs["value"].value = 2
    await node

    assert node.outputs["out"].value == {"a": 2}


@pytest_funcnodes.nodetest(dicts.dict_set_key)
async def test_dict_set_key_new_key():
    testdict = {"a": 1}

    node = dicts.dict_set_key()

    node.inputs["dictionary"].value = testdict
    node.inputs["key"].value = "b"
    node.inputs["value"].value = 2
    await node

    assert node.outputs["out"].value == {"a": 1, "b": 2}


@pytest_funcnodes.nodetest(dicts.dict_merge)
async def test_dict_merge_prefer_b_default():
    a = {"a": 1, "x": 1}
    b = {"x": 2, "b": 2}

    node = dicts.dict_merge()
    node.inputs["a"].value = a
    node.inputs["b"].value = b
    await node

    assert node.outputs["out"].value == {"a": 1, "x": 2, "b": 2}
    assert a == {"a": 1, "x": 1}
    assert b == {"x": 2, "b": 2}


@pytest_funcnodes.nodetest(dicts.dict_merge)
async def test_dict_merge_prefer_a():
    a = {"a": 1, "x": 1}
    b = {"x": 2, "b": 2}

    node = dicts.dict_merge()
    node.inputs["a"].value = a
    node.inputs["b"].value = b
    node.inputs["prefer"].value = "a"
    await node

    assert node.outputs["out"].value == {"x": 1, "b": 2, "a": 1}


@pytest_funcnodes.nodetest(dicts.dict_select_keys)
async def test_dict_select_keys_basic_and_ignore_missing():
    testdict = {"a": 1, "b": 2}

    node = dicts.dict_select_keys()
    node.inputs["dictionary"].value = testdict
    assert node.inputs["keys"].value_options["options"] == ["a", "b"]
    node.inputs["keys"].value = ["b", "c", "a"]
    await node

    assert node.outputs["out"].value == {"b": 2, "a": 1}
    assert testdict == {"a": 1, "b": 2}


@pytest_funcnodes.nodetest(dicts.dict_select_keys)
async def test_dict_select_keys_missing_raises_when_not_ignored():
    node = dicts.dict_select_keys()
    node.inputs["dictionary"].value = {"a": 1}
    node.inputs["keys"].value = ["b"]
    node.inputs["ignore_missing"].value = False
    with pytest.raises(fn.NodeTriggerError):
        await node


@pytest_funcnodes.nodetest(dicts.dict_rename_key)
async def test_dict_rename_key_basic():
    node = dicts.dict_rename_key()
    node.inputs["dictionary"].value = {"a": 1}
    assert node.inputs["old_key"].value_options["options"] == ["a"]
    node.inputs["old_key"].value = "a"
    node.inputs["new_key"].value = "b"
    await node

    assert node.outputs["out"].value == {"b": 1}


@pytest_funcnodes.nodetest(dicts.dict_rename_key)
async def test_dict_rename_key_missing_old_raises():
    node = dicts.dict_rename_key()
    node.inputs["dictionary"].value = {"a": 1}
    node.inputs["old_key"].value = "missing"
    node.inputs["new_key"].value = "b"
    with pytest.raises(fn.NodeTriggerError):
        await node


@pytest_funcnodes.nodetest(dicts.dict_rename_key)
async def test_dict_rename_key_existing_new_key_requires_overwrite():
    node = dicts.dict_rename_key()
    node.inputs["dictionary"].value = {"a": 1, "b": 2}
    node.inputs["old_key"].value = "a"
    node.inputs["new_key"].value = "b"
    with pytest.raises(fn.NodeTriggerError):
        await node

    node.inputs["overwrite"].value = True
    await node
    assert node.outputs["out"].value == {"b": 1}


@pytest_funcnodes.nodetest(dicts.dict_delete_key)
async def test_dict_delete_key_basic_and_ignore_missing():
    node = dicts.dict_delete_key()
    node.inputs["dictionary"].value = {"a": 1}
    assert node.inputs["key"].value_options["options"] == ["a"]
    node.inputs["key"].value = "a"
    await node
    assert node.outputs["out"].value == {}

    node.inputs["dictionary"].value = {"a": 1}
    node.inputs["key"].value = "missing"
    await node
    assert node.outputs["out"].value == {"a": 1}


@pytest_funcnodes.nodetest(dicts.dict_delete_key)
async def test_dict_delete_key_missing_raises_when_not_ignored():
    node = dicts.dict_delete_key()
    node.inputs["dictionary"].value = {"a": 1}
    node.inputs["key"].value = "missing"
    node.inputs["ignore_missing"].value = False
    with pytest.raises(fn.NodeTriggerError):
        await node


@pytest_funcnodes.nodetest(dicts.dict_pop)
async def test_dict_pop_basic():
    testdict = {"a": 1, "b": 2}

    node = dicts.dict_pop()
    node.inputs["dictionary"].value = testdict
    assert node.inputs["key"].value_options["options"] == ["a", "b"]
    node.inputs["key"].value = "a"
    await node

    assert node.outputs["new_dict"].value == {"b": 2}
    assert node.outputs["value"].value == 1
    assert testdict == {"a": 1, "b": 2}


@pytest_funcnodes.nodetest(dicts.dict_pop)
async def test_dict_pop_missing_uses_default():
    node = dicts.dict_pop()
    node.inputs["dictionary"].value = {"a": 1}
    node.inputs["key"].value = "missing"
    node.inputs["default"].value = 123
    await node

    assert node.outputs["new_dict"].value == {"a": 1}
    assert node.outputs["value"].value == 123


@pytest_funcnodes.nodetest(dicts.dict_pop)
async def test_dict_pop_missing_without_default_raises():
    node = dicts.dict_pop()
    node.inputs["dictionary"].value = {"a": 1}
    node.inputs["key"].value = "missing"
    with pytest.raises(fn.NodeTriggerError):
        await node


@pytest_funcnodes.nodetest(dicts.dict_deep_get)
async def test_dict_deep_get_basic_and_missing():
    node = dicts.dict_deep_get()
    node.inputs["obj"].value = {"a": {"b": 2}}
    node.inputs["path"].value = ["a", "b"]
    await node
    assert node.outputs["out"].value == 2

    node.inputs["path"].value = ["a", "missing"]
    await node
    assert node.outputs["out"].value is fn.NoValue

    node.inputs["path"].value = []
    await node
    assert node.outputs["out"].value == {"a": {"b": 2}}


@pytest_funcnodes.nodetest(dicts.dict_deep_set)
async def test_dict_deep_set_basic_and_create_missing():
    testdict = {"a": {"b": 1}}

    node = dicts.dict_deep_set()
    node.inputs["dictionary"].value = testdict
    node.inputs["path"].value = ["a", "b"]
    node.inputs["value"].value = 2
    await node
    assert node.outputs["out"].value == {"a": {"b": 2}}
    assert testdict == {"a": {"b": 1}}

    node.inputs["dictionary"].value = {}
    node.inputs["path"].value = ["a", "b"]
    node.inputs["value"].value = 1
    await node
    assert node.outputs["out"].value == {"a": {"b": 1}}


@pytest_funcnodes.nodetest(dicts.dict_deep_set)
async def test_dict_deep_set_missing_raises_when_not_creating():
    node = dicts.dict_deep_set()
    node.inputs["dictionary"].value = {}
    node.inputs["path"].value = ["a", "b"]
    node.inputs["value"].value = 1
    node.inputs["create_missing"].value = False
    with pytest.raises(fn.NodeTriggerError):
        await node


@pytest_funcnodes.nodetest(dicts.dict_deep_set)
async def test_dict_deep_set_empty_path_raises():
    node = dicts.dict_deep_set()
    node.inputs["dictionary"].value = {"a": 1}
    node.inputs["path"].value = []
    node.inputs["value"].value = 2
    with pytest.raises(fn.NodeTriggerError):
        await node
