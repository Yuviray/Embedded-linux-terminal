# **Embedded-linux-terminal**
**- Yuvanesh Rajamani, Collan Parker**
## Project Description:
For many beginners, Linux can pose an intimidating set of challenges. At first, many of the
specifics of the language are unintuitive. While all terminal emulators offer the resources to learn
and practice with the most important aspects of Linux (as this is a built-in feature of the
language), most terminals take a minimalist approach when it comes to the GUI. This approach
isn’t necessarily wrong but could result in limiting some users’ ability to succeed while using the
terminal. This application is designed to be a tool for new users to better learn the fundamentals of
Linux/Unix commands, and for experienced users to increase their productivity while working
within a Unix environment. This application is intended to be used as a tool to help beginners learn how to work with Linux.
In addition to this, the application will be able to fast track some processes and increase overall
efficiency for all users.
### Setup
1. Download github
2. Install libraries if need on your system
  - pygame
  - pygame.gui
4. Cd Terminal_Emulator
5. run game.py for main application
6. run unit_tests.py for unit tests

### Structural description
The main program is run from the game.py file. At program start a gui pops up that has the main terminal window on the left and center of the screen. To the right of the screen is the dragram tree window. In the code all of the windows are classes that inherent from one main window class. The main function in game.py is where most of the events are handled such as clicking and input. When a user enters a command in the terminal, they are accessing a class called CommandHandler where the user input is parsed and read. The CommandHandler will then call a function from the FileManagement class that stores all of our linux commands. The FileManagement class is in a separte file called functions.py. After calling the command the CommandHandler class will then display the output to the tereminal window. The directory window will display the current working directory and all its contents. Underneath the directory tree window is the Buttons that show the setting and help menu. These are also set up as classes that inherit from the main window class. When the settings button is clicked on overlay appears over the directory tree. This gives users the options to customize the background and text of the terminal window. Users then use the colorpicker to change the color. When the button is clicked again the overlay disappears. Next to the settings button is the help button. This works the same way as the background button in that an overlay appears and disappears at the click of the button. The help button distplays a dropdown list that displays all of the commands that available to the user and instructions on how to use them. The help button is implemented as text files that are stored in a folder in the project. When a user picks a command from the list, the matching text file is picked from the folder and displayed on the overlay. Almost all functionality in the program is implemented as classes for simplicity and for OOP, only the main function isnt a class since thats where the main gui is drawn and the events are handled.

