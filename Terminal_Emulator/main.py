import os

def ls():
    files = os.listdir(os.getcwd())
    for file in files:
        print(file)

def cd(path):
    os.chdir(path)

def mkfile(file):

    file_name = open(file,'w')
    file_name.close()
def mkfolder(folder):
    os.mkdir(folder)

def main():
    while True:
        term_input = input(os.getcwd() + "$ ")

        # Split the input into command and arguments
        command = term_input.split()
        if command[0] == "ls":
            ls()
        if command[0] == "cd":
            if len(command) > 1:
                cd(command[1])
            else:
                print("Error: Please specify a path.")
        if command[0] == "cat":
            if len(command) > 1:
                mkfile(command[2])
            else:
                print("Error: Please specify a path.")

        if command[0] == "mkdir":
            if len(command) > 1:
                mkfolder(command[1])
            else:
                print("Error: Please specify a path.")

if __name__ == "__main__":
    main()
