import pygame

def main():
    pygame.init()
    screen_width = 800
    screen_height = 600
    ball_radius = 25
    ball_color = (255, 0, 0)
    ball_position = [screen_width // 2, screen_height // 2]
    step_size = 20

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Red Ball movement")

    running = True
    while (running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and ball_position[1] - ball_radius - step_size >= 0:
                    ball_position[1] -= step_size
                    print(ball_position)
                elif event.key == pygame.K_DOWN and ball_position[1] + ball_radius + step_size <= screen_height:
                    ball_position[1] += step_size
                elif event.key == pygame.K_LEFT and ball_position[0] - ball_radius - step_size >= 0:
                    ball_position[0] -= step_size
                elif event.key == pygame.K_RIGHT and ball_position[0] + ball_radius + step_size <= screen_width:
                    ball_position[0] += step_size

        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, ball_color, ball_position, ball_radius)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()