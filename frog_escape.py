
import pygame

pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Frog Escape")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 75)

# Images
menu_background = pygame.transform.scale(pygame.image.load("background_solid_dirt.png").convert(), (900, 600))
game_background = pygame.transform.scale(pygame.image.load("background_color_trees.png").convert(), (900, 600))
bee_image = pygame.transform.scale(pygame.image.load("bee_a.png").convert_alpha(), (75, 65))

frog_image_1 = pygame.transform.scale(pygame.image.load("frog_idle.png").convert_alpha(), (75, 70))
frog_image_2 = pygame.transform.scale(pygame.image.load("frog_rest.png").convert_alpha(), (75, 70))

# Frog images facing left
frog_left_1 = pygame.transform.flip(frog_image_1, True, False)
frog_left_2 = pygame.transform.flip(frog_image_2, True, False)

missile_image = pygame.transform.scale(pygame.image.load("spaceMissiles_002.png").convert_alpha(), (55, 28))

# Variables
game = "menu"
frog_x, frog_y, jump_speed = 520, 430, 0
frog_direction = "right"
bee_x, bee_y = 95, 395
background_x = 0
missile_timer = 0
missiles = []
animation_timer = 0
current_frog = frog_image_1
score = 0
white = (255, 255, 255)
black = (0, 0, 0)

running = True

while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                game = "menu" if game != "menu" else "quit"

                if game == "quit":
                    running = False

            # Pause and resume
            if event.key == pygame.K_p:
                if game == "playing":
                    game = "paused"
                elif game == "paused":
                    game = "playing"

            if event.key == pygame.K_RETURN and game != "playing":
                if game == "menu" or game == "over":
                    game = "playing"
                    frog_x, frog_y, jump_speed = 520, 430, 0
                    frog_direction = "right"
                    bee_x, background_x = 95, 0
                    missile_timer, score = 0, 0
                    missiles = []
                    animation_timer = 0
                    current_frog = frog_image_1

    # Frog controls
    if game == "playing":
        if keys[pygame.K_LEFT]:
            frog_x -= 5
            frog_direction = "left"

        if keys[pygame.K_RIGHT]:
            frog_x += 5
            frog_direction = "right"

        if keys[pygame.K_SPACE] and frog_y == 430:
            jump_speed = -22

        if frog_x < 0:
            frog_x = 0

        if frog_x > 825:
            frog_x = 825

    # Menu
    if game == "menu":
        screen.blit(menu_background, (0, 0))
        screen.blit(big_font.render("FROG ESCAPE!", True, white), (260, 120))
        screen.blit(font.render("Press ENTER to play", True, white), (340, 250))
        screen.blit(font.render("SPACE to jump", True, white), (365, 300))
        screen.blit(font.render("P to pause", True, white), (375, 350))

    # Playing
    if game == "playing":

        # Scrolling background
        background_x -= 2

        if background_x <= -900:
            background_x = 0

        screen.blit(game_background, (background_x, 0))
        screen.blit(game_background, (background_x + 900, 0))

        # Frog jumping movement
        frog_y += jump_speed
        jump_speed += 0.6

        if frog_y >= 430:
            frog_y, jump_speed = 430, 0

        # Frog animation
        animation_timer += 1

        if animation_timer // 13 % 2 == 0:
            current_frog = frog_image_1
        else:
            current_frog = frog_image_2

        # Change direction of frog image
        if frog_direction == "left":
            if animation_timer // 13 % 2 == 0:
                current_frog = frog_left_1
            else:
                current_frog = frog_left_2

        # Bee and collision
        frog_rect = pygame.Rect(frog_x, frog_y, 75, 70)
        bee_rect = pygame.Rect(bee_x, bee_y, 75, 65)

        bee_x += 0.1
        bee_rect.x = bee_x

        if frog_rect.colliderect(bee_rect):
            game = "over"

        screen.blit(bee_image, (bee_x, bee_y))

        # Missiles
        missile_timer += 1

        if missile_timer > 240:
            missiles.append(pygame.Rect(bee_x + 55, bee_y + 25, 55, 28))
            missile_timer = 0

        for missile_rect in missiles[:]:
            missile_rect.x += 3
            screen.blit(missile_image, missile_rect)

            if missile_rect.colliderect(frog_rect):
                game = "over"

            if missile_rect.x > 900:
                missiles.remove(missile_rect)

        # Draw frog and score
        screen.blit(current_frog, (frog_x, frog_y))

        score += 1
        screen.blit(font.render("Score: " + str(score // 6), True, white), (30, 25))

    # Paused screen
    if game == "paused":
        screen.blit(game_background, (0, 0))

        # Draw the current game objects without moving them
        screen.blit(bee_image, (bee_x, bee_y))

        for missile_rect in missiles:
            screen.blit(missile_image, missile_rect)

        screen.blit(current_frog, (frog_x, frog_y))

        screen.blit(font.render("Score: " + str(score // 6), True, white), (30, 25))

        screen.blit(big_font.render("PAUSED", True, white), (350, 220))
        screen.blit(font.render("Press P to resume", True, white), (330, 300))
        screen.blit(font.render("ESC for menu", True, white), (350, 350))

    # Game over
    if game == "over":
        screen.blit(game_background, (0, 0))

        if frog_direction == "left":
            screen.blit(frog_left_1, (frog_x, 430))
        else:
            screen.blit(frog_image_1, (frog_x, 430))

        screen.blit(bee_image, (bee_x, bee_y))
        screen.blit(big_font.render("GAME OVER", True, black), (285, 200))
        screen.blit(font.render("Score: " + str(score // 6), True, black), (370, 280))
        screen.blit(font.render("Press ENTER to restart", True, black), (290, 350))
        screen.blit(font.render("ESC for menu", True, black), (355, 400))

    pygame.display.flip()

pygame.quit()
