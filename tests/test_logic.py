import unittest
from funcnodes_basic import logic
from funcnodes_basic import math_nodes
import time
import funcnodes_core as fn


class TestLogicNodes(unittest.IsolatedAsyncioTestCase):
    async def test_if_node(self):
        node = logic.IfNode()

        # Test when condition is True
        node.inputs["condition"].value = True
        node.inputs["input"].value = "true_value"
        await node
        self.assertEqual(node.outputs["on_true"].value, "true_value")
        self.assertEqual(node.outputs["on_false"].value, fn.NoValue)

        # Test when condition is False
        node.inputs["condition"].value = False
        node.inputs["input"].value = "false_value"
        await node
        self.assertEqual(node.outputs["on_false"].value, "false_value")
        self.assertEqual(node.outputs["on_true"].value, "true_value")

    async def test_wait_node(self):
        node = logic.WaitNode()

        # Test with a delay of 0.5 seconds
        node.inputs["delay"].value = 2
        node.inputs["input"].value = "waited_value"
        t = time.time()
        await node
        t_end = time.time() - t
        self.assertLessEqual(2, t_end)
        self.assertLess(t_end, 4.5)
        self.assertEqual(node.outputs["output"].value, "waited_value")

    async def test_for_node(self):
        node = logic.ForNode()
        node.inputs["input"].value = "hello"
        node.outputs["do"].connect(node.inputs["collector"])
        await node

        self.assertEqual(node.outputs["done"].value, ["h", "e", "l", "l", "o"])

    async def test_collector_node(self):
        node = logic.CollectorNode()

        # Test collecting values
        node.inputs["input"].value = "value1"
        await node
        self.assertEqual(node.outputs["output"].value, ["value1"])

        node.inputs["input"].value = "value2"
        await node
        self.assertEqual(node.outputs["output"].value, ["value1", "value2"])

        # Test resetting collection
        node.inputs["reset"].value = True
        node.inputs["input"].value = "value3"
        node.request_trigger()
        await node
        self.assertEqual(node.outputs["output"].value, ["value3"])

        # Test collecting again after reset
        node.inputs["input"].value = "value4"
        await node
        self.assertEqual(node.outputs["output"].value, ["value3", "value4"])

    async def test_while_node(self):
        valuenode = math_nodes.value_node()
        valuenode.inputs["value"].value = 10
        await valuenode

        larger_than_5 = math_nodes.greater_node()
        larger_than_5.inputs["a"].connect(valuenode.outputs["out"])
        larger_than_5.inputs["b"].value = 5
        await larger_than_5
        self.assertEqual(larger_than_5.outputs["out"].value, True)

        while_node = logic.WhileNode()
        while_node.inputs["condition"].connect(larger_than_5.outputs["out"])
        while_node.inputs["input"].connect(valuenode.outputs["out"])

        subtract_node = math_nodes.sub_node()
        subtract_node.inputs["a"].connect(while_node.outputs["do"])
        subtract_node.inputs["b"].value = 1
        subtract_node.outputs["out"].connect(valuenode.inputs["value"])

        await while_node

        self.assertLessEqual(subtract_node.outputs["out"].value, 5)
        self.assertGreaterEqual(subtract_node.outputs["out"].value, 4)
