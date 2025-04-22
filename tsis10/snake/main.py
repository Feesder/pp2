import pygame
import random
import sys
import psycopg2


# Database connection setup
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="tsis_nine",
            user="yerdos",
            password="Xad7rZbD863nfUAGTWb5S6p3y6wyXG44",
            host="localhost"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        sys.exit(1)


# Initialize database tables
def initialize_database():
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            # Create user table if not exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create user_score table if not exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_scores (
                    score_id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(user_id),
                    score INTEGER NOT NULL,
                    level INTEGER NOT NULL,
                    saved_state TEXT,
                    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    except psycopg2.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()


# Game initialization
pygame.init()
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 36)


# Game state
class GameState:
    def __init__(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.score = 0
        self.level = 1
        self.speed = 10
        self.walls = []
        self.food = None
        self.food_weight = 1
        self.food_timer = 0
        self.FOOD_LIFESPAN = 300
        self.paused = False
        self.game_over = False
        self.username = ""
        self.user_id = None
        self.input_active = True
        self.input_text = ""

    def reset(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.score = 0
        self.level = 1
        self.speed = 10
        self.walls = []
        self.food = None
        self.food_weight = 1
        self.food_timer = 0
        self.paused = False
        self.game_over = False
        self.generate_walls()
        self.food = self.get_food_position()
        self.food_weight = random.randint(1, 3)
        self.food_timer = self.FOOD_LIFESPAN

    def generate_walls(self):
        # Basic walls for level 1
        self.walls = []
        for x in range(COLS):
            self.walls.append((x, 0))
            self.walls.append((x, ROWS - 1))

        for y in range(ROWS):
            self.walls.append((0, y))
            self.walls.append((COLS - 1, y))

        # Add more obstacles for higher levels
        if self.level >= 2:
            # Add horizontal barriers
            for x in range(5, COLS - 5):
                self.walls.append((x, 10))
                self.walls.append((x, ROWS - 10))

        if self.level >= 3:
            # Add vertical barriers
            for y in range(5, ROWS - 5):
                self.walls.append((10, y))
                self.walls.append((COLS - 10, y))

        if self.level >= 4:
            # Add cross in the middle
            for x in range(COLS // 2 - 3, COLS // 2 + 3):
                self.walls.append((x, ROWS // 2))
            for y in range(ROWS // 2 - 3, ROWS // 2 + 3):
                self.walls.append((COLS // 2, y))

    def get_food_position(self):
        while True:
            x = random.randint(1, COLS - 2)
            y = random.randint(1, ROWS - 2)
            if (x, y) not in self.snake and (x, y) not in self.walls:
                return (x, y)

    def serialize_state(self):
        return {
            "snake": self.snake,
            "direction": self.direction,
            "score": self.score,
            "level": self.level,
            "speed": self.speed,
            "food": self.food,
            "food_weight": self.food_weight,
            "food_timer": self.food_timer
        }

    def deserialize_state(self, state_data):
        self.snake = state_data["snake"]
        self.direction = state_data["direction"]
        self.score = state_data["score"]
        self.level = state_data["level"]
        self.speed = state_data["speed"]
        self.food = state_data["food"]
        self.food_weight = state_data["food_weight"]
        self.food_timer = state_data["food_timer"]
        self.generate_walls()


# Database functions
def get_or_create_user(username):
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            # Check if user exists
            cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            result = cur.fetchone()

            if result:
                user_id = result[0]
                # Get the highest score for this user
                cur.execute("""
                    SELECT score, level FROM user_scores 
                    WHERE user_id = %s 
                    ORDER BY score DESC 
                    LIMIT 1
                """, (user_id,))
                score_data = cur.fetchone()
                return user_id, score_data
            else:
                # Create new user
                cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING user_id", (username,))
                user_id = cur.fetchone()[0]
                conn.commit()
                return user_id, None
    except psycopg2.Error as e:
        print(f"Error in get_or_create_user: {e}")
        return None, None
    finally:
        conn.close()


def save_game_state(user_id, game_state):
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO user_scores (user_id, score, level, saved_state)
                VALUES (%s, %s, %s, %s)
            """, (user_id, game_state.score, game_state.level, str(game_state.serialize_state())))
            conn.commit()
    except psycopg2.Error as e:
        print(f"Error saving game state: {e}")
    finally:
        conn.close()


def get_saved_state(user_id):
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT saved_state FROM user_scores 
                WHERE user_id = %s 
                ORDER BY saved_at DESC 
                LIMIT 1
            """, (user_id,))
            result = cur.fetchone()
            return eval(result[0]) if result else None
    except psycopg2.Error as e:
        print(f"Error getting saved state: {e}")
        return None
    finally:
        conn.close()


# Drawing functions
def draw_game(game_state):
    screen.fill(BLACK)

    # Draw walls
    for wall in game_state.walls:
        pygame.draw.rect(screen, GRAY, (wall[0] * CELL_SIZE, wall[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw snake
    for segment in game_state.snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw food
    if game_state.food:
        pygame.draw.rect(screen, RED,
                         (game_state.food[0] * CELL_SIZE, game_state.food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        weight_text = font.render(str(game_state.food_weight), True, YELLOW)
        screen.blit(weight_text, (game_state.food[0] * CELL_SIZE + 5, game_state.food[1] * CELL_SIZE + 2))

    # Draw score and level
    score_text = font.render(f"Score: {game_state.score}", True, WHITE)
    level_text = font.render(f"Level: {game_state.level}", True, WHITE)
    user_text = font.render(f"User: {game_state.username}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 120, 10))
    screen.blit(user_text, (WIDTH // 2 - 60, 10))

    # Draw pause indicator
    if game_state.paused:
        pause_text = large_font.render("PAUSED", True, BLUE)
        screen.blit(pause_text, (WIDTH // 2 - 70, HEIGHT // 2 - 30))
        hint_text = font.render("Press P to resume", True, WHITE)
        screen.blit(hint_text, (WIDTH // 2 - 80, HEIGHT // 2 + 20))

    pygame.display.update()


def draw_username_input(game_state):
    screen.fill(BLACK)

    title_text = large_font.render("Snake Game", True, GREEN)
    prompt_text = font.render("Enter your username:", True, WHITE)
    input_text = font.render(game_state.input_text, True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
    screen.blit(prompt_text, (WIDTH // 2 - 100, HEIGHT // 2 - 30))
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 150, HEIGHT // 2, 300, 40), 2)
    screen.blit(input_text, (WIDTH // 2 - 140, HEIGHT // 2 + 10))

    hint_text = font.render("Press ENTER to continue", True, GRAY)
    screen.blit(hint_text, (WIDTH // 2 - 120, HEIGHT // 2 + 60))

    pygame.display.update()


def show_game_over_screen(game_state):
    screen.fill(BLACK)

    game_over_text = large_font.render("💥 Game Over!", True, RED)
    score_text = font.render(f"Final Score: {game_state.score}", True, WHITE)
    level_text = font.render(f"Level Reached: {game_state.level}", True, WHITE)
    hint_text = font.render("Press ESC to quit or R to restart", True, GRAY)

    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
    screen.blit(level_text, (WIDTH // 2 - 80, HEIGHT // 2 + 20))
    screen.blit(hint_text, (WIDTH // 2 - 150, HEIGHT // 2 + 60))

    pygame.display.update()


def show_welcome_screen(game_state, previous_score=None):
    screen.fill(BLACK)

    welcome_text = large_font.render(f"Welcome, {game_state.username}!", True, GREEN)
    screen.blit(welcome_text, (WIDTH // 2 - 150, HEIGHT // 2 - 80))

    if previous_score:
        prev_score_text = font.render(f"Your previous high score: {previous_score[0]}", True, WHITE)
        prev_level_text = font.render(f"Previous level reached: {previous_score[1]}", True, WHITE)
        screen.blit(prev_score_text, (WIDTH // 2 - 120, HEIGHT // 2 - 20))
        screen.blit(prev_level_text, (WIDTH // 2 - 120, HEIGHT // 2 + 20))
    else:
        new_user_text = font.render("New user - let's get started!", True, WHITE)
        screen.blit(new_user_text, (WIDTH // 2 - 120, HEIGHT // 2))

    hint_text = font.render("Press SPACE to start or L to load last saved", True, GRAY)
    screen.blit(hint_text, (WIDTH // 2 - 200, HEIGHT // 2 + 80))

    pygame.display.update()


# Main game function
def main():
    initialize_database()
    game_state = GameState()

    # Username input loop
    while game_state.input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_state.input_text:
                        game_state.username = game_state.input_text
                        game_state.user_id, previous_score = get_or_create_user(game_state.username)
                        game_state.input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    game_state.input_text = game_state.input_text[:-1]
                else:
                    if len(game_state.input_text) < 20 and event.unicode.isalnum():
                        game_state.input_text += event.unicode

        draw_username_input(game_state)
        clock.tick(30)

    # Show welcome screen with previous score if available
    waiting = True
    load_saved = False

    show_welcome_screen(game_state, previous_score)

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    game_state.reset()
                elif event.key == pygame.K_l:
                    if game_state.user_id:
                        saved_state = get_saved_state(game_state.user_id)
                        if saved_state:
                            game_state.deserialize_state(saved_state)
                            load_saved = True
                            waiting = False

    # Main game loop
    running = True
    while running:
        if game_state.game_over:
            show_game_over_screen(game_state)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        game_state.reset()
                        game_state.game_over = False

        elif game_state.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_state.paused = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            draw_game(game_state)
            clock.tick(5)  # Slow tick rate when paused

        else:
            clock.tick(game_state.speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_state.paused = True
                        save_game_state(game_state.user_id, game_state)
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            # Handle key presses for snake direction
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and game_state.direction != (0, 1):
                game_state.direction = (0, -1)
            elif keys[pygame.K_DOWN] and game_state.direction != (0, -1):
                game_state.direction = (0, 1)
            elif keys[pygame.K_LEFT] and game_state.direction != (1, 0):
                game_state.direction = (-1, 0)
            elif keys[pygame.K_RIGHT] and game_state.direction != (-1, 0):
                game_state.direction = (1, 0)

            # Move snake
            new_head = (game_state.snake[0][0] + game_state.direction[0],
                        game_state.snake[0][1] + game_state.direction[1])

            # Check for collisions
            if (new_head in game_state.walls or
                    new_head in game_state.snake):
                game_state.game_over = True
                save_game_state(game_state.user_id, game_state)

            # Add new head
            game_state.snake.insert(0, new_head)

            # Check for food collision
            if new_head == game_state.food:
                game_state.score += game_state.food_weight
                game_state.food = game_state.get_food_position()
                game_state.food_weight = random.randint(1, 3)
                game_state.food_timer = game_state.FOOD_LIFESPAN

                # Level up every 5 points
                if game_state.score // 5 + 1 > game_state.level:
                    game_state.level += 1
                    game_state.speed += 2
                    game_state.generate_walls()
            else:
                # Remove tail if no food eaten
                game_state.snake.pop()

            # Food timer
            game_state.food_timer -= 1
            if game_state.food_timer <= 0:
                game_state.food = game_state.get_food_position()
                game_state.food_weight = random.randint(1, 3)
                game_state.food_timer = game_state.FOOD_LIFESPAN

            draw_game(game_state)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()