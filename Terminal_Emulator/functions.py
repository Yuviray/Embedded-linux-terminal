import os
import time
import shutil

class FileManagement:
    def cd(self, path):
        current_path = self.get_path_text()
        os.chdir(current_path[:-2] + "/" + path)

    def ls(self):
        return os.listdir(os.getcwd())

    def cat(self, file_name):
        new_file = open(file_name, 'w')
        new_file.close()

    def mkdir(self, dir_name):
        os.mkdir(dir_name)

    def rm(self, file_name):
        os.remove(file_name)

    def rmdir(self, dir_name):
        os.rmdir(dir_name)

    def pwd(self):
        return os.getcwd()

    def mv(self, src, dst):
        shutil.move(src, dst)

    def cp(self, src, dst):
        dst_dir = os.path.dirname(dst)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        shutil.copy(src, dst)

    def touch(self, file_name):
        new_file = open(file_name, 'w')
        new_file.close()

    def chmod(self, permission, file_name):
        os.chmod(file_name, permission)

    def chown(self, owner, file_name):
        os.chown(file_name, owner, -1)

    def grep(self, pattern, file_name):
        with open(file_name, 'r') as file:
            matching_lines = [line for line in file if pattern in line]
        return matching_lines

    def head(self, file_name, n):
        with open(file_name, 'r') as file:
            lines = file.readlines()
            return lines[:n]

    def tail(self, file_name, n):
        with open(file_name, 'r') as file:
            lines = file.readlines()
            return lines[-n:]

    def wget(self, url):
        cmd = 'wget {}'.format(url)
        output = os.popen(cmd).read()
        return output

    def get_path_text(self):
        current_folder = os.getcwd()
        return current_folder + "> "

    def list_files(self, startpath):
        text = "Directory Tree\n\n"
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            text += '{}{}/\n'.format(indent, os.path.basename(root))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                text += '{}{}\n'.format(subindent, f)
        return text