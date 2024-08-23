import unittest
from funcnodes_basic import lists


class TestListsMethods(unittest.IsolatedAsyncioTestCase):
    async def test_list_getindex(self):
        testlist = [1, 2, 3]

        node = lists.GetIndexNode()

        node.inputs["inputlist"].value = testlist
        node.inputs["index"].value = 1
        await node

        self.assertEqual(node.outputs["element"].value, 2)

    async def test_list_contains(self):
        testlist = [1, 2, 3]

        node = lists.contains()

        node.inputs["collection"].value = testlist
        node.inputs["item"].value = 2
        await node

        self.assertEqual(node.outputs["out"].value, True)
