import os
import time
import shutil
import datetime
import psutil
import subprocess
import socket
import platform

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
                if not f.startswith('.'):
                    text += '{}{}\n'.format(subindent, f)
        return text

    def df(self):
        total, used, free = shutil.disk_usage('/')

        print("Filesystem      1K-blocks    Used      Available")
        print(f"/               {total // 1024}      {used // 1024}      {free // 1024}")

    def find(self, startpath, name=None, type=None):
        result = []
        for root, dirs, files in os.walk(startpath):
            if name:
                if type == 'd':
                    for dirname in dirs:
                        if name == dirname:
                            result.append(os.path.join(root, dirname))
                elif type == 'f':
                    for filename in files:
                        if name == filename:
                            result.append(os.path.join(root, filename))
                else:
                    for dirname in dirs:
                        if name == dirname:
                            result.append(os.path.join(root, dirname))
                    for filename in files:
                        if name == filename:
                            result.append(os.path.join(root, filename))
            else:
                result.extend(os.path.join(root, dirname) for dirname in dirs)
                result.extend(os.path.join(root, filename) for filename in files)
        return result

    def echo(self, *args, **kwargs):
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        text = sep.join(args)
        print(text, end=end)

    def date(self):
        now = datetime.datetime.now()
        return now.strftime("%a %b %d %H:%M:%S %Y")

    def whoami(self):
        return os.getlogin()

    def uname(self):
        return platform.uname()

    def hostname(self):
        return socket.gethostname()

    def ping(self, host):
        cmd = ["ping", "-c", "4", host]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout

    def ps(self):
        cmd = ["ps", "aux"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split("\n")
        header = lines.pop(0).split()

        process_list = []
        for line in lines:
            process_info = line.split(maxsplit=10)
            process_dict = {
                "user": process_info[0],
                "pid": process_info[1],
                "cpu": process_info[2],
                "mem": process_info[3],
                "vsz": process_info[4],
                "rss": process_info[5],
                "tty": process_info[6],
                "stat": process_info[7],
                "start": process_info[8],
                "time": process_info[9],
                "command": process_info[10],
            }
            process_list.append(process_dict)
        return process_list

    def top(self):
        processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'username'])
        process_list = []

        for process in processes:
            process_list.append(process.info)

        return process_list

    def ifconfig(self):
        interfaces = psutil.net_if_addrs()
        interface_info = {}

        for interface, addresses in interfaces.items():
            interface_info[interface] = [{"address": addr.address, "netmask": addr.netmask} for addr in addresses]

        return interface_info

