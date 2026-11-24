
import pygame

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frog Escape")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 75)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# FROG CLASS
class Frog:

    def __init__(self):
        self.image_1 = pygame.transform.scale(
            pygame.image.load("frog_idle.png").convert_alpha(), (75, 70))

        self.image_2 = pygame.transform.scale(
            pygame.image.load("frog_rest.png").convert_alpha(), (75, 70))

        self.left_1 = pygame.transform.flip(self.image_1, True, False)
        self.left_2 = pygame.transform.flip(self.image_2, True, False)

        self.x = 520
        self.y = 430
        self.direction = "right"
        self.animation_timer = 0
        self.image = self.image_1

        self.rect = pygame.Rect(self.x, self.y, 75, 70)

    def move(self, keys):

        if keys[pygame.K_LEFT]:
            self.x -= 5
            self.direction = "left"

        if keys[pygame.K_RIGHT]:
            self.x += 5
            self.direction = "right"

        if keys[pygame.K_UP]:
            self.y -= 5

        if keys[pygame.K_DOWN]:
            self.y += 5

        self.x = max(0, min(self.x, 825))
        self.y = max(0, min(self.y, 530))

        self.rect.topleft = (self.x, self.y)

    def animate(self):

        self.animation_timer += 1

        if self.animation_timer // 13 % 2 == 0:
            if self.direction == "left":
                self.image = self.left_1
            else:
                self.image = self.image_1
        else:
            if self.direction == "left":
                self.image = self.left_2
            else:
                self.image = self.image_2

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


# BEE CLASS
class Bee:

    def __init__(self):

        self.image = pygame.transform.scale(
            pygame.image.load("bee_a.png").convert_alpha(), (75, 65))

        self.x = 95
        self.y = 200
        self.speed_x = 2
        self.speed_y = 2

        self.rect = pygame.Rect(self.x, self.y, 75, 65)

    def move(self):

        self.x += self.speed_x
        self.y += self.speed_y

        if self.x <= 0 or self.x >= 825:
            self.speed_x = -self.speed_x

        if self.y <= 0 or self.y >= 535:
            self.speed_y = -self.speed_y

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def shoot(self, frog):

        bee_centre = pygame.Vector2(self.x + 37, self.y + 32)
        frog_centre = pygame.Vector2(frog.x + 37, frog.y + 35)

        direction = frog_centre - bee_centre

        if direction.length() > 0:
            direction = direction.normalize()

            return Missile(
                bee_centre.x,
                bee_centre.y,
                direction.x * 4,
                direction.y * 4
            )

        return None


# MISSILE CLASS
class Missile:

    def __init__(self, x, y, speed_x, speed_y):

        self.image = pygame.transform.scale(
            pygame.image.load("spaceMissiles_002.png").convert_alpha(), (55, 28))

        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

        self.rect = pygame.Rect(self.x, self.y, 55, 28)

    def move(self):

        self.x += self.speed_x
        self.y += self.speed_y

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self):
        return (self.x < -60 or self.x > 960 or
                self.y < -60 or self.y > 660)


# GAME CLASS
class Game:

    def __init__(self):

        self.menu_background = pygame.transform.scale(
            pygame.image.load("background_solid_dirt.png").convert(), (WIDTH, HEIGHT))

        self.background = pygame.transform.scale(
            pygame.image.load("background_color_trees.png").convert(), (WIDTH, HEIGHT))

        self.frog = Frog()
        self.bee = Bee()

        self.missiles = []
        self.missile_timer = 0

        self.background_x = 0
        self.score = 0
        self.state = "menu"

    def reset(self):

        self.frog = Frog()
        self.bee = Bee()
        self.missiles = []
        self.missile_timer = 0
        self.background_x = 0
        self.score = 0
        self.state = "playing"

    def events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    if self.state == "menu":
                        return False
                    else:
                        self.state = "menu"

                if event.key == pygame.K_RETURN and self.state != "playing":
                    self.reset()

        return True

    def update(self):

        keys = pygame.key.get_pressed()

        self.frog.move(keys)
        self.frog.animate()

        self.bee.move()

        # Bee shooting
        self.missile_timer += 1

        if self.missile_timer > 180:
            missile = self.bee.shoot(self.frog)

            if missile:
                self.missiles.append(missile)

            self.missile_timer = 0

        # Move missiles
        for missile in self.missiles[:]:

            missile.move()

            if missile.off_screen():
                self.missiles.remove(missile)

            elif missile.rect.colliderect(self.frog.rect):
                self.state = "over"

        # Check bee collision
        if self.frog.rect.colliderect(self.bee.rect):
            self.state = "over"

        self.score += 1

    def draw_background(self):

        self.background_x -= 2

        if self.background_x <= -WIDTH:
            self.background_x = 0

        screen.blit(self.background, (self.background_x, 0))
        screen.blit(self.background, (self.background_x + WIDTH, 0))

    def draw_menu(self):

        screen.blit(self.menu_background, (0, 0))
        screen.blit(big_font.render("FROG ESCAPE!", True, WHITE), (260, 120))
        screen.blit(font.render("Press ENTER to play", True, WHITE), (340, 250))
        screen.blit(font.render("Use ARROW KEYS to move", True, WHITE), (310, 300))

    def draw_game(self):

        self.draw_background()

        self.bee.draw(screen)

        for missile in self.missiles:
            missile.draw(screen)

        self.frog.draw(screen)

        screen.blit(
            font.render("Score: " + str(self.score // 6), True, WHITE),
            (30, 25)
        )

    def draw_game_over(self):

        screen.blit(self.background, (0, 0))

        self.frog.draw(screen)
        self.bee.draw(screen)

        screen.blit(big_font.render("GAME OVER", True, BLACK), (285, 200))
        screen.blit(font.render("Score: " + str(self.score // 6), True, BLACK), (370, 280))
        screen.blit(font.render("Press ENTER to restart", True, BLACK), (290, 350))
        screen.blit(font.render("ESC for menu", True, BLACK), (355, 400))

    def draw(self):

        if self.state == "menu":
            self.draw_menu()

        elif self.state == "playing":
            self.draw_game()

        elif self.state == "over":
            self.draw_game_over()


# CREATE GAME
game = Game()
running = True

# MAIN GAME LOOP
while running:

    clock.tick(60)

    running = game.events()

    if game.state == "playing":
        game.update()

    game.draw()

    pygame.display.flip()

pygame.quit()
