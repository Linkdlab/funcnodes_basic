import unittest
from funcnodes_basic import dicts

# DictGetNode,
# dict_keys,
# dict_values,
# dict_items,
# dict_from_items,
# dict_from_keys_values,
# dict_to_list,


class TestDictMethods(unittest.IsolatedAsyncioTestCase):
    async def test_dict_get(self):
        testdict = {"a": 1, "b": 2, "c": 3}

        node = dicts.DictGetNode()

        node.inputs["dictionary"].value = testdict
        await node

        self.assertEqual(
            node.inputs["key"].value_options["options"], {"a": "0", "b": "1", "c": "2"}
        )

        node.inputs["key"].value = "0"
        await node

        self.assertEqual(node.outputs["value"].value, 1)

    async def test_dict_keys(self):
        testdict = {"a": 1, "b": 2, "c": 3}

        node = dicts.dict_keys()

        node.inputs["dictionary"].value = testdict
        await node

        self.assertEqual(node.outputs["out"].value, ["a", "b", "c"])

    async def test_dict_values(self):
        testdict = {"a": 1, "b": 2, "c": 3}

        node = dicts.dict_values()

        node.inputs["dictionary"].value = testdict
        await node

        self.assertEqual(node.outputs["out"].value, [1, 2, 3])

    async def test_dict_items(self):
        testdict = {"a": 1, "b": 2, "c": 3}

        node = dicts.dict_items()

        node.inputs["dictionary"].value = testdict
        await node

        self.assertEqual(node.outputs["out"].value, [("a", 1), ("b", 2), ("c", 3)])

    async def test_dict_from_items(self):
        testitems = [("a", 1), ("b", 2), ("c", 3)]

        node = dicts.dict_from_items()

        node.inputs["items"].value = testitems
        await node

        self.assertEqual(node.outputs["out"].value, {"a": 1, "b": 2, "c": 3})

    async def test_dict_from_keys_values(self):
        testkeys = ["a", "b", "c"]
        testvalues = [1, 2, 3]

        node = dicts.dict_from_keys_values()

        node.inputs["keys"].value = testkeys
        node.inputs["values"].value = testvalues
        await node

        self.assertEqual(node.outputs["out"].value, {"a": 1, "b": 2, "c": 3})

    async def test_dict_to_list(self):
        testdict = {"a": 1, "b": 2, "c": 3}

        node = dicts.dict_to_list()

        node.inputs["dictionary"].value = testdict
        await node

        self.assertEqual(node.outputs["keys"].value, ["a", "b", "c"])
        self.assertEqual(node.outputs["values"].value, [1, 2, 3])
