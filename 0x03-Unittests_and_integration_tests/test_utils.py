#!/usr/bin/env python3
"""
Unittest For the Utils module
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for utils
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    def test_access_nested_map(self, np, path, expected):
        """
        Test access_nested_map()
        """
        path = list(path)
        self.assertEqual(access_nested_map(np, path), expected)