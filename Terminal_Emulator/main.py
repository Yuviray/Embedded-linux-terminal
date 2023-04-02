import os

path = os.getcwd()

def ls():
    files = os.listdir(path)
    for file in files:
        print(file)

def cd():
    path = input("path : ")
    os.chdir(path)

def mkfile():
    file = input("File name : ")
    file_name = open(file,'w')
    file_name.close()
def mkfolder():
    folder = input("folder name : ")
    os.mkdir(folder)

def main():
    while True:
        command = input("[terminal]$ ")
        if command == "ls":
            ls()
        if command == "cd":
            cd()
        if command == "cat":
            mkfile()
        if command == "mkdir":
            mkfolder()

if __name__ == "__main__":
    main()