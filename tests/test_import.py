import unittest
import funcnodes as fn


class TestImport(unittest.TestCase):
    def test_find(self):
        res = fn.lib.libfinder.find_shelf_from_module("funcnodes_basic")

        self.assertEqual(res[0]["name"], "basics")
        self.assertGreater(len(res[0]["subshelves"]), 0, res[0])
