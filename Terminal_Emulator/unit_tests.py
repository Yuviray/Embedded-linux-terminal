import unittest
from unittest.mock import patch
from testing import*

class TestCommandLine(unittest.TestCase):
    def test_cd_command_with_valid_path(self):
        with patch('os.chdir') as mock_chdir:
            cd("test_dir")
            mock_chdir.assert_called_once_with('/Users/yuvaneshrajamani/PycharmProjects/Embedded-linux-terminal/Terminal_Emulator/test_dir') # replace with expected path
    
    def test_ls_command(self):
        with open("test.txt", "w") as f:
            f.write("test")
        self.assertIn("test.txt", ls())
        os.remove("test.txt")
        
    def test_cat_command(self):
        file_name = "test.txt"
        with open(file_name, "w") as f:
            f.write("test")
        cat(file_name)
        self.assertTrue(os.path.exists(file_name))
        os.remove(file_name)
        
    def test_mkdir_command(self):
        dir_name = "test_dir"
        mkdir(dir_name)
        self.assertTrue(os.path.exists(dir_name))
        os.rmdir(dir_name)
        
    def test_getPathText(self):
        self.assertIsInstance(getPathText(), str)
    
if __name__ == '__main__':
    unittest.main()
