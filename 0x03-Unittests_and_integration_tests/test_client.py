#!/usr/bin/env python3
"""
Unittests for the GitHub orgs clients
"""

import unittest
from unittest.mock import Mock, patch
from client import GithubOrgClient
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """
    Test GitHubOrgClient
    """

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"})
        ])
    @patch('utils.get_json')
    def test_org(self, org, url, mock_get_json):
        """
        Test that GitHubOrgClient returns correct value
        """
        mock_get_json.return_value = url

        client = GithubOrgClient(org)
        result = client.org

        mock_get_json.assert_called_once_with(client.ORG_URL.format(org=org))
        self.assetEqual(result, expected_value)
