import pygame
import os
import time
from functions import FileManagement

import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIColourPickerDialog

pygame.init()
file_manager = FileManagement()
max_lines = 300
prev_lines = []   
line_spacing = 8
next_y = 0
font_size = 16
font = pygame.font.Font('fonts/UbuntuMono-Regular.ttf', font_size)
master_folder_change = True

def appendTerminalText(text_to_add):
    global line_spacing, prev_lines, next_y, font
    prev_lines.append(text_to_add)
    next_y += font.get_height() + line_spacing



class DirectoryManager:
    def __init__(self):
        self.directory_lines = []
        self.master_folder_change = False

    def update_directory_lines(self):
        self.directory_lines.clear()
        directory_text = file_manager.list_files(os.getcwd())
        lines = directory_text.split('\n')
        for line in lines:
            self.directory_lines.append(line)

class CommandHandler:
    def callCommand(self, user_input):
        self.file_manager = FileManagement()

        command = user_input.split()

        # if user does not enter anything
        if len(command) == 0:
            return

        # Check if the user enters a valid command, if not just reset
        if command[0] == "cd":
            if len(command) == 2:
                try:
                    self.file_manager.cd(command[1])
                except:
                    appendTerminalText("Error: Please enter a valid path.")
            else:
                appendTerminalText("Error: Please specify a path.")

        elif command[0] == "ls":
            files = self.file_manager.ls()
            i = len(prev_lines)
            for file in files:
                last_time = os.path.getmtime(file)
                last_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time))
                appendTerminalText(last_time_str + "\t\t\t\t" + str(file))
                i += 1

        elif command[0] == "cat":
            if len(command) == 2:
                try:
                    self.file_manager.cat(command[1])
                except:
                    appendTerminalText("Error: Please enter a valid file name.")

            else:
                appendTerminalText("Error: Please specify a file name.")

        elif command[0] == "mkdir":
            if len(command) == 2:
                try:
                    self.file_manager.mkdir(command[1])
                except:
                    appendTerminalText("Error: Please enter a valid directory name.")
            else:
                appendTerminalText("Error: Please specify a directory name.")

        elif command[0] == "rm":
            if len(command) == 2:
                try:
                    self.file_manager.rm(command[1])
                except:
                    appendTerminalText("Error: Please enter a valid file name.")

            else:
                appendTerminalText("Error: Please specify a file name.")

        elif command[0] == "rmdir":
            if len(command) == 2:
                try:
                    self.file_manager.rmdir(command[1])
                except:
                    appendTerminalText("Error: Please enter a valid directory name.")
            else:
                appendTerminalText("Error: Please specify a directory name.")

        elif command[0] == "pwd":
            if len(command) > 1:
                appendTerminalText("pwd: too many arguments")
            else:
                self.file_manager.pwd()

        elif command[0] == "mv":
            if len(command) > 1:
                if len(command) < 3:
                    try:
                        self.file_manager.mv(command[1], command[2])
                    except:
                        appendTerminalText("Error: Please enter a valid file name.")

            else:
                appendTerminalText("Error: Please specify a file source.")

        elif command[0] == "cp":
            if len(command) > 1:
                if len(command) < 3:
                    try:
                        self.file_manager.cp(command[1], command[2])
                    except:
                        appendTerminalText("Error: Please enter a valid file name.")

            else:
                appendTerminalText("Error: Please specify a file source.")

        elif command[0] == "touch":
            if len(command) > 1:
                try:
                    self.file_manager.touch(command[1])
                except:
                    appendTerminalText("Error: Please enter a valid file name.")

            else:
                appendTerminalText("Error: Please specify a file name.")

        elif command[0] == "chmod":
            if len(command) > 1:
                if len(command) < 3:
                    try:
                        self.file_manager.chmod(command[1], command[2])
                    except:
                        appendTerminalText("Error: Please enter a valid file name.")

            else:
                appendTerminalText("Error: Please specify a file ")

        elif command[0] == "chown":
            if len(command) > 1:
                if len(command) < 3:
                    try:
                        self.file_manager.chown(command[1], command[2])
                    except:
                        appendTerminalText("Error: Please enter a valid file name.")

            else:
                appendTerminalText("Error: Please specify a file ")

        elif command[0] == "grep":
            if len(command) > 1:
                if len(command) < 3:
                    try:
                        self.file_manager.grep(command[1], command[2])
                    except:
                        appendTerminalText("Error: Please enter a valid file name.")

            else:
                appendTerminalText("Error: Please specify a file ")

        elif command[0] == "head":
            if len(command) > 1:
                if len(command) > 2 :
                    try:
                        self.file_manager.head(command[1], command[2])
                    except:
                        appendTerminalText("Error: Please enter a valid file name.")
                else:
                    try:
                        self.file_manager.head(command[1])
                    except:
                        appendTerminalText("Error: Please enter a valid file name.")
            else:
                self.file_manager.head(command[1], 10)

        elif command[0] == "df":
            self.file_manager.df()

        elif command[0] == "wget ":
            if len(command) > 1:
                try:
                    self.file_manager.wget(command[1])
                except:
                    appendTerminalText("Error: Please enter a valid link")
            else:
                appendTerminalText("Error: Please specify a link.")

class Terminal:
    def __init__(self):

        # Define terminal window variables
        self.terminal_width = 900
        self.terminal_height = 600
        self.terminal_background_color = pygame.Color(0, 0, 0)
        self.terminal_text_color = pygame.Color(255, 255, 255)
        self.cursor_color = pygame.Color(255, 255, 255)
        self.terminal_active = True  # can set false if user should click before typing
        self.terminal_window = pygame.Surface((self.terminal_width, self.terminal_height))

class WorkingTree(Terminal):
    def __init__(self):
        super().__init__()
        # Define working tree window variables
        self.working_tree_width = 400
        self.working_tree_height = 500
        self.working_tree_background_color = pygame.Color(8,1,20)
        self.working_tree_text_color = self.terminal_text_color
        self.working_tree_active = False
        self.working_tree_box = pygame.Rect(self.terminal_width, 0, self.working_tree_width, self.working_tree_height)
        self.working_tree_window = pygame.Surface((self.working_tree_width, self.working_tree_height))

class OptionsMenu:
    def __init__(self, term, tree):
        self.options_width = tree.working_tree_width
        self.options_height = term.terminal_height - tree.working_tree_height
        self.options_background_color = pygame.Color(15, 15, 15)
        self.options_window = pygame.Surface((self.options_width, self.options_height))

        self.overlay_surface_width = tree.working_tree_width
        self.overlay_surface_height = tree.working_tree_height
        self.overlay_background_color = pygame.Color(100, 100, 100)
        self.overlay_surface = pygame.Surface((self.overlay_surface_width, self.overlay_surface_height))
        self.overlay_surface.fill(term.terminal_background_color)
        self.sub_font = pygame.font.Font('fonts/UbuntuMono-Regular.ttf', font_size)
        self.color_menu_open = False


class TerminalScrollbar:
    def __init__(self, term):
        self.terminal_max_rows = term.terminal_height // (font.get_height() + line_spacing)
        self.terminal_scroll_position = 0
        self.terminal_scrollbar_width = 20
        self.terminal_scrollbar_height = 35
        self.terminal_scrollbar_x = term.terminal_width - self.terminal_scrollbar_width
        self.terminal_scrollbar_y = 0
def main():
    command_handler = CommandHandler()
    directory_manager = DirectoryManager()
    term = Terminal()
    tree = WorkingTree()

    options = OptionsMenu(term, tree)
    term_scroll = TerminalScrollbar(term)

    # ___________________________________________________
    # |Main Terminal Window               | working-    |
    # |900w x 600h                        | tree        |
    # |                                   | 400w x 500h | 
    # |                                   |             |
    # |                                   |_____________|
    # |                                   | Options     |
    # |                                   | 400w x 100h |
    # |___________________________________|_____________|  

    global font_size, next_y, prev_lines, max_lines, line_spacing, master_folder_change


    # Define screen variable
    screen_width = term.terminal_width + tree.working_tree_width
    screen_height = term.terminal_height
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pseudo Terminal")

    # Define file path box
    current_path = file_manager.get_path_text()
    path_surface = font.render(current_path, True, term.terminal_text_color)

    # Define text input box
    input_box = pygame.Rect(0, 0, term.terminal_width, term.terminal_height)
    input_text = ""

    # Define cursor variables
    cursor_surface = font.render("|", True, term.cursor_color)
    cursor_visible = True
    cursor_blink_time = 500  # Time between cursor blinks in milliseconds
    cursor_blink_timer = 0



    # Define working tree scrollbar variable
    working_tree_max_rows = tree.working_tree_height // (font.get_height() + line_spacing)
    working_tree_scroll_position = 0
    working_tree_scrollbar_width = 20
    working_tree_scrollbar_height = 35
    working_tree_scrollbar_x = tree.working_tree_width - working_tree_scrollbar_width
    working_tree_scrollbar_y = 0

    # Define command history
    command_history = []
    path_history = []
    max_history_length = 50
    history_index = 0
    overlay = 0
    
    # Define settings button
    settings_button_rect = pygame.Rect(term.terminal_width + 25, tree.working_tree_height + 25, 50 ,50 )
    settings_image = pygame.image.load("img/settings.png")
    settings_image = pygame.transform.scale(settings_image, (40, 40))

    ui_manager = pygame_gui.UIManager((screen_width, screen_height))
    
    #custom background color
    background_color_picker_button= UIButton(relative_rect=pygame.Rect(-310, -550, 220, 30),
                                        text='Pick Background Color', manager=ui_manager,
                                        anchors={'left': 'right', 'right': 'right',
                                                'top': 'bottom', 'bottom': 'bottom'})

    #custom text color
    text_color_picker_button = UIButton(relative_rect=pygame.Rect(-310, -500, 220, 30),
                                    text='Pick Text Color', manager=ui_manager,
                                    anchors={'left': 'right', 'right': 'right',
                                            'top': 'bottom', 'bottom': 'bottom'})

    clock = pygame.time.Clock()

    while True:
        # Handle events
        time_delta = clock.tick(60) / 1000
        current_path = file_manager.get_path_text()
        
        # Process all events
        for event in pygame.event.get():

            # If user exits out
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # If user clicks down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input box
                if input_box.collidepoint(event.pos):
                    terminal_active = True
                else:
                    terminal_active = False
                
                if tree.working_tree_box.collidepoint(event.pos):
                    working_tree_active = True
                else:
                    working_tree_active = False

                # If the user clicked on settings button and the settings aren't up yet
                if settings_button_rect.collidepoint(event.pos) and overlay == 0:
                    overlay = 1

                # If the user clicked on settings button while settings are up
                elif settings_button_rect.collidepoint(event.pos) and overlay == 1:
                    overlay = 0

                elif event.button == 4 and len(prev_lines) > term_scroll.terminal_max_rows and terminal_active:
                    term_scroll.terminal_scroll_position = max(0, term_scroll.terminal_scroll_position - 1)
                
                elif event.button == 5 and len(prev_lines) > term_scroll.terminal_max_rows and terminal_active:
                    term_scroll.terminal_scroll_position = min(len(prev_lines) - term_scroll.terminal_max_rows, term_scroll.terminal_scroll_position + 1)

                
                elif event.button == 4 and len(directory_manager.directory_lines) > working_tree_max_rows and working_tree_active:
                    working_tree_scroll_position = max(0, working_tree_scroll_position - 1)
                
                elif event.button == 5 and len(directory_manager.directory_lines) > working_tree_max_rows and working_tree_active:
                    working_tree_scroll_position = min(len(directory_manager.directory_lines) - working_tree_max_rows, working_tree_scroll_position + 1)


            # If the user entered a key
            elif event.type == pygame.KEYDOWN:
                if len(prev_lines) > term_scroll.terminal_max_rows:
                    terminal_scroll_position = len(prev_lines) - term_scroll.terminal_max_rows
                # If the user has clicked onto the terminal window
                if term.terminal_active:
                    # If user hits 'enter' key
                    if event.key == pygame.K_RETURN:
                        # Update command history
                        appendTerminalText(current_path + input_text)

                        command_history.append(input_text)
                        path_history.append(current_path)

                        # Process the user's input
                        command_handler.callCommand(input_text)

                        if len(command_history) > max_history_length:
                            command_history.pop(0)
                            path_history.pop(0)
                        
                        history_index = len(command_history)

                        if len(prev_lines) > max_lines:
                            prev_lines.pop(0)

                        # Reset user input and go to next line
                        input_text = ""

                    # If user hits 'backspace' key
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]

                    # If user hits the up arrow
                    elif event.key == pygame.K_UP:
                        # Cycle to older commands
                        if history_index > 0:
                            history_index -= 1
                            input_text = command_history[history_index]
                            current_path = path_history[history_index]

                    # If user hits the down arrow
                    elif event.key == pygame.K_DOWN:
                        # Cycle to newer commands
                        if history_index < len(command_history) - 1:
                            history_index += 1
                            input_text = command_history[history_index]
                            current_path = path_history[history_index]

                    # Else: add key to end of user input
                    else:
                        input_text += event.unicode  


            # If user clicks the button to edit background color
            elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == background_color_picker_button:
                color_menu_open = True
                background_color_picker = UIColourPickerDialog(pygame.Rect(905, 50, 390, 390),
                                                ui_manager,
                                                window_title="Change Background Color",
                                                initial_colour=term.terminal_background_color)
                
                if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                    terminal_background_color = event.colour

            # If user clicks the button to edit text color
            elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == text_color_picker_button:
                color_menu_open = True
                text_color_picker = UIColourPickerDialog(pygame.Rect(905, 50, 390, 390),
                                                ui_manager,
                                                window_title="Change Text Color",
                                                initial_colour=term.terminal_text_color)
                
                if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                    terminal_text_color = event.colour

            # If user exits out of color menu
            elif event.type == pygame_gui.UI_WINDOW_CLOSE:
                color_menu_open = False
                background_color_picker_button.enable()
                background_color_picker = None
                text_color_picker_button.enable()
                text_color_picker = None

            ui_manager.process_events(event)

        # Draw Options Window  
        options.options_window.fill(options.options_background_color)
        screen.blit(options.options_window, (term.terminal_width, tree.working_tree_height))
        pygame.draw.rect(screen,options.options_background_color, settings_button_rect)
        screen.blit(settings_image, (settings_button_rect.centerx - 20, settings_button_rect.centery - 20))
            
        # If settings is enable
        if overlay == 1:
            # Draw menu overlay
            options.overlay_surface.fill(options.overlay_background_color)
            screen.blit(options.overlay_surface, (term.terminal_width, 0))

            if options.color_menu_open:
                background_color_picker_button.disable()
                text_color_picker_button.disable()

            else:
                background_color_picker_button.enable()
                text_color_picker_button.enable()

            ui_manager.update(time_delta)
            ui_manager.draw_ui(screen)
        
        else:
            # Get current directory information
            background_color_picker_button.disable()
            text_color_picker_button.disable()
            tree.working_tree_window.fill(tree.working_tree_background_color)

            # Draw working tree scroll bar if nec. 
            if (len(directory_manager.directory_lines) > working_tree_max_rows):
                working_tree_scrollbar_y = int(tree.working_tree_height*((working_tree_scroll_position) / (len(directory_manager.directory_lines) - working_tree_max_rows)))
                if (working_tree_scroll_position == (len(directory_manager.directory_lines) - working_tree_max_rows)):
                    working_tree_scrollbar_y = tree.working_tree_height - working_tree_scrollbar_height
                pygame.draw.rect(tree.working_tree_window, (20, 120, 220), (working_tree_scrollbar_x, working_tree_scrollbar_y, working_tree_scrollbar_width, working_tree_scrollbar_height))
            #updates directory tree
            directory_manager.update_directory_lines()

            for i in range(working_tree_scroll_position, min(len(directory_manager.directory_lines), working_tree_scroll_position + working_tree_max_rows)):
                tree_text = options.sub_font.render(directory_manager.directory_lines[i], True, tree.working_tree_text_color)
                y = (i - working_tree_scroll_position) * (options.sub_font.get_height() + line_spacing)
                tree.working_tree_window.blit(tree_text, (10, y))

            # Draw current directory
            screen.blit(tree.working_tree_window, (term.terminal_width, 0))
            ui_manager.update(time_delta)

        # Get Terminal Ready to be drawn

        # Fill in the terminal background
        term.terminal_window.fill(term.terminal_background_color)

        # Update the path text
        current_path = file_manager.get_path_text()
        #terminal_window.blit(path_surface, (10, 10))

        # Draw Terminal Scroll bar
        if (len(prev_lines) > term_scroll.terminal_max_rows):
            terminal_scrollbar_y = int(term.terminal_height*((term_scroll.terminal_scroll_position) / (len(prev_lines) - term_scroll.terminal_max_rows)))
            if (term_scroll.terminal_scroll_position == (len(prev_lines) - term_scroll.terminal_max_rows)):
                term_scroll.terminal_scrollbar_y = term.terminal_height - term_scroll.terminal_scrollbar_height
            pygame.draw.rect(term.terminal_window, (20, 120, 220), (term_scroll.terminal_scrollbar_x, term_scroll.terminal_scrollbar_y, term_scroll.terminal_scrollbar_width, term_scroll.terminal_scrollbar_height))

        # Draw the current text
        text_surface = font.render(current_path + input_text, True, term.terminal_text_color)
        
        if len(prev_lines) == 0:
            term.terminal_window.blit(text_surface, (10, 0))

        ########## TODO: FIX BUG WITH SCROLL HERE!!!
        elif len(prev_lines) > term_scroll.terminal_max_rows:
            term.terminal_window.blit(text_surface, (10, term.terminal_height - font.get_height() - line_spacing))

            # Draw the previous commands
            for i in reversed(range(term_scroll.terminal_scroll_position + 1, len(prev_lines))):
                previous_surface = font.render(prev_lines[i], True, term.terminal_text_color)
                next_y = (i - term_scroll.terminal_scroll_position - 1) * (font.get_height() + line_spacing)
                term.terminal_window.blit(previous_surface, (10, next_y))

        else:
            # Draw the previous commands
            for i in range(term_scroll.terminal_scroll_position, min(len(prev_lines), term_scroll.terminal_scroll_position + term_scroll.terminal_max_rows)):
                previous_surface = font.render(prev_lines[i], True, term.terminal_text_color)
                next_y = (i - term_scroll.terminal_scroll_position) * (font.get_height() + line_spacing)
                term.terminal_window.blit(previous_surface, (10, next_y))
            
            term.terminal_window.blit(text_surface, (10, next_y + font.get_height() + line_spacing))


        # If the user has clicked onto the terminal
        if term.terminal_active:
            # Adjust cursor visibility
            if pygame.time.get_ticks() - cursor_blink_timer > cursor_blink_time:
                cursor_blink_timer = pygame.time.get_ticks()
                cursor_visible = not cursor_visible

            # Draw Cursor
            if cursor_visible:
                cursor_pos = text_surface.get_width() + line_spacing
                
                if len(prev_lines) == 0:
                    term.terminal_window.blit(cursor_surface, (cursor_pos, next_y))

                elif len(prev_lines) > term_scroll.terminal_max_rows - 1:
                    term.terminal_window.blit(cursor_surface, (cursor_pos, term.terminal_height - font.get_height() - line_spacing))
                else:
                    term.terminal_window.blit(cursor_surface, (cursor_pos, next_y + font.get_height() + line_spacing))

        #Draw Terminal Window
        screen.blit(term.terminal_window, (0,0))
        
        # Update the display
        pygame.display.update()

main()