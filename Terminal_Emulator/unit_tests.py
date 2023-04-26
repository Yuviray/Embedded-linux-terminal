import unittest
from unittest.mock import patch
from game import*
from functions import FileManagement
from functions import*
import shutil
from unittest.mock import patch
from io import StringIO
import socket
import platform
from datetime import datetime

class TestCommandLine(unittest.TestCase):
    file_manager = FileManagement()
    def test_cd_command_with_valid_path(self):
        with patch('os.chdir') as mock_chdir:
            file_manager.cd("test_dir")
            mock_chdir.assert_called_once_with('/Users/yuvaneshrajamani/PycharmProjects/Embedded-linux-terminal/Terminal_Emulator/test_dir') # replace with expected path
    
    def test_ls_command(self):
        with open("test.txt", "w") as f:
            f.write("test")
        self.assertIn("test.txt", file_manager.ls())
        os.remove("test.txt")
        
    def test_cat_command(self):
        file_name = "test.txt"
        with open(file_name, "w") as f:
            f.write("test")
        file_manager.cat(file_name)
        self.assertTrue(os.path.exists(file_name))
        os.remove(file_name)
        
    def test_mkdir_command(self):
        dir_name = "test_dir"
        file_manager.mkdir(dir_name)
        self.assertTrue(os.path.exists(dir_name))
        os.rmdir(dir_name)
        
    def test_rm(self):
        test_file = 'test_file.txt'
        with open(test_file, 'w') as f:
            f.write('test')
        file_manager.rm(test_file)
        self.assertFalse(os.path.exists(test_file))

    def test_rmdir(self):
        test_dir = 'test_dir'
        os.mkdir(test_dir)
        file_manager.rmdir(test_dir)
        self.assertFalse(os.path.exists(test_dir))

    def test_pwd(self):
        current_dir = os.getcwd()
        self.assertEqual(file_manager.pwd(), current_dir)

    def test_mv(self):
        test_file = 'test_file.txt'
        with open(test_file, 'w') as f:
            f.write('test')
        new_dir = 'new_dir'
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)
        os.mkdir(new_dir)
        new_location = os.path.join(new_dir, test_file)
        file_manager.mv(test_file, new_location)
        self.assertTrue(os.path.exists(new_location))
        self.assertFalse(os.path.exists(test_file))
        shutil.rmtree(new_dir)

    def test_cp(self):
        test_file = 'test_file.txt'
        with open(test_file, 'w') as f:
            f.write('test')
        new_dir = 'new_dir'
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)
        os.mkdir(new_dir)
        new_location = os.path.join(new_dir, test_file)
        file_manager.cp(test_file, new_location)
        self.assertTrue(os.path.exists(new_location))
        self.assertTrue(os.path.exists(test_file))
        shutil.rmtree(new_dir)
        
    def test_getPathText(self):
        self.assertIsInstance(file_manager.get_path_text(), str)
        
    def test_touch(self):
        file_name = 'test_file.txt'
        file_manager.touch(file_name)
        self.assertTrue(os.path.exists(file_name))
        os.remove(file_name)
        
    def test_chmod(self):
        file_name = 'test_file.txt'
        file_manager.touch(file_name)
        with open(file_name, 'w') as file:
            file.write('test data')
        file_manager.chmod(0o644, file_name)
        self.assertEqual(os.stat(file_name).st_mode & 0o777, 0o644)
        os.remove(file_name)

    def test_grep(self):
        file_name = 'test_file.txt'
        file_manager.touch(file_name)
        with open(file_name, 'w') as file:
            file.write('line1\nline2\nline3\nline4\nline5')
        matching_lines = file_manager.grep('line', file_name)
        self.assertEqual(matching_lines, ['line1\n', 'line2\n', 'line3\n', 'line4\n', 'line5'])
        os.remove(file_name)
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_df(self, mock_stdout):
        file_manager.df()
        self.assertIn('Filesystem', mock_stdout.getvalue())
        self.assertIn('1K-blocks', mock_stdout.getvalue())
        self.assertIn('Used', mock_stdout.getvalue())
        self.assertIn('Available', mock_stdout.getvalue())
        
    def test_tail(self):
        with open("test_tail.txt", "w") as f:
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5")
        result = self.file_manager.tail("test_tail.txt", 3)
        self.assertEqual(result, ["Line 3\n", "Line 4\n", "Line 5"])
        os.remove("test_tail.txt")

    def test_date(self):
        current_date = self.file_manager.date()
        now = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
        self.assertEqual(current_date, now)

    def test_uname(self):
        uname_result = self.file_manager.uname()
        self.assertEqual(uname_result, platform.uname())

    def test_hostname(self):
        hostname_result = self.file_manager.hostname()
        self.assertEqual(hostname_result, socket.gethostname())

    def test_whoami(self):
        whoami_result = self.file_manager.whoami()
        self.assertEqual(whoami_result, os.getlogin())

    @patch('sys.stdout', new_callable=StringIO)
    def test_echo(self, mock_stdout):
        self.file_manager.echo("hello", "world", sep="-", end="!")
        self.assertEqual(mock_stdout.getvalue(), "hello-world!")
    
    @patch('os.popen')
    def test_wget(self, mock_popen):
        self.file_manager.wget('https://example.com')
        mock_popen.assert_called_once_with('wget https://example.com')
    
    @patch('shutil.disk_usage')
    def test_df(self, mock_disk_usage):
        mock_disk_usage.return_value = (1024, 512, 256)
        with patch('builtins.print') as mock_print:
            self.file_manager.df()
            mock_print.assert_any_call("Filesystem      1K-blocks    Used      Available")
            mock_print.assert_any_call("/               1      0      0")

    def test_find(self):
        test_dir = "test_dir"
        os.makedirs(os.path.join(test_dir, "subdir"))
        with open(os.path.join(test_dir, "file1.txt"), "w") as f:
            f.write("test")
        with open(os.path.join(test_dir, "subdir", "file2.txt"), "w") as f:
            f.write("test")
        result = self.file_manager.find(test_dir, name="file1.txt")
        self.assertEqual(len(result), 1)
        self.assertIn(os.path.join(test_dir, "file1.txt"), result)
        result = self.file_manager.find(test_dir, name="file2.txt", type='f')
        self.assertEqual(len(result), 1)
        self.assertIn(os.path.join(test_dir, "subdir", "file2.txt"), result)
        shutil.rmtree(test_dir)
    
    def test_touch(self):
        test_file = "test_file.txt"
        self.file_manager.touch(test_file)
        self.assertTrue(os.path.exists(test_file))
        os.remove(test_file)

    def test_head(self):
        test_file = "test_file.txt"
        with open(test_file, 'w') as file:
            file.write("line1\nline2\nline3\nline4\nline5")
        
        result = self.file_manager.head(test_file, 3)
        self.assertEqual(result, ["line1\n", "line2\n", "line3\n"])
        os.remove(test_file)

    @patch('builtins.print')
    def test_echo(self, mock_print):
        self.file_manager.echo("hello", "world", sep=", ")
        mock_print.assert_called_once_with("hello, world", end='\n')

    @patch('subprocess.run')
    def test_ping(self, mock_subprocess_run):
        self.file_manager.ping("localhost")
        mock_subprocess_run.assert_called_once()

    @patch('subprocess.run')
    def test_ps(self, mock_subprocess_run):
        self.file_manager.ps()
        mock_subprocess_run.assert_called_once()

    @patch('psutil.process_iter')
    def test_top(self, mock_process_iter):
        self.file_manager.top()
        mock_process_iter.assert_called_once()

    @patch('psutil.net_if_addrs')
    def test_ifconfig(self, mock_net_if_addrs):
        self.file_manager.ifconfig()
        mock_net_if_addrs.assert_called_once()

    
if __name__ == '__main__':
    unittest.main()
