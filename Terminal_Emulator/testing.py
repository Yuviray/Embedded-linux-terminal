import pygame
import os

def cd(path):
    current_path = getPathText()
    
    try:
        os.chdir(current_path[:-2] + "\\" + path)
    except:
        print("Error: Please enter a valid path.")


def getPathText():
    current_folder = os.getcwd()
    return current_folder + "> "

def callCommand(user_input):
    command = user_input.split()

    if command[1] == "cd":
        if len(command) > 2:
            cd(command[2])

        else:
            print("Error: Please specify a path.")

def main():
    # Initialize Pygame
    pygame.init()

    # Set the screen size
    screen_width = 1000
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Define terminal colors
    background_color = (0, 0, 0)
    text_color = (255, 255, 255)
    cursor_color = (255, 255, 255)

    # Define font
    font_size = 16
    font = pygame.font.Font('fonts/UbuntuMono-Regular.ttf', font_size)

    # Define text input box
    input_box = pygame.Rect(0, 0, screen_width, screen_height)
    pathText = getPathText()
    text = pathText
    active = True # can set false if user should click before typing
    next_y = 0

    # Define cursor variables
    cursor_surface = font.render("|", True, cursor_color)
    cursor_visible = True
    cursor_blink_time = 500  # Time between cursor blinks in milliseconds
    cursor_blink_timer = 0

    # Define command history
    command_history = []
    max_history_length = 50
    history_index = 0
        
    # Game loop
    while True:
        # Handle events
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
                        callCommand(text)

                        # Update command history
                        command_history.append(text)
                        if len(command_history) > max_history_length:
                            command_history.pop(0)
                        history_index = len(command_history)

                        # update previous command output
                        output_surface =  font.render(text, True, text_color)
                        screen.blit(output_surface, (10, next_y))
                        text = getPathText()
                        next_y += font.get_height() + 8

                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]

                    elif event.key == pygame.K_UP:
                        if history_index > 0:
                            history_index -= 1
                            text = command_history[history_index]

                    elif event.key == pygame.K_DOWN:
                        if history_index < len(command_history) - 1:
                            history_index += 1
                            text = command_history[history_index]

                    else:
                        text += event.unicode  

        # Update the path text
        pathText = getPathText()

        # Draw the terminal background
        screen.fill(background_color)

        # Draw the previous commands
        for i in range(len(command_history)):
            command_surface = font.render(command_history[i], True, text_color)
            screen.blit(command_surface, (10, i * (font.get_height() + 8)))
        
        # Draw the text
        text_surface = font.render(text, True, text_color)
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