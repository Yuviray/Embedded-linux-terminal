import unittest
from unittest.mock import patch
from testing import*
import shutil

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
        
    def test_rm(self):
        # Create a test file and remove it
        test_file = 'test_file.txt'
        with open(test_file, 'w') as f:
            f.write('test')
        rm(test_file)
        self.assertFalse(os.path.exists(test_file))

    def test_rmdir(self):
        # Create a test directory and remove it
        test_dir = 'test_dir'
        os.mkdir(test_dir)
        rmdir(test_dir)
        self.assertFalse(os.path.exists(test_dir))

    def test_pwd(self):
        # Test that pwd() returns the current working directory
        current_dir = os.getcwd()
        self.assertEqual(pwd(), current_dir)

    def test_mv(self):
        # Create a test file and move it to a new location
        test_file = 'test_file.txt'
        with open(test_file, 'w') as f:
            f.write('test')
        new_dir = 'new_dir'
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)
        os.mkdir(new_dir)
        new_location = os.path.join(new_dir, test_file)
        mv(test_file, new_location)
        self.assertTrue(os.path.exists(new_location))
        self.assertFalse(os.path.exists(test_file))
        shutil.rmtree(new_dir)

    def test_cp(self):
        # Create a test file and copy it to a new location
        test_file = 'test_file.txt'
        with open(test_file, 'w') as f:
            f.write('test')
        new_dir = 'new_dir'
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)
        os.mkdir(new_dir)
        new_location = os.path.join(new_dir, test_file)
        cp(test_file, new_location)
        self.assertTrue(os.path.exists(new_location))
        self.assertTrue(os.path.exists(test_file))
        shutil.rmtree(new_dir)
        
    def test_getPathText(self):
        self.assertIsInstance(getPathText(), str)
    
if __name__ == '__main__':
    unittest.main()
