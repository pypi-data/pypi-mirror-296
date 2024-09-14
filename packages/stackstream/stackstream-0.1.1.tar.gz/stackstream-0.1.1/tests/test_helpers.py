import unittest
from unittest.mock import patch, MagicMock
import subprocess
import sys
from io import StringIO
from stackstream.helpers import (
    build_branch_structure,
    create_empty_commit,
    create_new_branch,
    does_remote_branch_exist,
    get_commit_message,
    get_creation_commit,
    run_command,
    run_git_command
)

class TestHelpers(unittest.TestCase):

    @patch('subprocess.Popen')
    def test_run_command(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = (b'output', b'error')
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        output, error, code = run_command('test command')

        self.assertEqual(output, 'output')
        self.assertEqual(error, 'error')
        self.assertEqual(code, 0)
        mock_popen.assert_called_with('test command', stdout=-1, stderr=-1, shell=True)

    @patch('subprocess.run')
    def test_run_git_command(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        run_git_command(['status'])
        mock_run.assert_called_once_with(['git', 'status'], check=True, text=True)

        mock_error = subprocess.CalledProcessError(1, ['git', 'status'])
        mock_error.stderr = "Error message"
        mock_run.side_effect = mock_error

        stderr_capture = StringIO()
        sys.stderr = stderr_capture

        with self.assertRaises(SystemExit) as cm:
            run_git_command(['status'])

        sys.stderr = sys.__stderr__

        self.assertEqual(cm.exception.code, 1)
        self.assertEqual(stderr_capture.getvalue(), "Error message")
        mock_run.assert_called_with(['git', 'status'], check=True, text=True)

    @patch('stackstream.helpers.run_command')
    def test_does_remote_branch_exist(self, mock_run_command):
        mock_run_command.return_value = ('', '', 0)
        self.assertTrue(does_remote_branch_exist('main'))
        mock_run_command.assert_called_with('git ls-remote --exit-code --heads origin main')

    @patch('stackstream.helpers.run_command')
    def test_create_empty_commit(self, mock_run_command):
        create_empty_commit('Test commit')
        mock_run_command.assert_called_with('git commit --allow-empty -m "Test commit"')

    @patch('stackstream.helpers.run_command')
    def test_create_new_branch(self, mock_run_command):
        create_new_branch('new-branch', 'main')
        mock_run_command.assert_called_with('git checkout -b "new-branch" "main"')

    @patch('stackstream.helpers.run_command')
    def test_get_commit_message(self, mock_run_command):
        mock_run_command.return_value = ('Commit message', '', 0)
        message = get_commit_message('abc123')
        self.assertEqual(message, 'Commit message')
        mock_run_command.assert_called_with('git log -1 --pretty=%B abc123')

    # Add more tests for other helper functions...

    @patch('stackstream.helpers.get_commit_with_message')
    def test_get_creation_commit(self, mock_get_commit_with_message):
        mock_get_commit_with_message.return_value = ('abc123', '', 0)
        commit = get_creation_commit('feature-branch')
        self.assertEqual(commit, 'abc123')
        mock_get_commit_with_message.assert_called_with('feature-branch', 'Created branch feature-branch from', 100)

    @patch('stackstream.helpers.get_trunk_name')
    @patch('stackstream.helpers.get_local_branches')
    @patch('stackstream.helpers.get_merged_branches')
    @patch('stackstream.helpers.get_creation_commit')
    @patch('stackstream.helpers.get_commit_message')
    def test_build_branch_structure(self, mock_get_commit_message, mock_get_creation_commit,
                                    mock_get_merged_branches, mock_get_local_branches, mock_get_trunk_name):
        # Set up mock return values
        mock_get_trunk_name.return_value = 'main'
        mock_get_local_branches.return_value = ['main', 'feature-1', 'feature-2', 'feature-3']
        mock_get_merged_branches.return_value = ('origin/feature-3\n', '', 0)
        mock_get_creation_commit.side_effect = [None, 'def456', None]
        mock_get_commit_message.side_effect = [
            'Created branch feature-2 from feature-1',
        ]

        # Call the function
        parent_dict, children_dict, trunk = build_branch_structure()

        # Assert the expected results
        expected_parent_dict = {'feature-2': 'feature-1'}
        expected_children_dict = {
            'feature-1': ['feature-2'],
            'feature-2': [],
            'feature-3': []
        }
        expected_trunk = 'main'

        self.assertEqual(parent_dict, expected_parent_dict)
        self.assertEqual(children_dict, expected_children_dict)
        self.assertEqual(trunk, expected_trunk)

        # Verify that the mocked functions were called as expected
        mock_get_trunk_name.assert_called_once()
        mock_get_local_branches.assert_called_once()
        mock_get_merged_branches.assert_called_once_with('main')
        self.assertEqual(mock_get_creation_commit.call_count, 2)
        self.assertEqual(mock_get_commit_message.call_count, 1)

if __name__ == '__main__':
    unittest.main()