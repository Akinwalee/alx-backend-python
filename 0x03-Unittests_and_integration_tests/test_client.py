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

    @patch.object(GithubOrgClient, "org")
    def test_public_repos_url(self, mock_org):
        """
        Test _public_repos_url
        """
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/googlle/repos"}

        client = GithubOrgClient("google")
        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/google/repos")

    @patch("utils.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test public_repos()
        """
        payload = [
                {"name": "repo1", "license": {"key": "nit"}},
                {"name": "repo2", "license": {"key": "apache-2.0"}},
                {"name": "repo3", "license": None}
                ]
        mock_get_json.return_value = payload
        client = GithubOrgClient("google")

        with patch.object(client, "_public_repos_url",
                        new="https://api.github.com/orgs/google/repos"):
            #client = GithubOrgClient("google")
            result = client.public_repos()

            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            mock_get_json.assert_called_once_with(
                    "https://api.github.com/orgs/google/repos")
            #client._public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False)
        ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test has_license
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
