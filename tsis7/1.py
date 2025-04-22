from datetime import datetime

import pygame

def main():
    pygame.init()
    screen_width = 800
    screen_height = 600
    center = [screen_width // 2, screen_height // 2]

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Mickey clock')

    original_right_arm = pygame.image.load('images/rightarm.png')
    new_width = original_right_arm.get_width() * 3 / 4
    new_height = original_right_arm.get_height() * 3 / 4
    original_right_arm = pygame.transform.scale(original_right_arm, (new_width, new_height))
    original_left_arm = pygame.image.load('images/leftarm.png')
    new_width = original_left_arm.get_width() * 3 / 4
    new_height = original_left_arm.get_height() * 3 / 4
    original_left_arm = pygame.transform.scale(original_left_arm, (new_width, new_height))

    clock = pygame.image.load('images/clock.png')
    pygame.display.set_icon(clock)
    clock = pygame.transform.scale(clock, (screen_width, screen_height))

    running = True
    while running:
        now = datetime.now()

        right_arm = pygame.transform.rotate(original_right_arm, -now.minute * 6 - 50)
        right = right_arm.get_rect(center=center)

        left_arm = pygame.transform.rotate(original_left_arm, -now.second * 6)
        left = left_arm.get_rect(center=center)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        screen.blit(clock, (0, 0))
        screen.blit(right_arm, right)
        screen.blit(left_arm, left)
        pygame.display.flip()

if __name__ == '__main__':
    main()