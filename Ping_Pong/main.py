import pygame
from pygame import sprite

pygame.init()

# Class definitions for GameSprite, Player, etc.
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (wight, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def update_l(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

# Game setup
back = (200, 255, 255)
win_width = 600
win_height = 500
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Ping-Pong')
window.fill(back)

# Flags and clock
game = True
finish = False
clock = pygame.time.Clock()
FPS = 60

game_over = False

# Object creation
racket1 = Player('racket.png', 30, 200, 4, 50, 150)
racket2 = Player('racket.png', 520, 200, 4, 50, 150)
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

font = pygame.font.Font(None, 35)
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))

speed_x = 3
speed_y = 3

# Start screen functions
def start_screen():
    intro_text = ["Ты проиграл! ",
                  "Нажмите кнопку, чтобы начать игру"]
    fon = pygame.transform.scale(pygame.image.load('fon.png'), (win_width, win_height))
    window.blit(fon, (0, 0))
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        window.blit(string_rendered, intro_rect)

    # Draw the start button
    pygame.draw.rect(window, (0, 0, 255), (200, 300, 200, 50))
    button_text = font.render('Начать игру', True, (255, 255, 255))
    window.blit(button_text, (240, 310))


# Добавляем функцию для обработки события нажатия на кнопку "начать игру"
def start_game():
    global game, finish, game_over
    game = True
    finish = False
    game_over = False
    racket1.rect.y = 200
    racket2.rect.y = 200
    ball.rect.x = 200
    ball.rect.y = 200

# Основной цикл игры
while game:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if button is clicked and start the game
            if 200 <= event.pos[0] <= 400 and 300 <= event.pos[1] <= 350:
                start_game()

    # Only draw the game screen if not in start menu
    if not finish:
        window.fill(back)
        racket1.update_l()
        racket2.update_r()

        # Ball movement and collision detection
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            speed_y *= 1

        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1

        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))
            game_over = True

        if ball.rect.x > win_width:
            finish = True
            window.blit(lose2, (200, 200))
            game_over = True

        racket1.reset()
        racket2.reset()
        ball.reset()
    else:
        # Draw the start screen if game is not started
        start_screen()
        pygame.display.flip()  # Update the display with start screen

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
