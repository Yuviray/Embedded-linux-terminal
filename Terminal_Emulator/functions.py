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


def getPathText():
    current_folder = os.getcwd()
    return current_folder + "> "

def list_files(directory):
    text = ''
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isfile(full_path):
            text += '- {}\n'.format(item)
        elif os.path.isdir(full_path):
            text += '+ {}/\n'.format(item)
            subtext = list_files(full_path)
            sublines = subtext.strip().split('\n')
            sublines = ['    ' + line for line in sublines]
            text += '\n'.join(sublines) + '\n'
    return text

