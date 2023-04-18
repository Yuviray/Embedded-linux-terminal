import unittest
from unittest.mock import patch
from game import*
from functions import*
import shutil
from unittest.mock import patch
from io import StringIO


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
        
    def test_touch(self):
        file_name = 'test_file.txt'
        touch(file_name)
        self.assertTrue(os.path.exists(file_name))
        os.remove(file_name)
        
    def test_chmod(self):
        file_name = 'test_file.txt'
        touch(file_name)
        with open(file_name, 'w') as file:
            file.write('test data')
        chmod(0o644, file_name)
        self.assertEqual(os.stat(file_name).st_mode & 0o777, 0o644)
        os.remove(file_name)
        
    def test_chown(self):
        file_name = 'test_file.txt'
        touch(file_name)
        with open(file_name, 'w') as file:
            file.write('test data')
        chown(1000, file_name)
        self.assertEqual(os.stat(file_name).st_uid, 1000)
        os.remove(file_name)
        
    def test_grep(self):
        file_name = 'test_file.txt'
        touch(file_name)
        with open(file_name, 'w') as file:
            file.write('line1\nline2\nline3\nline4\nline5')
        matching_lines = grep('line', file_name)
        self.assertEqual(matching_lines, ['line1\n', 'line2\n', 'line3\n', 'line4\n', 'line5'])
        os.remove(file_name)
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_df(self, mock_stdout):
        df()
        self.assertIn('Filesystem', mock_stdout.getvalue())
        self.assertIn('1K-blocks', mock_stdout.getvalue())
        self.assertIn('Used', mock_stdout.getvalue())
        self.assertIn('Available', mock_stdout.getvalue())

    
if __name__ == '__main__':
    unittest.main()
