import unittest
from unittest.mock import patch, MagicMock
from github_repo_extractor import GitHubRepoExtractor

class TestGitHubRepoExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = GitHubRepoExtractor('https://github.com/user/repo.git', 'fake_token')

    def test_initialization(self):
        self.assertEqual(self.extractor.repo_input, 'https://github.com/user/repo.git')
        self.assertEqual(self.extractor.access_token, 'fake_token')
        self.assertIsNone(self.extractor.local_path)

    @patch('github_repo_extractor.Github')
    def test_get_repo_from_input(self, mock_github):
        mock_repo = MagicMock()
        mock_github.return_value.get_repo.return_value = mock_repo
        
        repo = self.extractor.get_repo_from_input('user/repo')
        
        self.assertEqual(repo, mock_repo)
        mock_github.return_value.get_repo.assert_called_once_with('user/repo')

    @patch('github_repo_extractor.git')
    def test_clone_repo(self, mock_git):
        self.extractor.repo = MagicMock()
        self.extractor.repo.clone_url = 'https://github.com/user/repo.git'
        
        self.extractor.clone_repo()
        
        mock_git.Repo.clone_from.assert_called_once()

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

if __name__ == '__main__':
    unittest.main()
