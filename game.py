import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FPS
clock = pygame.time.Clock()


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((100, 20))
        self.surf.fill(BLACK)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Ограничение движения в пределах экрана
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((15, 15))
        self.surf.fill(BLACK)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = [random.choice((-2, 2)), 2]

    def update(self):
        self.rect.move_ip(self.speed)

        # Отражение от стен и потолка
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]

        # Выход из игры, если мяч коснулся нижней части экрана
        if self.rect.bottom >= SCREEN_HEIGHT:
            pygame.quit()
            sys.exit()


class Brick(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
        super().__init__()
        self.surf = pygame.Surface((50, 20))
        self.surf.fill(BLACK)
        self.rect = self.surf.get_rect(center=(xpos, ypos))


# Создадим группы спрайтов
all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
paddle = Paddle()
ball = Ball()
all_sprites.add(paddle)
all_sprites.add(ball)

# Расставляем кирпичики
for i in range(6):  # 6 рядов кирпичей
    for j in range(10):  # 10 кирпичей в ряду
        brick = Brick(j * 55 + 50, i * 25 + 25)
        all_sprites.add(brick)
        bricks.add(brick)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pressed_keys = pygame.key.get_pressed()

    # Обновление
    paddle.update(pressed_keys)
    ball.update()

    # Столкновения мяча с ракеткой
    if pygame.sprite.collide_rect(ball, paddle):
        ball.speed[1] = -ball.speed[1]

    # Столкновения мяча с кирпичами
    hit = pygame.sprite.spritecollide(ball, bricks, dokill=True)
    if hit:
        ball.speed[1] = -ball.speed[1]

    # Отрисовка
    screen.fill(WHITE)
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()
    clock.tick(30)