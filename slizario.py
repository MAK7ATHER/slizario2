
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1000, 700
CELL = 20
FPS = 12

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slizario")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 25, bold=True)
BIG_FONT = pygame.font.SysFont("arial", 55, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 18)

WHITE = (245, 245, 255)
PURPLE = (145, 70, 255)
CYAN = (40, 230, 255)
PINK = (255, 70, 170)
ORANGE = (255, 170, 50)

state = "menu"
score = 0
best_score = 0

snake = []
direction = (1, 0)
next_direction = (1, 0)
food = (30, 20)


def draw_text(text, font, color, x, y, center=True):
    image = font.render(text, True, color)
    rect = image.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(image, rect)


def draw_background():
    screen.fill((12, 10, 30))

    for i in range(45):
        x = (i * 137) % WIDTH
        y = (i * 83) % HEIGHT
        pygame.draw.circle(
            screen, (35, 25, 75), (x, y), 2
        )

    pygame.draw.rect(
        screen,
        (40, 30, 75),
        (40, 40, WIDTH - 80, HEIGHT - 80),
        2,
        border_radius=20
    )


def draw_button(text, rect, mouse):
    color = CYAN if rect.collidepoint(mouse) else PURPLE

    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=12)

    draw_text(text, FONT, WHITE, rect.centerx, rect.centery)


def spawn_food():
    while True:
        pos = (
            random.randint(3, WIDTH // CELL - 4),
            random.randint(3, HEIGHT // CELL - 4)
        )
        if pos not in snake:
            return pos


def reset_game():
    global snake, direction, next_direction
    global food, score, state

    snake = [(25, 17), (24, 17), (23, 17)]
    direction = (1, 0)
    next_direction = (1, 0)
    score = 0
    food = spawn_food()
    state = "playing"


def draw_snake():
    for i, (x, y) in enumerate(snake):
        rect = pygame.Rect(
            x * CELL, y * CELL, CELL - 2, CELL - 2
        )

        if i == 0:
            color = CYAN
        else:
            color = (
                max(30, 120 - i % 50),
                max(50, 220 - i % 40),
                255
            )

        pygame.draw.rect(
            screen, color, rect, border_radius=6
        )

        if i == 0:
            pygame.draw.circle(
                screen, (10, 10, 25),
                (x * CELL + 6, y * CELL + 6), 2
            )
            pygame.draw.circle(
                screen, (10, 10, 25),
                (x * CELL + 14, y * CELL + 6), 2
            )


def draw_food():
    x, y = food
    center = (
        x * CELL + CELL // 2,
        y * CELL + CELL // 2
    )

    pygame.draw.circle(screen, ORANGE, center, CELL // 2)
    pygame.draw.circle(screen, WHITE, center, 4)


def draw_hud():
    draw_text(f"Рахунок: {score}", FONT, WHITE, 130, 65)
    draw_text(f"Рекорд: {best_score}", SMALL_FONT, CYAN, 130, 95)


def end_game():
    global state, best_score

    state = "gameover"
    best_score = max(best_score, score)


def move_snake():
    global direction, next_direction, food, score

    direction = next_direction

    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    if (
        new_head[0] < 2
        or new_head[0] >= WIDTH // CELL - 2
        or new_head[1] < 2
        or new_head[1] >= HEIGHT // CELL - 2
    ):
        end_game()
        return

    eating = new_head == food

    # Не дозволяємо врізатися в тіло.
    # Якщо змійка не їсть, остання клітинка звільняється.
    body = snake if eating else snake[:-1]

    if new_head in body:
        end_game()
        return

    snake.insert(0, new_head)

    if eating:
        score += 1
        food = spawn_food()
    else:
        snake.pop()


def handle_key(key):
    global next_direction, state

    if key == pygame.K_UP and direction != (0, 1):
        next_direction = (0, -1)

    elif key == pygame.K_DOWN and direction != (0, -1):
        next_direction = (0, 1)

    elif key == pygame.K_LEFT and direction != (1, 0):
        next_direction = (-1, 0)

    elif key == pygame.K_RIGHT and direction != (-1, 0):
        next_direction = (1, 0)

    elif key == pygame.K_ESCAPE:
        state = "menu"


def draw_menu():
    draw_background()
    mouse = pygame.mouse.get_pos()

    draw_text("SLIZARIO", BIG_FONT, CYAN, WIDTH // 2, 180)
    draw_text(
        "NEON SNAKE GAME", SMALL_FONT, PINK,
        WIDTH // 2, 225
    )

    play_rect = pygame.Rect(
        WIDTH // 2 - 130, 320, 260, 60
    )
    quit_rect = pygame.Rect(
        WIDTH // 2 - 130, 410, 260, 60
    )

    draw_button("ГРАТИ", play_rect, mouse)
    draw_button("ВИХІД", quit_rect, mouse)

    return play_rect, quit_rect


running = True

while running:
    clock.tick(FPS)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if state == "playing":
                handle_key(event.key)

            elif event.key == pygame.K_ESCAPE:
                state = "menu"

            elif state == "gameover":
                if event.key == pygame.K_RETURN:
                    reset_game()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if state == "menu":
                    play_rect, quit_rect = draw_menu()

                    if play_rect.collidepoint(event.pos):
                        reset_game()

                    elif quit_rect.collidepoint(event.pos):
                        running = False

                elif state == "gameover":
                    if event.button == 1:
                        reset_game()

    if state == "menu":
        draw_menu()

    elif state == "playing":
        draw_background()
        move_snake()

        if state == "playing":
            draw_food()
            draw_snake()
            draw_hud()

        else:
            draw_food()
            draw_snake()
            draw_hud()

    elif state == "gameover":
        draw_background()
        draw_food()
        draw_snake()
        draw_hud()

        draw_text(
            "GAME OVER", BIG_FONT, PINK,
            WIDTH // 2, HEIGHT // 2 - 60
        )

        draw_text(
            "Enter — грати знову", FONT, WHITE,
            WIDTH // 2, HEIGHT // 2 + 5
        )

        draw_text(
            "Esc — головне меню", SMALL_FONT, CYAN,
            WIDTH // 2, HEIGHT // 2 + 50
        )

    pygame.display.flip()

pygame.quit()
