
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frog Escape")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 40, 40)
GREEN = (30, 200, 60)


# ---------------- FROG CLASS ----------------

class Frog:
    def __init__(self):
        self.image1 = pygame.image.load("frog_idle.png").convert_alpha()
        self.image2 = pygame.image.load("frog_rest.png").convert_alpha()

        self.image1 = pygame.transform.scale(self.image1, (75, 70))
        self.image2 = pygame.transform.scale(self.image2, (75, 70))

        self.left1 = pygame.transform.flip(self.image1, True, False)
        self.left2 = pygame.transform.flip(self.image2, True, False)

        self.x = 520
        self.y = 430
        self.direction = "right"
        self.health = 5
        self.animation_timer = 0
        self.fire_timer = 0

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

        self.x = max(0, min(self.x, WIDTH - 75))
        self.y = max(0, min(self.y, HEIGHT - 70))

        self.animation_timer += 1

    def shoot(self, bees):
        if self.fire_timer > 0 or len(bees) == 0:
            return None

        nearest_bee = min(
            bees,
            key=lambda bee: (bee.x - self.x) ** 2 + (bee.y - self.y) ** 2
        )

        direction = pygame.Vector2(
            nearest_bee.x - self.x,
            nearest_bee.y - self.y
        )

        if direction.length() > 0:
            direction = direction.normalize()

        self.fire_timer = 20

        return Bullet(
            self.x + 35,
            self.y + 30,
            direction.x * 8,
            direction.y * 8,
            "frog"
        )

    def draw(self, screen):
        frame = (self.animation_timer // 13) % 2

        if self.direction == "right":
            image = self.image1 if frame == 0 else self.image2
        else:
            image = self.left1 if frame == 0 else self.left2

        screen.blit(image, (self.x, self.y))


# ---------------- BEE CLASS ----------------

class Bee:
    def __init__(self, speed):
        self.image = pygame.image.load("bee_a.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 65))

        self.x = random.choice([20, 800])
        self.y = random.randint(50, 500)

        self.speed_x = random.choice([-speed, speed])
        self.speed_y = random.choice([-speed, speed])

        self.health = 5
        self.fire_timer = random.randint(60, 120)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x <= 0 or self.x >= WIDTH - 75:
            self.speed_x *= -1

        if self.y <= 0 or self.y >= HEIGHT - 65:
            self.speed_y *= -1

    def shoot(self, frog):
        if self.fire_timer > 0:
            self.fire_timer -= 1
            return None

        direction = pygame.Vector2(
            frog.x - self.x,
            frog.y - self.y
        )

        if direction.length() > 0:
            direction = direction.normalize()

        self.fire_timer = 150

        return Bullet(
            self.x + 35,
            self.y + 30,
            direction.x * 6,
            direction.y * 6,
            "bee"
        )

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

        pygame.draw.rect(screen, RED, (self.x, self.y - 10, 50, 6))
        pygame.draw.rect(
            screen,
            GREEN,
            (self.x, self.y - 10, self.health * 10, 6)
        )


# ---------------- BULLET CLASS ----------------

class Bullet:
    def __init__(self, x, y, speed_x, speed_y, owner):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.owner = owner

        self.rect = pygame.Rect(x, y, 55, 28)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.topleft = (self.x, self.y)

    def off_screen(self):
        return (
            self.x < -60 or self.x > WIDTH + 60 or
            self.y < -60 or self.y > HEIGHT + 60
        )

    def draw(self, screen, image):
        screen.blit(image, (self.x, self.y))


# ---------------- GAME CLASS ----------------

class Game:
    def __init__(self):
        self.menu_background = pygame.image.load(
            "background_solid_dirt.png"
        ).convert()

        self.menu_background = pygame.transform.scale(
            self.menu_background, (WIDTH, HEIGHT)
        )

        self.background = pygame.image.load(
            "background_color_trees.png"
        ).convert()

        self.background = pygame.transform.scale(
            self.background, (WIDTH, HEIGHT)
        )

        self.bullet_image = pygame.image.load(
            "spaceMissiles_002.png"
        ).convert_alpha()

        self.bullet_image = pygame.transform.scale(
            self.bullet_image, (55, 28)
        )

        self.state = "menu"
        self.reset()

        self.state = "menu"

    def reset(self):
        self.frog = Frog()
        self.bees = [Bee(2)]
        self.bullets = []

        self.bee_kills = 0
        self.background_x = 0
        self.score = 0

    # ---------------- EVENTS ----------------

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

                elif event.key == pygame.K_RETURN:

                    if self.state == "menu" or self.state == "game_over":
                        self.reset()
                        self.state = "playing"

                elif event.key == pygame.K_SPACE and self.state == "playing":

                    bullet = self.frog.shoot(self.bees)

                    if bullet:
                        self.bullets.append(bullet)

        return True

    # ---------------- UPDATE ----------------

    def update(self):
        keys = pygame.key.get_pressed()

        self.frog.move(keys)

        if self.frog.fire_timer > 0:
            self.frog.fire_timer -= 1

        for bee in self.bees:
            bee.move()

            bullet = bee.shoot(self.frog)

            if bullet:
                self.bullets.append(bullet)

        # Move bullets

        for bullet in self.bullets[:]:
            bullet.move()

            if bullet.off_screen():
                self.bullets.remove(bullet)

        # Check bullet collisions

        for bullet in self.bullets[:]:

            if bullet.owner == "frog":

                for bee in self.bees[:]:
                    bee_rect = pygame.Rect(bee.x, bee.y, 75, 65)

                    if bullet.rect.colliderect(bee_rect):
                        bee.health -= 1
                        self.bullets.remove(bullet)
                        break

            elif bullet.owner == "bee":

                frog_rect = pygame.Rect(
                    self.frog.x, self.frog.y, 75, 70
                )

                if bullet.rect.colliderect(frog_rect):
                    self.frog.health -= 1
                    self.bullets.remove(bullet)

                    if self.frog.health <= 0:
                        self.state = "game_over"

        # Remove dead bees and spawn new ones

        for bee in self.bees[:]:

            if bee.health <= 0:
                self.bees.remove(bee)

                self.bee_kills += 1
                speed = 2 + self.bee_kills * 0.3

                self.bees.append(Bee(speed))
                self.bees.append(Bee(speed))

        # Check frog and bee collisions

        frog_rect = pygame.Rect(
            self.frog.x, self.frog.y, 75, 70
        )

        for bee in self.bees:

            bee_rect = pygame.Rect(bee.x, bee.y, 75, 65)

            if frog_rect.colliderect(bee_rect):
                self.frog.health = 0
                self.state = "game_over"
                break

        self.score += 1

    # ---------------- BACKGROUND ----------------

    def draw_background(self):
        self.background_x -= 1

        if self.background_x <= -WIDTH:
            self.background_x = 0

        screen.blit(self.background, (self.background_x, 0))
        screen.blit(self.background, (self.background_x + WIDTH, 0))

    # ---------------- FROG HEALTH ----------------

    def draw_frog_health(self):
        pygame.draw.rect(screen, RED, (20, 20, 150, 20))

        pygame.draw.rect(
            screen,
            GREEN,
            (20, 20, self.frog.health * 30, 20)
        )

        font = pygame.font.SysFont(None, 25)
        text = font.render("Frog Health", True, WHITE)
        screen.blit(text, (180, 20))

    # ---------------- MENU ----------------

    def draw_menu(self):
        screen.blit(self.menu_background, (0, 0))

        font = pygame.font.SysFont(None, 70)
        title = font.render("FROG ESCAPE", True, WHITE)

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 180)
        )

        font = pygame.font.SysFont(None, 35)

        text = font.render("Press ENTER to Start", True, WHITE)

        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, 300)
        )

        text = font.render(
            "Arrow Keys = Move    SPACE = Fire",
            True, WHITE
        )

        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, 370)
        )

        text = font.render("ESC = Quit", True, WHITE)

        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, 420)
        )

    # ---------------- GAME SCREEN ----------------

    def draw_game(self):
        self.draw_background()

        for bee in self.bees:
            bee.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen, self.bullet_image)

        self.frog.draw(screen)
        self.draw_frog_health()

        font = pygame.font.SysFont(None, 30)

        score_text = font.render(
            "Score: " + str(self.score // 6), True, WHITE
        )

        screen.blit(score_text, (750, 20))

        bee_text = font.render(
            "Bees: " + str(len(self.bees)), True, WHITE
        )

        screen.blit(bee_text, (750, 50))

    # ---------------- GAME OVER ----------------

    def draw_game_over(self):
        self.draw_background()

        for bee in self.bees:
            bee.draw(screen)

        self.frog.draw(screen)
        self.draw_frog_health()

        font = pygame.font.SysFont(None, 75)
        text = font.render("GAME OVER", True, BLACK)

        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, 200)
        )

        font = pygame.font.SysFont(None, 35)

        text = font.render(
            "Score: " + str(self.score // 6), True, BLACK
        )

        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, 290)
        )

        text = font.render(
            "ENTER = Restart    ESC = Menu",
            True, BLACK
        )

        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, 350)
        )

    # ---------------- DRAW ----------------

    def draw(self):
        if self.state == "menu":
            self.draw_menu()

        elif self.state == "playing":
            self.draw_game()

        elif self.state == "game_over":
            self.draw_game_over()


# ---------------- MAIN PROGRAM ----------------

game = Game()
running = True

while running:

    clock.tick(60)

    running = game.events()

    if game.state == "playing":
        game.update()

    game.draw()

    pygame.display.flip()

pygame.quit()
