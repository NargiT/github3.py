"""Unit tests for Repository Commits."""
import github3
import pytest

from github3.exceptions import GitHubException

from . import helper

get_commit_example_data = helper.create_example_data_helper("commit_example")
example_commit_data = get_commit_example_data()

url_for = helper.create_url_helper(example_commit_data["url"])


class TestRepoCommitIterator(helper.UnitIteratorHelper):

    """Unit tests for RepoCommit iterator methods."""

    described_class = github3.repos.commit.RepoCommit
    example_data = example_commit_data

    def test_statuses(self):
        """Verify the request to iterate over statuses of a commit."""
        i = self.instance.statuses()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for("statuses"), params={"per_page": 100}, headers={}
        )

    def test_comments(self):
        """Verify the request to iterate over comments of a commit."""
        i = self.instance.comments()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for("comments"), params={"per_page": 100}, headers={}
        )


class TestRepoCommitIteratorAppInstAuth(helper.UnitIteratorAppInstHelper):

    """Unit tests for RepoCommit iterator methods."""

    described_class = github3.repos.commit.RepoCommit
    example_data = example_commit_data

    def test_check_runs(self):
        """Verify the request to iterate over check runs of a commit."""
        i = self.instance.check_runs()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for("check-runs"),
            params={"per_page": 100},
            headers=github3.checks.CheckRun.CUSTOM_HEADERS,
        )

    def test_check_suits(self):
        """Verify the request to iterate over check suits of a commit."""
        i = self.instance.check_suites()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for("check-suites"),
            params={"per_page": 100},
            headers=github3.checks.CheckSuite.CUSTOM_HEADERS,
        )


class TestRepoCommitRequiresAuth(helper.UnitRequiresAuthenticationHelper):

    """Unit test for auth required Repository Commit methods."""

    described_class = github3.repos.commit.RepoCommit
    example_data = example_commit_data

    def test_check_runs(self):
        with pytest.raises(GitHubException):
            self.instance.check_runs()

    def test_check_suites(self):
        with pytest.raises(GitHubException):
            self.instance.check_suites()
