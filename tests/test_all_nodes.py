from all_nodes_test_base import TestAllNodesBase
from test_strings import TestStringMethods
from test_dict import TestDictMethods
from test_lists import TestListsMethods
from test_math import TestMathNodes
from test_logic import TestLogicNodes


class TestAllNodes(
    TestStringMethods,
    TestDictMethods,
    TestListsMethods,
    TestMathNodes,
    TestLogicNodes,
    TestAllNodesBase,
):
    # in this test class all nodes should be triggered at least once to mark them as testing
    pass
