import unittest
from funcnodes_basic import dicts


class TestStringMethods(unittest.IsolatedAsyncioTestCase):
    async def test_get(self):
        testdict = {"a": 1, "b": 2, "c": 3}

        node = dicts.DictGetNode()

        node.inputs["dictionary"].value = testdict
        await node

        self.assertEqual(
            node.inputs["key"].value_options["options"], {0: "a", 1: "b", 2: "c"}
        )

        node.inputs["key"].value = 0
        await node

        self.assertEqual(node.outputs["value"].value, 1)
