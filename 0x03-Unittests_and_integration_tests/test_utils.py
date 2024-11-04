#!/usr/bin/env python3
"""
Unittest For the Utils module
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import Mock, patch


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for utils access_nested_map
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

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'")
        ])
    def test_access_nested_map_exception(self, np, path, expected):
        """
        Test access_nested_map for exception
        """
        path = list(path)
        with self.assertRaises(KeyError) as context:
            access_nested_map(np, path)

        self.assertEqual(str(context.exception), expected)


class TestGetJson(unittest.TestCase):
    """
    Test class for utils get_json
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
        ])
    @patch("requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test get_json() method with mocked data
        """
        mock = Mock()
        mock.json.return_value = test_payload
        mock_get.return_value = mock

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test class for memoize()
    """
    def test_memoize(self):
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test = TestClass()

        with patch.object(test, 'a_method', return_value=42) as mock_method:
            call_1 = test.a_property
            call_2 = test.a_property

            self.assertEqual(call_1, 42)
            self.assertEqual(call_2, 42)
            mock_method.assert_called_once()
