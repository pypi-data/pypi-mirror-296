import unittest
from unittest.mock import patch, MagicMock
from stackstream.api import create_branch, hoist_branch, create_pr, propagate_commits

class TestApi(unittest.TestCase):

    @patch('stackstream.api.get_current_branch')
    @patch('stackstream.api.create_new_branch')
    @patch('stackstream.api.create_empty_commit')
    def test_create_branch(self, mock_create_empty_commit, mock_create_new_branch, mock_get_current_branch):
        mock_get_current_branch.return_value = 'main'
        create_branch('new-feature')
        mock_create_new_branch.assert_called_once_with('new-feature', 'main')
        mock_create_empty_commit.assert_called_once_with('Created branch new-feature from main')

    @patch('stackstream.api.get_current_branch')
    @patch('stackstream.api.get_creation_commit')
    @patch('stackstream.api.rebase_onto')
    def test_hoist_branch(self, mock_rebase_onto, mock_get_creation_commit, mock_get_current_branch):
        mock_get_current_branch.return_value = 'feature-branch'
        mock_get_creation_commit.return_value = 'abc123'
        hoist_branch()
        mock_rebase_onto.assert_called_once_with('origin/main', 'abc123')

    @patch('stackstream.api.get_current_branch')
    @patch('stackstream.api.get_creation_commit')
    @patch('stackstream.api.get_commit_message')
    @patch('stackstream.api.update_remote_refs')
    @patch('stackstream.api.does_remote_branch_exist')
    @patch('stackstream.api.get_trunk_name')
    @patch('stackstream.api.get_pr_output')
    @patch('stackstream.api.run_command')
    def test_create_pr(self, mock_run_command, mock_get_pr_output, mock_get_trunk_name, 
                       mock_does_remote_branch_exist, mock_update_remote_refs, 
                       mock_get_commit_message, mock_get_creation_commit, mock_get_current_branch):
        mock_get_current_branch.return_value = 'feature-branch'
        mock_get_creation_commit.return_value = 'abc123'
        mock_get_commit_message.return_value = 'Created branch feature-branch from parent-branch'
        mock_does_remote_branch_exist.return_value = True
        mock_get_trunk_name.return_value = 'main'
        mock_get_pr_output.return_value = '{"url": "https://github.com/org/repo/pull/1"}'
        mock_run_command.return_value = ('PR URL', '', 0)

        create_pr()

        mock_run_command.assert_called_once()
        self.assertIn('--base "parent-branch"', mock_run_command.call_args[0][0])
        self.assertIn('--title "Pull request for feature-branch"', mock_run_command.call_args[0][0])

    @patch('stackstream.api.get_current_branch')
    @patch('stackstream.api.build_branch_structure')
    @patch('stackstream.api.rebase_and_update_refs')
    @patch('stackstream.api.does_remote_branch_exist')
    @patch('stackstream.api.push_with_lease')
    @patch('stackstream.api.push_and_set_upstream')
    def test_propagate_commits(self, mock_push_and_set_upstream, mock_push_with_lease, 
                               mock_does_remote_branch_exist, mock_rebase_and_update_refs, 
                               mock_build_branch_structure, mock_get_current_branch):
        mock_get_current_branch.return_value = 'feature-1'
        mock_build_branch_structure.return_value = (
            {'feature-2': 'feature-1', 'feature-3': 'feature-2'},
            {'feature-1': ['feature-2'], 'feature-2': ['feature-3'], 'feature-3': []},
            'main'
        )
        mock_rebase_and_update_refs.return_value = ('', '', 0)
        mock_does_remote_branch_exist.return_value = True
        mock_push_with_lease.return_value = ('', '', 0)

        propagate_commits(push=True)

        mock_rebase_and_update_refs.assert_called_with('feature-1', 'feature-3')
        mock_push_with_lease.assert_any_call('feature-1')
        mock_push_with_lease.assert_any_call('feature-2')
        mock_push_with_lease.assert_any_call('feature-3')

if __name__ == '__main__':
    unittest.main()