import unittest
from unittest.mock import patch, MagicMock
from github import GithubException
from github_repo_extractor import GitHubRepoExtractor

class TestGitHubRepoExtractor(unittest.TestCase):

    @patch('github_repo_extractor.github_repo_extractor.Github')
    @patch('github_repo_extractor.github_repo_extractor.git')
    def setUp(self, mock_git, mock_github):
        self.mock_git = mock_git
        self.mock_github = mock_github
        self.mock_repo = MagicMock()
        self.mock_github.return_value.get_repo.return_value = self.mock_repo
        self.extractor = GitHubRepoExtractor('https://github.com/user/repo.git', 'fake_token')

    def test_initialization(self):
        self.assertEqual(self.extractor.repo_input, 'https://github.com/user/repo.git')
        self.assertEqual(self.extractor.access_token, 'fake_token')
        self.assertIsNone(self.extractor.local_path)

    def test_get_repo_from_input(self):
        # Test with full URL
        repo = self.extractor.get_repo_from_input('https://github.com/user/repo.git')
        self.mock_github.return_value.get_repo.assert_called_with('user/repo')
        self.assertEqual(repo, self.mock_repo)

        # Test with owner/repo format
        repo = self.extractor.get_repo_from_input('user/repo')
        self.mock_github.return_value.get_repo.assert_called_with('user/repo')
        self.assertEqual(repo, self.mock_repo)

        # Test with invalid input
        with self.assertRaises(ValueError):
            self.extractor.get_repo_from_input('invalid_input')

    def test_clone_repo(self):
        self.extractor.repo = self.mock_repo
        self.mock_repo.clone_url = 'https://github.com/user/repo.git'
        self.extractor.clone_repo()
        self.mock_git.Repo.clone_from.assert_called_once()

    def test_set_ignore_list(self):
        self.extractor.set_ignore_list(files=['.gitignore'], folders=['tests'], extensions=['.log'])
        self.assertIn('.gitignore', self.extractor.ignore_files)
        self.assertIn('tests', self.extractor.ignore_folders)
        self.assertIn('.log', self.extractor.ignore_extensions)

    def test_should_process(self):
        self.extractor.set_ignore_list(files=['.gitignore'], folders=['tests'], extensions=['.log'])
        self.assertTrue(self.extractor.should_process('src/main.py'))
        self.assertFalse(self.extractor.should_process('.gitignore'))
        self.assertFalse(self.extractor.should_process('tests/test_main.py'))
        self.assertFalse(self.extractor.should_process('logs/error.log'))

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="test content")
    @patch('os.walk')
    def test_process_content(self, mock_walk, mock_open):
        mock_walk.return_value = [
            ('/fake/path', [], ['file1.py', 'file2.txt'])
        ]
        mock_output_file = MagicMock()
        mock_progress_bar = MagicMock()

        self.extractor.repo_path = '/fake/path'
        self.extractor.process_content('', mock_output_file, mock_progress_bar)

        self.assertEqual(mock_output_file.write.call_count, 4)  # 2 files * (1 header + 1 content)
        self.assertEqual(mock_progress_bar.update.call_count, 2)  # 2 files processed

    def test_extract_to_file(self):
        with patch('github_repo_extractor.github_repo_extractor.tqdm') as mock_tqdm, \
             patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            self.extractor.clone_repo = MagicMock()
            self.extractor.count_files = MagicMock()
            self.extractor.process_content = MagicMock()

            self.extractor.extract_to_file('output.txt')

            self.extractor.clone_repo.assert_called_once()
            self.extractor.count_files.assert_called_once()
            self.extractor.process_content.assert_called_once()
            mock_file.assert_called_once_with('output.txt', 'w', encoding='utf-8')

if __name__ == '__main__':
    unittest.main()
