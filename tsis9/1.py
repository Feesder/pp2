import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer with Coins & PNGs")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)

background_img = pygame.image.load("images/road_back.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

player_img = pygame.image.load("images/car.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (60, 80))
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 80))

enemy_img = pygame.image.load("images/enemy_car.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (60, 80))

coin_img = pygame.image.load("images/coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (40, 40))

player_speed = 5
coin_score = 0
enemy_speed_increase = 0
SPEED_UP_EVERY_N_COINS = 5

enemies = []
for _ in range(3):
    x = random.randint(40, WIDTH - 40)
    y = random.randint(-600, -100)
    speed = random.randint(3, 6)
    rect = enemy_img.get_rect(topleft=(x, y))
    enemies.append({"rect": rect, "speed": speed})

coins = []
for _ in range(3):
    x = random.randint(40, WIDTH - 40)
    y = random.randint(-600, -100)
    rect = coin_img.get_rect(topleft=(x, y))
    weight = random.randint(1, 3)
    coins.append({"rect": rect, "weight": weight})

running = True

while running:
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and player_rect.left > 0:
        player_rect.move_ip(-player_speed, 0)

    if keys[pygame.K_d] and player_rect.right < WIDTH:
        player_rect.move_ip(player_speed, 0)

    for enemy in enemies:
        enemy["rect"].y += enemy["speed"]
        if enemy["rect"].top > HEIGHT:
            enemy["rect"].x = random.randint(40, WIDTH - 40)
            enemy["rect"].y = random.randint(-600, -100)
            enemy["speed"] = random.randint(3, 6) + enemy_speed_increase

    for coin in coins:
        coin["rect"].y += 4
        if coin["rect"].top > HEIGHT:
            coin["rect"].x = random.randint(40, WIDTH - 40)
            coin["rect"].y = random.randint(-600, -100)
            coin["weight"] = random.randint(1, 3)

    for enemy in enemies:
        if player_rect.colliderect(enemy["rect"]):
            text = font.render("Game Over!", True, (200, 0, 0))
            screen.blit(text, (WIDTH // 2 - 60, HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

    for coin in coins:
        if player_rect.colliderect(coin["rect"]):
            coin_score += coin["weight"]
            coin["rect"].x = random.randint(40, WIDTH - 40)
            coin["rect"].y = random.randint(-600, -100)
            coin["weight"] = random.randint(1, 3)

            if coin_score // SPEED_UP_EVERY_N_COINS > enemy_speed_increase:
                enemy_speed_increase += 1

    screen.blit(player_img, player_rect)

    for enemy in enemies:
        screen.blit(enemy_img, enemy["rect"])

    for coin in coins:
        screen.blit(coin_img, coin["rect"])

    score_text = font.render(f"Coins: {coin_score}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH - 140, 10))

    pygame.display.update()
    clock.tick(60)