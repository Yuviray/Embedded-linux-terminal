import os
import time
import shutil

def cd(path):
    current_path = getPathText()
    os.chdir(current_path[:-2] + "/" + path)

def ls():
    return os.listdir(os.getcwd())

def cat(file_name):
    new_file = open(file_name,'w')
    new_file.close()

def mkdir(dir_name):
    os.mkdir(dir_name)

def rm(file_name):
    os.remove(file_name)

def rmdir(dir_name):
    os.rmdir(dir_name)

def pwd():
    return os.getcwd()

def mv(src, dst):
    shutil.move(src, dst)

def cp(src, dst):
    dst_dir = os.path.dirname(dst)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    shutil.copy(src, dst)
    
def touch(file_name):
    new_file = open(file_name, 'w')
    new_file.close()

def chmod(permission, file_name):
    os.chmod(file_name, permission)

def chown(owner, file_name):
    os.chown(file_name, owner, -1)

def grep(pattern, file_name):
    with open(file_name, 'r') as file:
        matching_lines = [line for line in file if pattern in line]
    return matching_lines
#def ln(src, dst):
#    os.symlink(src, dst)

#def du(file_name):
#    cmd = 'du -sh {}'.format(file_name)
#    output = os.popen(cmd).read()
#    return output

def df():
    cmd = 'df'
    output = os.popen(cmd).read()
    return output

#def find(path, option):
#    cmd = 'find {} {}'.format(path, option)
#    output = os.popen(cmd).read()
#    return output

def head(file_name,n):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return lines[:n]

def tail(file_name, n):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return lines[-n:]

def wget(url):
    cmd = 'wget {}'.format(url)
    output = os.popen(cmd).read()
    return output


def getPathText():
    current_folder = os.getcwd()
    return current_folder + "> "

def list_files(startpath):
    text = "Directory Tree\n\n"
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        text += '{}{}/\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            text += '{}{}\n'.format(subindent, f)
    return text

