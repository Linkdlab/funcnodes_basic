import unittest
from funcnodes_basic import lists

import funcnodes as fn

fn.config.IN_NODE_TEST = True


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

    async def test_to_list(self):
        node = lists.to_list()

        node.inputs["obj"].value = 1
        await node

        self.assertEqual(node.outputs["out"].value, [1])

    async def test_list_length(self):
        testlist = [1, 2, 3]

        node = lists.list_length()

        node.inputs["lst"].value = testlist
        await node

        self.assertEqual(node.outputs["out"].value, 3)

    async def test_list_append(self):
        testlist = [1, 2, 3]

        node = lists.list_append()

        node.inputs["lst"].value = testlist
        node.inputs["item"].value = 4
        await node

        self.assertEqual(node.outputs["out"].value, [1, 2, 3, 4])
        self.assertEqual(testlist, [1, 2, 3])

    async def test_list_extend(self):
        testlist = [1, 2, 3]

        node = lists.list_extend()

        node.inputs["lst"].value = testlist
        node.inputs["items"].value = [4, 5]
        await node

        self.assertEqual(node.outputs["out"].value, [1, 2, 3, 4, 5])
        self.assertEqual(testlist, [1, 2, 3])

    async def test_list_pop(self):
        testlist = [1, 2, 3]

        node = lists.list_pop()

        node.inputs["lst"].value = testlist
        node.inputs["index"].value = 1
        await node

        self.assertEqual(node.outputs["new_list"].value, [1, 3])
        self.assertEqual(testlist, [1, 2, 3])

        self.assertEqual(node.outputs["item"].value, 2)

    async def test_list_remove(self):
        testlist = [1, 2, 3, 3, 3]

        node = lists.list_remove()

        node.inputs["lst"].value = testlist
        node.inputs["item"].value = 3
        await node

        self.assertEqual(node.outputs["out"].value, [1, 2, 3, 3])
        self.assertEqual(testlist, [1, 2, 3, 3, 3])
        node.inputs["all"].value = True
        await node

        self.assertEqual(node.outputs["out"].value, [1, 2])
        self.assertEqual(testlist, [1, 2, 3, 3, 3])

    async def test_list_index(self):
        testlist = [1, 2, 3]

        node = lists.list_index()

        node.inputs["lst"].value = testlist
        node.inputs["item"].value = 2
        await node

        self.assertEqual(node.outputs["out"].value, 1)

    async def test_list_reverse(self):
        testlist = [1, 2, 3]

        node = lists.list_reverse()

        node.inputs["lst"].value = testlist
        await node

        self.assertEqual(node.outputs["out"].value, [3, 2, 1])
        self.assertEqual(testlist, [1, 2, 3])

    async def test_list_sort(self):
        testlist = [3, 2, 1]

        node = lists.list_sort()

        node.inputs["lst"].value = testlist
        await node

        self.assertEqual(node.outputs["out"].value, [1, 2, 3])
        self.assertEqual(testlist, [3, 2, 1])

        node.inputs["reverse"].value = True
        await node

        self.assertEqual(node.outputs["out"].value, [3, 2, 1])
        self.assertEqual(testlist, [3, 2, 1])

    async def test_list_count(self):
        testlist = [1, 2, 3, 3]

        node = lists.list_count()

        node.inputs["lst"].value = testlist
        node.inputs["item"].value = 3
        await node

        self.assertEqual(node.outputs["out"].value, 2)

    async def test_list_insert(self):
        testlist = [1, 2, 3]

        node = lists.list_insert()

        node.inputs["lst"].value = testlist
        node.inputs["index"].value = 1
        node.inputs["item"].value = 4
        await node

        self.assertEqual(node.outputs["out"].value, [1, 4, 2, 3])
        self.assertEqual(testlist, [1, 2, 3])

    async def test_list_set(self):
        testlist = [1, 2, 3]

        node = lists.list_set()

        node.inputs["lst"].value = testlist
        node.inputs["index"].value = 1
        node.inputs["item"].value = 4
        await node

        self.assertEqual(node.outputs["out"].value, [1, 4, 3])
        self.assertEqual(testlist, [1, 2, 3])

    async def test_list_slice(self):
        testlist = [1, 2, 3, 4]

        node = lists.list_slice()

        node.inputs["lst"].value = testlist
        node.inputs["start"].value = 1
        node.inputs["end"].value = 3
        await node

        self.assertEqual(node.outputs["out"].value, [2, 3])
        self.assertEqual(testlist, [1, 2, 3, 4])

    async def test_list_slice_step(self):
        testlist = [1, 2, 3, 4, 5]

        node = lists.list_slice_step()

        node.inputs["lst"].value = testlist
        node.inputs["start"].value = 1
        node.inputs["end"].value = 4
        node.inputs["step"].value = 2
        await node

        self.assertEqual(node.outputs["out"].value, [2, 4])
        self.assertEqual(testlist, [1, 2, 3, 4, 5])
