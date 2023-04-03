import os
import tkinter as tk

def list_files(startpath):
    text = "Directory Tree\n"
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        #print('{}{}/'.format(indent, os.path.basename(root)))
        text += '{}{}/\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            #print('{}{}'.format(subindent, f))
            text += '{}{}\n'.format(subindent, f)
    return text

def ls():
    files = os.listdir(os.getcwd())
    for file in files:
        print(file)


    #list_files(os.getcwd())

def cd(path):
    os.chdir(path)

def mkfile(file):
    file_name = open(file,'w')
    file_name.close()

def mkfolder(folder):
    os.mkdir(folder)


def tree():
    root = tk.Tk()
    text_widget = tk.Text(root)
    text_widget.pack()
    text_widget.insert(tk.END, list_files(os.getcwd()))
    root.mainloop()
    root.quit()


def main():
    while True:

        term_input = input(os.getcwd() + "$ ")

        # Split the input into command and arguments
        command = term_input.split()
        if command[0] == "ls":
            tree()
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
        else:
            os.system(term_input)




if __name__ == "__main__":
    main()
