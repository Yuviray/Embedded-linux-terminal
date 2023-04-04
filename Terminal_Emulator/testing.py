import pygame

def getPathText():
    pathText = "PS C:\\Users\\user>"
    return pathText

def setCommand(userInput):
    print(userInput)

def main():
    # Initialize Pygame
    pygame.init()

    # Set the screen size
    screen_width = 800
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Define terminal colors
    background_color = (0, 0, 0)
    text_color = (255, 255, 255)
    cursor_color = (255, 255, 255)

    # Define font
    font_size = 24
    font = pygame.font.Font('fonts/UbuntuMono-Regular.ttf', font_size)

    # Define text input box
    input_box = pygame.Rect(0, 0, screen_width - 20, font_size * 2)
    text = ""
    pathText = getPathText()
    active = False

    # Define cursor variables
    cursor_surface = font.render("|", True, cursor_color)
    cursor_visible = True
    cursor_blink_time = 500  # Time between cursor blinks in milliseconds
    cursor_blink_timer = 0
        
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
                # Check if the user typed a key
                if active:
                    if event.key == pygame.K_RETURN:
                        # Process the user's input
                        setCommand(text)
                        text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode    

        # Draw the terminal background
        screen.fill(background_color)

        # Draw the text
        text_surface = font.render(pathText + " " + text, True, text_color)
        screen.blit(text_surface, (0, 10))

            # Draw the cursor
        if active:
            if pygame.time.get_ticks() - cursor_blink_timer > cursor_blink_time:
                cursor_blink_timer = pygame.time.get_ticks()
                cursor_visible = not cursor_visible

            if cursor_visible:
                cursor_pos = text_surface.get_width()
                screen.blit(cursor_surface, (cursor_pos, 10))

        # Update the display
        pygame.display.update()


main()