import unittest
from funcnodes_basic import strings

from funcnodes_basic.strings import (
    string_length,
    string_concat,
    string_split,
    string_join,
    string_upper,
    string_lower,
    string_replace,
    string_strip,
    string_startswith,
    string_endswith,
    string_contains,
    string_format_map,
    string_capitalize,
    string_title,
    string_swapcase,
    string_zfill,
    string_center,
    string_ljust,
    string_rjust,
    string_count,
    string_find,
    string_rfind,
    string_index,
    string_rindex,
    string_isalnum,
    string_isalpha,
    string_isdigit,
    string_islower,
    string_isupper,
    string_isspace,
    string_istitle,
    string_isprintable,
    string_isidentifier,
    string_isdecimal,
    string_isnumeric,
    string_isascii,
    re_match,
    re_fullmatch,
    re_search,
    re_findall,
    re_sub,
    re_subn,
    re_escape,
    re_split,
    string_decode,
    string_encode,
    string_input,
    regex_shelf,
    NODE_SHELF,
)


class TestStringMethods(unittest.IsolatedAsyncioTestCase):
    async def test_methods(self):
        tested_nodes = []

        teststring = "Hello, World!"
        for nodeclass, expected_output, output in [
            (string_length, len(teststring), "length"),
            (string_split, teststring.split(" "), "split"),
            (string_upper, teststring.upper(), "upper"),
            (string_lower, teststring.lower(), "lower"),
            (string_strip, teststring.strip(), "stripped"),
            (string_capitalize, teststring.capitalize(), "capitalized"),
            (string_title, teststring.title(), "titled"),
            (string_swapcase, teststring.swapcase(), "swapped"),
            (string_isalnum, teststring.isalnum(), "is_alphanumeric"),
            (string_isalpha, teststring.isalpha(), "is_alphabetical"),
            (string_isdigit, teststring.isdigit(), "is_digit"),
            (string_islower, teststring.islower(), "is_lowercase"),
            (string_isupper, teststring.isupper(), "is_uppercase"),
            (string_isspace, teststring.isspace(), "is_space"),
            (string_istitle, teststring.istitle(), "is_title"),
            (string_isprintable, teststring.isprintable(), "is_printable"),
            (string_isidentifier, teststring.isidentifier(), "is_identifier"),
            (string_isdecimal, teststring.isdecimal(), "is_decimal"),
            (string_isnumeric, teststring.isnumeric(), "is_numeric"),
            (string_isascii, teststring.isascii(), "is_ascii"),
        ]:
            node = nodeclass()
            node.inputs["s"].value = teststring
            await node
            self.assertEqual(node.outputs[output].value, expected_output)
            tested_nodes.append(node.__class__)

        node = string_concat()
        node.inputs["s1"].value = "Hello"
        node.inputs["s2"].value = "World"
        await node
        self.assertEqual(node.outputs["concatenated"].value, "HelloWorld")
        tested_nodes.append(node.__class__)

        node = string_replace()
        node.inputs["s"].value = "Hello, World!"
        node.inputs["old"].value = "o"
        node.inputs["new"].value = "0"
        await node
        self.assertEqual(node.outputs["replaced"].value, "Hell0, W0rld!")
        tested_nodes.append(node.__class__)

        node = string_join()
        node.inputs["strings"].value = ["Hello", "World"]
        await node
        self.assertEqual(node.outputs["joined"].value, "Hello World")
        tested_nodes.append(node.__class__)

        node = string_startswith()
        node.inputs["s"].value = "Hello, World!"
        node.inputs["prefix"].value = "Hello"
        await node
        self.assertEqual(node.outputs["starts_with"].value, True)
        tested_nodes.append(node.__class__)

        node = string_endswith()
        node.inputs["s"].value = "Hello, World!"
        node.inputs["suffix"].value = "World!"
        await node
        self.assertEqual(node.outputs["ends_with"].value, True)
        tested_nodes.append(node.__class__)

        node = string_contains()
        node.inputs["s"].value = "Hello, World!"
        node.inputs["sub"].value = "World"
        await node
        self.assertEqual(node.outputs["contains"].value, True)
        tested_nodes.append(node.__class__)

        node = string_format_map()
        node.inputs["s"].value = "Hello, {name}!"
        node.inputs["mapping"].value = {"name": "World"}
        await node
        self.assertEqual(node.outputs["formatted"].value, "Hello, World!")
        tested_nodes.append(node.__class__)

        for nodeclass, expected_output, output in [
            (string_zfill, teststring.zfill(20), "zfilled"),
            (string_center, teststring.center(20), "centered"),
            (string_ljust, teststring.ljust(20), "left_justified"),
            (string_rjust, teststring.rjust(20), "right_justified"),
        ]:
            node = nodeclass()
            node.inputs["s"].value = teststring
            node.inputs["width"].value = 20
            await node
            self.assertEqual(node.outputs[output].value, expected_output)
            tested_nodes.append(node.__class__)

        for nodeclass, expected_output, output in [
            (string_count, teststring.count("o"), "count"),
            (string_find, teststring.find("o"), "index"),
            (string_rfind, teststring.rfind("o"), "index"),
            (string_index, teststring.index("o"), "index"),
            (string_rindex, teststring.rindex("o"), "index"),
        ]:
            node = nodeclass()
            node.inputs["s"].value = teststring
            node.inputs["sub"].value = "o"
            await node
            self.assertEqual(node.outputs[output].value, expected_output)
            tested_nodes.append(node.__class__)

        node = string_decode()
        node.inputs["b"].value = b"Hello, World!"
        await node
        self.assertEqual(node.outputs["decoded"].value, "Hello, World!")
        tested_nodes.append(node.__class__)

        node = string_encode()
        node.inputs["s"].value = "Hello, World!"
        await node
        self.assertEqual(node.outputs["encoded"].value, b"Hello, World!")
        tested_nodes.append(node.__class__)

        node = string_input()
        node.inputs["s"].value = "Hello, World!"
        await node
        self.assertEqual(node.outputs["string"].value, "Hello, World!")
        tested_nodes.append(node.__class__)

        for nodeclass in NODE_SHELF["nodes"]:
            if nodeclass not in tested_nodes:
                raise AssertionError(f"Node {nodeclass} was not tested")

    async def test_regex(self):
        tested_nodes = []

        teststring = "Hello, World!"

        node = re_findall()
        node.inputs["pattern"].value = "Hello|World"
        node.inputs["string"].value = teststring
        await node
        self.assertEqual(node.outputs["matches"].value, ["Hello", "World"])
        tested_nodes.append(node.__class__)

        node = re_match()
        node.inputs["pattern"].value = "Hello|World"
        node.inputs["string"].value = teststring
        await node
        self.assertEqual(node.outputs["match"].value, True)
        self.assertEqual(node.outputs["groups"].value, ["Hello"])
        tested_nodes.append(node.__class__)

        node = re_fullmatch()
        node.inputs["pattern"].value = "Hello, World!"
        node.inputs["string"].value = teststring
        await node
        self.assertEqual(node.outputs["match"].value, True)
        tested_nodes.append(node.__class__)

        node = re_search()
        node.inputs["pattern"].value = "Hello|World"
        node.inputs["string"].value = teststring
        await node
        self.assertEqual(node.outputs["match"].value, True)
        self.assertEqual(node.outputs["groups"].value, ["Hello"])
        tested_nodes.append(node.__class__)

        node = re_sub()
        node.inputs["pattern"].value = "o"
        node.inputs["repl"].value = "0"
        node.inputs["string"].value = teststring
        await node
        self.assertEqual(node.outputs["substituted"].value, "Hell0, W0rld!")
        tested_nodes.append(node.__class__)

        node = re_subn()
        node.inputs["pattern"].value = "o"
        node.inputs["repl"].value = "0"
        node.inputs["string"].value = teststring
        await node
        self.assertEqual(node.outputs["substituted"].value, "Hell0, W0rld!")
        self.assertEqual(node.outputs["count"].value, 2)
        tested_nodes.append(node.__class__)

        node = re_escape()
        node.inputs["pattern"].value = "Hello\tWorld!"
        await node
        self.assertEqual(node.outputs["escaped"].value, "Hello\\\tWorld!")
        tested_nodes.append(node.__class__)

        node = re_split()
        node.inputs["pattern"].value = ", "
        node.inputs["string"].value = teststring
        await node
        self.assertEqual(node.outputs["splitted"].value, ["Hello", "World!"])
        tested_nodes.append(node.__class__)

        for nodeclass in regex_shelf["nodes"]:
            if nodeclass not in tested_nodes:
                raise AssertionError(f"Node {nodeclass} was not tested")
