import pygame
import os
import time
from functions import FileManagement

import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIColourPickerDialog

pygame.init()
file_manager = FileManagement()

class DirectoryManager:
    def __init__(self):
        self.directory_lines = []
        self.master_folder_change = True

    def update_directory_lines(self):
        self.directory_lines.clear()
        directory_text = file_manager.list_files(os.getcwd())
        lines = directory_text.split('\n')
        for line in lines:
            self.directory_lines.append(line)
    
    def negateMasterFolderChange(self):
        self.master_folder_change = not self.master_folder_change

class CommandHandler:
    def callCommand(self, terminal):
        self.file_manager = FileManagement()

        command = terminal.text.split()

        # if user does not enter anything
        if len(command) == 0:
            return

        # Check if the user enters a valid command, if not just reset
        if command[0] == "cd":
            if len(command) == 2:
                try:
                    self.file_manager.cd(command[1])
                except:
                    terminal.appendTerminalText("Error: Please enter a valid path.")
            else:
                terminal.appendTerminalText("Error: Please specify a path.")

        elif command[0] == "ls":
            files = self.file_manager.ls()
            i = len(terminal.prev_lines)
            for file in files:
                last_time = os.path.getmtime(file)
                last_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time))
                terminal.appendTerminalText(last_time_str + "\t\t\t\t" + str(file))
                i += 1

        elif command[0] == "cat":
            if len(command) == 2:
                try:
                    self.file_manager.cat(command[1])
                except:
                    terminal.appendTerminalText("Error: Please enter a valid file name.")

            else:
                terminal.appendTerminalText("Error: Please specify a file name.")

        elif command[0] == "mkdir":
            if len(command) == 2:
                try:
                    self.file_manager.mkdir(command[1])
                except:
                    terminal.appendTerminalText("Error: Please enter a valid directory name.")
            else:
                terminal.appendTerminalText("Error: Please specify a directory name.")

        elif command[0] == "rm":
            if len(command) == 2:
                try:
                    self.file_manager.rm(command[1])
                except:
                    terminal.appendTerminalText("Error: Please enter a valid file name.")

            else:
                terminal.appendTerminalText("Error: Please specify a file name.")

        elif command[0] == "rmdir":
            if len(command) == 2:
                try:
                    self.file_manager.rmdir(command[1])
                except:
                    terminal.appendTerminalText("Error: Please enter a valid directory name.")
            else:
                terminal.appendTerminalText("Error: Please specify a directory name.")

        elif command[0] == "pwd":
            if len(command) > 1:
                terminal.appendTerminalText("pwd: too many arguments")
            else:
                self.file_manager.pwd()

        elif command[0] == "mv":
            if len(command) > 1:
                if len(command) < 3:
                    try:
                        self.file_manager.mv(command[1], command[2])
                    except:
                        terminal.appendTerminalText("Error: Please enter a valid file name.")

            else:
                terminal.appendTerminalText("Error: Please specify a file source.")

        elif command[0] == "cp":
            if len(command) > 1:
                if len(command) < 3:
                    try:
                        self.file_manager.cp(command[1], command[2])
                    except:
                        terminal.appendTerminalText("Error: Please enter a valid file name.")

            else:
                terminal.appendTerminalText("Error: Please specify a file source.")

        elif command[0] == "touch":
            if len(command) > 1:
                try:
                    self.file_manager.touch(command[1])
                except:
                    terminal.appendTerminalText("Error: Please enter a valid file name.")

            else:
                terminal.appendTerminalText("Error: Please specify a file name.")

        elif command[0] == "chmod":
            if len(command) > 1:
                if len(command) < 3:
                    try:
                        self.file_manager.chmod(command[1], command[2])
                    except:
                        terminal.appendTerminalText("Error: Please enter a valid file name.")

            else:
                terminal.appendTerminalText("Error: Please specify a file ")

        elif command[0] == "grep":
            if len(command) > 1:
                if len(command) < 3:
                    try:
                        self.file_manager.grep(command[1], command[2])
                    except:
                        terminal.appendTerminalText("Error: Please enter a valid file name.")

            else:
                terminal.appendTerminalText("Error: Please specify a file ")

        elif command[0] == "head":
            if len(command) > 1:
                if len(command) > 2 :
                    try:
                        self.file_manager.head(command[1], command[2])
                    except:
                        terminal.appendTerminalText("Error: Please enter a valid file name.")
                else:
                    try:
                        self.file_manager.head(command[1], 10)
                    except:
                        terminal.appendTerminalText("Error: Please enter a valid file name.")
            else:
                terminal.appendTerminalText("Error: Please enter a valid file name.")

        elif command[0] == "df":
            self.file_manager.df()

        elif command[0] == "wget ":
            if len(command) > 1:
                try:
                    self.file_manager.wget(command[1])
                except:
                    terminal.appendTerminalText("Error: Please enter a valid link")
            else:
                terminal.appendTerminalText("Error: Please specify a link.")

        elif command[0] == "find":
            if len(command) >= 2:
                startpath = command[1]
                name = None
                type = None

                if '-name' in command:
                    try:
                        name_index = command.index('-name')
                        name = command[name_index + 1]
                    except IndexError:
                        terminal.appendTerminalText("Error: Please specify a name after -name flag.")
                        return

                if '-type' in command:
                    try:
                        type_index = command.index('-type')
                        type = command[type_index + 1]
                        if type not in ['f', 'd']:
                            terminal.appendTerminalText("Error: Invalid type. Use 'f' for files or 'd' for directories.")
                            return
                    except IndexError:
                        terminal.appendTerminalText("Error: Please specify a type after -type flag.")
                        return

                try:
                    results = self.file_manager.find(startpath, name=name, type=type)
                    for result in results:
                        terminal.appendTerminalText(result)
                except Exception as e:
                    terminal.appendTerminalText(f"Error: {e}")

            else:
                terminal.appendTerminalText("Error: Please specify a start path.")

        elif command[0] == "echo":
            if len(command) > 1:
                text_to_echo = ' '.join(command[1:])
                terminal.appendTerminalText(text_to_echo)
            else:
                terminal.appendTerminalText("Error: Please specify text to echo.")

        elif command[0] == "date":
            current_date = self.file_manager.date()
            terminal.appendTerminalText(current_date)

        elif command[0] == "whoami":
            terminal.appendTerminalText(self.file_manager.whoami())

        elif command[0] == "uname":
            terminal.appendTerminalText(str(self.file_manager.uname()))

        elif command[0] == "hostname":
            terminal.appendTerminalText(self.file_manager.hostname())

        elif command[0] == "ping":
            if len(command) == 2:
                terminal.appendTerminalText(self.file_manager.ping(command[1]))
            else:
                terminal.appendTerminalText("Error: Please specify a host.")

        elif command[0] == "ps":
            process_list = self.file_manager.ps()
            for process in process_list:
                terminal.appendTerminalText(f"{process['pid']} {process['user']} {process['command']} {process['stat']} {process['start']}")

        elif command[0] == "top":
            process_list = self.file_manager.top()
            for process in process_list:
                terminal.appendTerminalText(f"{process['pid']} {process['username']} {process['name']} {process['cpu_percent']} {process['memory_percent']}")

        elif command[0] == "ifconfig":
            interface_info = self.file_manager.ifconfig()
            for interface, addresses in interface_info.items():
                terminal.appendTerminalText(f"{interface}:")
                for address_info in addresses:
                    terminal.appendTerminalText(f"    inet {address_info['address']} netmask {address_info['netmask']}")

    # ___________________________________________________
    # |Main Terminal Window               | working-    |
    # |900w x 600h                        | tree        |
    # |                                   | 400w x 500h |
    # |                                   |             |
    # |                                   |_____________|
    # |                                   | Options     |
    # |                                   | 400w x 100h |
    # |___________________________________|_____________|

class Window:
    def __init__(self, wid, heit, x_val, y_val, b_color, t_color, font_sz):
        self.width = wid
        self.height = heit
        self.x_cord = x_val
        self.y_cord = y_val
        self.background_color = b_color
        self.text_color = t_color
        self.font_size = font_sz
        self.line_spacing = self.font_size // 2
        self.font = pygame.font.Font('fonts/UbuntuMono-Regular.ttf', self.font_size)
        self.max_rows_of_text = self.height // (self.font.get_height() + self.line_spacing)
        self.text = ""
        self.next_y_for_print = 0
        self.surface = pygame.Surface((self.width, self.height))
    
    def setWidth(self, width):
        self.panel_width = width
    def setHeight(self, height):
        self.panel_height = height
    def setXcord(self, x_val):
        self.x_cord = x_val
    def setYcord(self, y_val):
        self.y_cord = y_val
    def setBackgroundColor(self, color):
        self.background_color = color
    def setTextColor(self, color):
        self.text_color = color
    def setFontSize(self, font_sz):
        self.font_size = font_sz
    def setFont(self, fon):
        self.font = fon
    def setText(self, tex):
        self.text = tex
    def setNextYforPrint(self, n_y):
        self.next_y_for_print = n_y
    def setSurface(self, surf):
        self.surface = surf


class ScrollBar():
    def __init__(self, scroll_pos, wid, heit, x_val, y_val):
        self.scroll_position = scroll_pos
        self.width = wid
        self.height = heit
        self.x_cord = x_val
        self.y_cord = y_val
    
    def setScrollPosition(self, pos):
        self.scroll_position = pos
    def setWidth(self, wid):
        self.width = wid
    def setHeight(self, heit):
        self.height = heit
    def setXcord(self, x_val):
        self.x_cord = x_val
    def setYcord(self, y_val):
        self.y_cord = y_val


class Terminal(Window):
    def __init__(self):
        super().__init__(900, 600, 0, 0, pygame.Color(0,0,0), pygame.Color(255,255,255), 16)
        self.active = True  # can set false if user should click before typing
        self.input_box = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        
        self.scroll_bar = ScrollBar(0, 20 ,35, self.width - 20, 0)

        self.cursor_surface = self.font.render("|", True, self.text_color)
        self.cursor_visible = True
        self.cursor_blink_time = 500  # Time between cursor blinks in milliseconds
        self.cursor_blink_timer = 0

        # Define command history
        self.command_history = []
        self.path_history = []
        self.max_history_length = 50
        self.prev_lines = []
        self.max_prev_lines = 300
        self.history_index = 0

    def setHistoryIndex(self, i):
        self.history_index = i

    def appendTerminalText(self, text_to_add):
        self.prev_lines.append(text_to_add)
        self.setNextYforPrint(self.next_y_for_print + self.font.get_height() + self.line_spacing)

class TreeDiagram(Window):
    def __init__(self):
        super().__init__(400, 500, 900, 0, pygame.Color(8,1,20), pygame.Color(255,255,255), 16)
        self.active = False
        self.input_box = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.scroll_bar = ScrollBar(0, 20 ,35, self.width - 20, 0)

class SettingsOverlay(Window):
    def __init__(self):
        super().__init__(400, 500, 900, 0, pygame.Color(100,100,100), pygame.Color(255,255,255), 16)
        self.color_menu_open = False
        self.overlay = False

        self.ui_manager = pygame_gui.UIManager((1300, 600))

        # custom background color
        self.background_color_picker_button = UIButton(
            relative_rect=pygame.Rect(-310, -550, 220, 30),
            text='Pick Background Color',
            manager=self.ui_manager,
            anchors={'left': 'right', 'right': 'right', 'top': 'bottom', 'bottom': 'bottom'}
        )

        # custom text color
        self.text_color_picker_button = UIButton(
            relative_rect=pygame.Rect(-310, -500, 220, 30),
            text='Pick Text Color',
            manager=self.ui_manager,
            anchors={'left': 'right', 'right': 'right', 'top': 'bottom', 'bottom': 'bottom'}
        )

class HelpOverlay(Window):
    def __init__(self):
        super().__init__(400, 500, 900, 0, pygame.Color(255,255,255), pygame.Color(0,0,0), 16)
        self.overlay = False

class OptionsButtonsPanel(Window):
    def __init__(self):
        super().__init__(400, 100, 900, 600, pygame.Color(15,15,15), pygame.Color(0, 0, 0), 16)

        self.settings_button_rect = pygame.Rect(925, 525, 50, 50)
        self.settings_image = pygame.transform.scale(pygame.image.load("img/settings.png"), (40, 40))

        self.help_button_rect = pygame.Rect(975, 525, 50, 50)
        self.help_image = pygame.transform.scale(pygame.image.load("img/help-button.png"), (50, 50))


def main():
    command_handler = CommandHandler()
    directory_manager = DirectoryManager()

    # Define all windows
    terminal = Terminal()
    tree = TreeDiagram()
    settings = SettingsOverlay()
    helper = HelpOverlay()
    options = OptionsButtonsPanel()

    # Define screen variables
    screen_width = terminal.width + tree.width
    screen_height = terminal.height
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pseudo Terminal")

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
                if terminal.input_box.collidepoint(event.pos):
                    terminal.active = True
                else:
                    terminal.active = False
                
                if tree.input_box.collidepoint(event.pos):
                    tree.active = True
                else:
                    tree.active = False

                # If the user clicked on settings button and the settings aren't up yet
                if options.settings_button_rect.collidepoint(event.pos) and not settings.overlay:
                    settings.overlay = True

                # If the user clicked on settings button while settings are up
                elif options.settings_button_rect.collidepoint(event.pos) and settings.overlay:
                    settings.overlay = False
                    
                # If the user clicked on the help button and the help window isn't up yet
                if options.help_button_rect.collidepoint(event.pos) and not helper.overlay:
                    helper.overlay = True

                # If the user clicked on help window button while help window is up
                elif options.help_button_rect.collidepoint(event.pos) and helper.overlay:
                    helper.overlay = False

                elif event.button == 4 and len(terminal.prev_lines) > terminal.max_rows_of_text and terminal.active:
                    terminal.scroll_bar.scroll_position = max(0, terminal.scroll_bar.scroll_position - 1)
                
                elif event.button == 5 and len(terminal.prev_lines) > terminal.max_rows_of_text and terminal.active:
                    terminal.scroll_bar.scroll_position = min(len(terminal.prev_lines) - terminal.max_rows_of_text + 1, terminal.scroll_bar.scroll_position + 1)

                elif event.button == 4 and len(directory_manager.directory_lines) > tree.max_rows_of_text and tree.active:
                    tree.scroll_bar.scroll_position = max(0, tree.scroll_bar.scroll_position - 1)
                
                elif event.button == 5 and len(directory_manager.directory_lines) > tree.max_rows_of_text and tree.active:
                    tree.scroll_bar.scroll_position = min(len(directory_manager.directory_lines) - tree.max_rows_of_text + 1, tree.scroll_bar.scroll_position + 1)


            # If the user entered a key
            elif event.type == pygame.KEYDOWN:
                if len(terminal.prev_lines) > terminal.max_rows_of_text:
                    terminal.scroll_bar.scroll_position = (len(terminal.prev_lines) - terminal.max_rows_of_text) + 1
                # If the user has clicked onto the terminal window
                if terminal.active:
                    # If user hits 'enter' key
                    if event.key == pygame.K_RETURN:
                        # Update command history
                        terminal.appendTerminalText(current_path + terminal.text)

                        terminal.command_history.append(terminal.text)
                        terminal.path_history.append(current_path)

                        # Process the user's input
                        command_handler.callCommand(terminal)

                        if len(terminal.command_history) > terminal.max_history_length:
                            terminal.command_history.pop(0)
                            terminal.path_history.pop(0)
                        
                        terminal.setHistoryIndex(len(terminal.command_history))

                        if len(terminal.prev_lines) > terminal.max_prev_lines:
                            terminal.prev_lines.pop(0)

                        # Reset user input and go to next line
                        terminal.setText("")

                        if len(terminal.prev_lines) > terminal.max_rows_of_text:
                            terminal.scroll_bar.scroll_position = (len(terminal.prev_lines) - terminal.max_rows_of_text) + 1

                    # If user hits 'backspace' key
                    elif event.key == pygame.K_BACKSPACE:
                        terminal.setText(terminal.text[:-1])

                    # If user hits the up arrow
                    elif event.key == pygame.K_UP:
                        # Cycle to older commands
                        if terminal.history_index > 0:
                            terminal.setHistoryIndex(terminal.history_index - 1)
                            terminal.setText(terminal.command_history[terminal.history_index])
                            current_path = terminal.path_history[terminal.history_index]

                    # If user hits the down arrow
                    elif event.key == pygame.K_DOWN:
                        # Cycle to newer commands
                        if terminal.history_index < len(terminal.command_history) - 1:
                            terminal.setHistoryIndex(terminal.history_index + 1)
                            terminal.setText(terminal.command_history[terminal.history_index])
                            current_path = terminal.path_history[terminal.history_index]

                    # Else: add key to end of user input
                    else:
                        terminal.setText(terminal.text + event.unicode)


            # If user clicks the button to edit background color
            elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == settings.background_color_picker_button:
                settings.color_menu_open = True
                background_color_picker = UIColourPickerDialog(pygame.Rect(905, 50, 390, 390),
                                                settings.ui_manager,
                                                window_title="Change Background Color",
                                                initial_colour=terminal.background_color)
                
                if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                    terminal.setBackgroundColor(event.colour)

            # If user clicks the button to edit text color
            elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == settings.text_color_picker_button:
                color_menu_open = True
                text_color_picker = UIColourPickerDialog(pygame.Rect(905, 50, 390, 390),
                                                settings.ui_manager,
                                                window_title="Change Text Color",
                                                initial_colour=terminal.text_color)
                
                if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                    terminal.setTextColor(event.colour)

            # If user exits out of color menu
            elif event.type == pygame_gui.UI_WINDOW_CLOSE:
                settings.color_menu_open = False
                settings.background_color_picker_button.enable()
                background_color_picker = None
                settings.text_color_picker_button.enable()
                text_color_picker = None

            settings.ui_manager.process_events(event)
            
        # If settings is enable
        if settings.overlay:
            # Draw menu overlay
            helper.overlay = False

            settings.surface.fill(settings.background_color)
            screen.blit(settings.surface, (terminal.width, 0))

            if settings.color_menu_open:
                settings.background_color_picker_button.disable()
                settings.text_color_picker_button.disable()

            else:
                settings.background_color_picker_button.enable()
                settings.text_color_picker_button.enable()

            settings.ui_manager.update(time_delta)
            settings.ui_manager.draw_ui(screen)
            
        elif helper.overlay == 1:
            # Draw menu overlay
            settings.background_color_picker_button.disable()
            settings.text_color_picker_button.disable()
            helper.surface.fill(helper.background_color)
            screen.blit(helper.surface, (terminal.width, 0))
        
        else:
            # Get current directory information
            settings.background_color_picker_button.disable()
            settings.text_color_picker_button.disable()
            tree.surface.fill(tree.background_color)

            # Draw working tree scroll bar if nec. 
            if (len(directory_manager.directory_lines) > tree.max_rows_of_text):
                tree.scroll_bar.setYcord(int(tree.height*((tree.scroll_bar.scroll_position) / (len(directory_manager.directory_lines) - tree.max_rows_of_text))))
                if (tree.scroll_bar.scroll_position == (len(directory_manager.directory_lines) - tree.max_rows_of_text)):
                    tree.scroll_bar.setYcord(tree.height - tree.scroll_bar.height)
                pygame.draw.rect(tree.surface, (20, 120, 220), (tree.scroll_bar.x_cord, tree.scroll_bar.y_cord, tree.scroll_bar.width, tree.scroll_bar.height))
            #updates directory tree
            directory_manager.update_directory_lines()

            for i in range(tree.scroll_bar.scroll_position, min(len(directory_manager.directory_lines), tree.scroll_bar.scroll_position + tree.max_rows_of_text)):
                #tree.setText()
                tree_text = options.font.render(directory_manager.directory_lines[i], True, tree.text_color)
                tree.setNextYforPrint((i - tree.scroll_bar.scroll_position) * (tree.font.get_height() + tree.line_spacing))
                tree.surface.blit(tree_text, (10, tree.next_y_for_print))

            # Draw current directory
            screen.blit(tree.surface, (terminal.width, 0))
            settings.ui_manager.update(time_delta)
        # Get Terminal Ready to be drawn

        # Fill in the terminal background
        terminal.surface.fill(terminal.background_color)

        # Update the path text
        current_path = file_manager.get_path_text()

        # Draw Terminal Scroll bar
        if (len(terminal.prev_lines) > terminal.max_rows_of_text):
            terminal.scroll_bar.setYcord(int(terminal.height*((terminal.scroll_bar.scroll_position) / (len(terminal.prev_lines) - terminal.max_rows_of_text))))
            if (terminal.scroll_bar.scroll_position == (len(terminal.prev_lines) - terminal.max_rows_of_text)):
                terminal.scroll_bar.setYcord(terminal.height - terminal.scroll_bar.height)
            pygame.draw.rect(terminal.surface, (20, 120, 220), (terminal.scroll_bar.x_cord, terminal.scroll_bar.y_cord, terminal.scroll_bar.width, terminal.scroll_bar.height))

        # Draw the current text
        text_surface = terminal.font.render(current_path + terminal.text, True, terminal.text_color)
        
        if len(terminal.prev_lines) == 0:
            terminal.surface.blit(text_surface, (10, 0))

        ########## TODO: FIX BUG WITH SCROLL HERE!!!

        elif len(terminal.prev_lines) > terminal.max_rows_of_text:
            for i in range(terminal.scroll_bar.scroll_position, min(len(terminal.prev_lines), terminal.scroll_bar.scroll_position + terminal.max_rows_of_text)):
                previous_surface = terminal.font.render(terminal.prev_lines[i], True, terminal.text_color)
                terminal.setNextYforPrint((i - terminal.scroll_bar.scroll_position) * (terminal.font.get_height() + terminal.line_spacing))
                terminal.surface.blit(previous_surface, (10, terminal.next_y_for_print))
            
            terminal.surface.blit(text_surface, (10, terminal.next_y_for_print + terminal.font.get_height() + terminal.line_spacing))

        else:
            # Draw the previous commands
            for i in range(terminal.scroll_bar.scroll_position, min(len(terminal.prev_lines), terminal.scroll_bar.scroll_position + terminal.max_rows_of_text)):
                previous_surface = terminal.font.render(terminal.prev_lines[i], True, terminal.text_color)
                terminal.setNextYforPrint((i - terminal.scroll_bar.scroll_position) * (terminal.font.get_height() + terminal.line_spacing))
                terminal.surface.blit(previous_surface, (10, terminal.next_y_for_print))
            
            terminal.surface.blit(text_surface, (10, terminal.next_y_for_print + terminal.font.get_height() + terminal.line_spacing))

        # If the user has clicked onto the terminal
        if terminal.active:
            # Adjust cursor visibility
            if pygame.time.get_ticks() - terminal.cursor_blink_timer > terminal.cursor_blink_time:
                terminal.cursor_blink_timer = pygame.time.get_ticks()
                terminal.cursor_visible = not terminal.cursor_visible

            # Draw Cursor
            if terminal.cursor_visible:
                terminal.cursor_pos = text_surface.get_width() + terminal.line_spacing
                
                if len(terminal.prev_lines) == 0:
                    terminal.surface.blit(terminal.cursor_surface, (terminal.cursor_pos, terminal.next_y_for_print))

                elif len(terminal.prev_lines) > terminal.max_rows_of_text - 1:
                    terminal.surface.blit(terminal.cursor_surface, (terminal.cursor_pos, terminal.height - terminal.font.get_height() - terminal.line_spacing))
                else:
                    terminal.surface.blit(terminal.cursor_surface, (terminal.cursor_pos, terminal.next_y_for_print + terminal.font.get_height() + terminal.line_spacing))

        #Draw Terminal Window
        screen.blit(terminal.surface, (0,0))

        # Draw Options Window  

        options.surface.fill(options.background_color)
        screen.blit(options.surface, (terminal.width, tree.height))
        
        pygame.draw.rect(screen, options.background_color, options.settings_button_rect)
        screen.blit(options.settings_image, (options.settings_button_rect.centerx - 20, options.settings_button_rect.centery - 20))
        pygame.draw.rect(screen, options.background_color, options.help_button_rect)
        screen.blit(options.help_image, (options.help_button_rect.centerx - 25, options.help_button_rect.centery - 25))

        # Update the display
        pygame.display.update()

if __name__ == '__main__':
    main()