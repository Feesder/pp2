import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = WHITE
current_color = BLACK

brush_size = 5
min_brush = 1
max_brush = 50

TOOL_PENCIL = "pencil"
TOOL_RECTANGLE = "rectangle"
TOOL_CIRCLE = "circle"
TOOL_ERASER = "eraser"
tool = TOOL_PENCIL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint_App")
screen.fill(BG_COLOR)

clock = pygame.time.Clock()

color_palette = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (255, 255, 255)
]

font = pygame.font.Font(None, 30)


def draw_ui():
    for i, color in enumerate(color_palette):
        pygame.draw.rect(screen, color, (10 + i * 35, 10, 30, 30))

    pygame.draw.rect(screen, (180, 180, 180), (700, 10, 30, 30))
    pygame.draw.rect(screen, (180, 180, 180), (740, 10, 30, 30))

    plus = font.render("+", True, BLACK)
    minus = font.render("-", True, BLACK)
    screen.blit(plus, (707, 10))
    screen.blit(minus, (747, 10))

    label = font.render(f"Brush: {brush_size}", True, BLACK)
    screen.blit(label, (600, 15))


def get_color_from_palette(pos):
    x, y = pos
    if 10 <= y <= 40:
        for i, color in enumerate(color_palette):
            if 10 + i * 35 <= x <= 10 + i * 35 + 30:
                return color

    return None


drawing = False
start_pos = None

while True:
    clock.tick(FPS)
    draw_ui()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                tool = TOOL_PENCIL

            elif event.key == pygame.K_2:
                tool = TOOL_RECTANGLE

            elif event.key == pygame.K_3:
                tool = TOOL_CIRCLE

            elif event.key == pygame.K_4:
                tool = TOOL_ERASER

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selected = get_color_from_palette(event.pos)
                if selected is not None:
                    current_color = selected
                    tool = TOOL_PENCIL if selected != WHITE else TOOL_ERASER

                elif 700 <= event.pos[0] <= 730 and 10 <= event.pos[1] <= 40:
                    brush_size = min(max_brush, brush_size + 1)

                elif 740 <= event.pos[0] <= 770 and 10 <= event.pos[1] <= 40:
                    brush_size = max(min_brush, brush_size - 1)

                else:
                    drawing = True
                    start_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos
                if tool == TOOL_RECTANGLE:
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    rect = pygame.Rect(min(x1, x2), min(y1, y2),
                                       abs(x2 - x1), abs(y2 - y1))

                    pygame.draw.rect(screen, current_color, rect, brush_size)

                elif tool == TOOL_CIRCLE:
                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                    pygame.draw.circle(screen, current_color, start_pos, radius, brush_size)

                drawing = False

    if drawing and tool in [TOOL_PENCIL, TOOL_ERASER]:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(screen, current_color, mouse_pos, brush_size)

    pygame.display.update()