import pygame
import os
import time

background_color = (0, 0, 0)
text_color = (255, 255, 255)
cursor_color = (255, 255, 255)
font_size = 16
screen_width = 1000
screen_height = 500
active = True # can set false if user should click before typing
next_y = 0
max_lines = 300
prev_lines = []

def cd(path):
    current_path = getPathText()
    os.chdir(current_path[:-2] + "\\" + path)

def ls():
    return os.listdir(os.getcwd())

def cat(file_name):
    new_file = open(file_name,'w')
    new_file.close()

def mkdir(dir_name):
    os.mkdir(dir_name)

def getPathText():
    current_folder = os.getcwd()
    return current_folder + "> "

def callCommand(user_input, font, screen):
    global text_color, prev_lines, max_lines, next_y
    command = user_input.split()

    # if user does not enter anything
    if len(command) == 0:
        return
    
    # Check if the user enters a valid command, if not just reset
    elif command[0] == "cd":
        if len(command) > 1:
            try:    
                cd(command[1])
            except:
                prev_lines.append("Error: Please enter a valid path.")
                next_y += font.get_height() + 8
        else:
            prev_lines.append("Error: Please specify a path.")
            next_y += font.get_height() + 8

    elif command[0] == "ls":
        files = ls()
        i = len(prev_lines)
        for file in files:
            next_y += font.get_height() + 8
            last_time = os.path.getmtime(file)
            last_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time))
            prev_lines.append(str(file) + "\t\t" + last_time_str)
            i+=1

    elif command[0] == "cat":
        if len(command) > 1:
            try:
                cat(command[1])
            except:
                prev_lines.append("Error: Please enter a valid file name.")
                next_y += font.get_height() + 8

        else:
            prev_lines.append("Error: Please specify a file name.")
            next_y += font.get_height() + 8

    if command[0] == "mkdir":
        if len(command) > 1:
            try:
                mkdir(command[1])
            except:
                prev_lines.append("Error: Please enter a valid directory name.")
                next_y += font.get_height() + 8
        else:
            prev_lines.append("Error: Please specify a directory name.")
            next_y += font.get_height() + 8

def main():
    global background_color,text_color, cursor_color, font_size, screen_width,\
    screen_height, active, next_y, prev_lines, max_lines

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Psuedo Terminal")
    font = pygame.font.Font('fonts/UbuntuMono-Regular.ttf', font_size)

    # Define path box
    current_path = getPathText()
    path_surface = font.render(current_path, True, text_color)
    screen.blit(path_surface, (10, 10))

    # Define text input box
    input_box = pygame.Rect(0, 0, screen_width, screen_height)
    input_text = ""
    
    # Define cursor variables
    cursor_surface = font.render("|", True, cursor_color)
    cursor_visible = True
    cursor_blink_time = 500  # Time between cursor blinks in milliseconds
    cursor_blink_timer = 0

    # Define command history
    command_history = []
    path_history = []
    max_history_length = 50
    history_index = 0

    while True:
        # Handle events
        current_path = getPathText()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the user clicked on the input box
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            elif event.type == pygame.KEYDOWN:
                # Check if the user typed a key and clicked on the window
                if active:

                    if event.key == pygame.K_RETURN:
                        # Process the user's input
                        prev_lines.append(current_path + input_text)
                        callCommand(input_text, font, screen)

                        # Update command history
                        command_history.append(input_text)
                        path_history.append(current_path)
                        if len(command_history) > max_history_length:
                            command_history.pop(0)
                            path_history.pop(0)
                        history_index = len(command_history)

                        if len(prev_lines) > max_lines:
                            prev_lines.pop(0)

                        # Reset user input and go to next line
                        input_text = ""
                        next_y += font.get_height() + 8

                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]

                    # Cycle up through commands
                    elif event.key == pygame.K_UP:
                        if history_index > 0:
                            history_index -= 1
                            input_text = command_history[history_index]
                            current_path = path_history[history_index]

                    # Cycle down through commands
                    elif event.key == pygame.K_DOWN:
                        if history_index < len(command_history) - 1:
                            history_index += 1
                            input_text = command_history[history_index]
                            current_path = path_history[history_index]

                    else:
                        input_text += event.unicode  

        # Update the path text
        current_path = getPathText()

        # Draw the terminal background
        screen.fill(background_color)

        # Draw the previous commands
        for i in range(len(prev_lines)):
            previous_surface = font.render(prev_lines[i], True, text_color)
            screen.blit(previous_surface, (10, i * (font.get_height() + 8)))
        
        # Draw the text
        text_surface = font.render(current_path + input_text, True, text_color)
        screen.blit(text_surface, (10, next_y))

        # Draw the cursor
        if active:
            if pygame.time.get_ticks() - cursor_blink_timer > cursor_blink_time:
                cursor_blink_timer = pygame.time.get_ticks()
                cursor_visible = not cursor_visible

            if cursor_visible:
                cursor_pos = text_surface.get_width() + 8
                screen.blit(cursor_surface, (cursor_pos, next_y))

        # Update the display
        pygame.display.update()

main()