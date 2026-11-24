
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

frog_left_1 = pygame.transform.flip(frog_image_1, True, False)
frog_left_2 = pygame.transform.flip(frog_image_2, True, False)

missile_image = pygame.transform.scale(pygame.image.load("spaceMissiles_002.png").convert_alpha(), (55, 28))

# Variables
game = "menu"
frog_x, frog_y = 520, 430
frog_direction = "right"

bee_x, bee_y = 95, 200
bee_speed_x, bee_speed_y = 2, 2

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

                    frog_x, frog_y = 520, 430
                    frog_direction = "right"

                    bee_x, bee_y = 95, 200
                    bee_speed_x, bee_speed_y = 2, 2

                    background_x = 0
                    missile_timer = 0
                    missiles = []

                    animation_timer = 0
                    current_frog = frog_image_1
                    score = 0

    # Frog controls
    if game == "playing":

        if keys[pygame.K_LEFT]:
            frog_x -= 5
            frog_direction = "left"

        if keys[pygame.K_RIGHT]:
            frog_x += 5
            frog_direction = "right"

        if keys[pygame.K_UP]:
            frog_y -= 5

        if keys[pygame.K_DOWN]:
            frog_y += 5

        # Keep frog on screen
        if frog_x < 0:
            frog_x = 0
        if frog_x > 825:
            frog_x = 825
        if frog_y < 0:
            frog_y = 0
        if frog_y > 530:
            frog_y = 530

    # Menu
    if game == "menu":
        screen.blit(menu_background, (0, 0))
        screen.blit(big_font.render("FROG ESCAPE!", True, white), (260, 120))
        screen.blit(font.render("Press ENTER to play", True, white), (340, 250))
        screen.blit(font.render("Use ARROW KEYS to move", True, white), (310, 300))
        screen.blit(font.render("P to pause", True, white), (375, 350))

    # Playing
    if game == "playing":

        # Scrolling background
        background_x -= 2

        if background_x <= -900:
            background_x = 0

        screen.blit(game_background, (background_x, 0))
        screen.blit(game_background, (background_x + 900, 0))

        # Frog animation
        animation_timer += 1

        if animation_timer // 13 % 2 == 0:
            current_frog = frog_image_1
        else:
            current_frog = frog_image_2

        if frog_direction == "left":
            if animation_timer // 13 % 2 == 0:
                current_frog = frog_left_1
            else:
                current_frog = frog_left_2

        # Bee movement
        bee_x += bee_speed_x
        bee_y += bee_speed_y

        # Bee bounces off screen edges
        if bee_x <= 0 or bee_x >= 825:
            bee_speed_x = -bee_speed_x

        if bee_y <= 0 or bee_y >= 535:
            bee_speed_y = -bee_speed_y

        bee_rect = pygame.Rect(bee_x, bee_y, 75, 65)
        frog_rect = pygame.Rect(frog_x, frog_y, 75, 70)

        # Check collision with bee
        if frog_rect.colliderect(bee_rect):
            game = "over"

        screen.blit(bee_image, (bee_x, bee_y))

        # Bee fires missiles
        missile_timer += 1

        if missile_timer > 180:
            bee_centre = pygame.Vector2(bee_x + 37, bee_y + 32)
            frog_centre = pygame.Vector2(frog_x + 37, frog_y + 35)

            direction = frog_centre - bee_centre

            if direction.length() > 0:
                direction = direction.normalize()

                missiles.append([
                    bee_centre.x,
                    bee_centre.y,
                    direction.x * 4,
                    direction.y * 4
                ])

            missile_timer = 0

        # Move and draw missiles
        for missile in missiles[:]:

            missile[0] += missile[2]
            missile[1] += missile[3]

            missile_rect = pygame.Rect(missile[0], missile[1], 55, 28)

            screen.blit(missile_image, missile_rect)

            if missile_rect.colliderect(frog_rect):
                game = "over"

            if (missile[0] < -60 or missile[0] > 960 or
                missile[1] < -60 or missile[1] > 660):
                missiles.remove(missile)

        # Draw frog and score
        screen.blit(current_frog, (frog_x, frog_y))

        score += 1
        screen.blit(font.render("Score: " + str(score // 6), True, white), (30, 25))

    # Paused
    if game == "paused":

        # Draw background without scrolling
        screen.blit(game_background, (background_x, 0))
        screen.blit(game_background, (background_x + 900, 0))

        # Draw bee
        screen.blit(bee_image, (bee_x, bee_y))

        # Draw missiles without moving them
        for missile in missiles:
            missile_rect = pygame.Rect(missile[0], missile[1], 55, 28)
            screen.blit(missile_image, missile_rect)

        # Draw frog
        screen.blit(current_frog, (frog_x, frog_y))

        # Draw score
        screen.blit(font.render("Score: " + str(score // 6), True, white), (30, 25))

        # Pause message
        screen.blit(big_font.render("PAUSED", True, white), (350, 220))
        screen.blit(font.render("Press P to resume", True, white), (330, 300))
        screen.blit(font.render("ESC for menu", True, white), (350, 350))

    # Game over
    if game == "over":
        screen.blit(game_background, (0, 0))

        if frog_direction == "left":
            screen.blit(frog_left_1, (frog_x, frog_y))
        else:
            screen.blit(frog_image_1, (frog_x, frog_y))

        screen.blit(bee_image, (bee_x, bee_y))
        screen.blit(big_font.render("GAME OVER", True, black), (285, 200))
        screen.blit(font.render("Score: " + str(score // 6), True, black), (370, 280))
        screen.blit(font.render("Press ENTER to restart", True, black), (290, 350))
        screen.blit(font.render("ESC for menu", True, black), (355, 400))

    pygame.display.flip()

pygame.quit()
