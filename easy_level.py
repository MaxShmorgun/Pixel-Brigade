import pygame
import sys
import random
import os

def easy_level():
    # --- Ініціалізація ---
    try:
        screen = pygame.display.get_surface()
        WIDTH, HEIGHT = screen.get_size()
    except:
        WIDTH, HEIGHT = 1200, 800
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixel Brigade")

    clock = pygame.time.Clock()

    # --- Кольори ---
    WHITE = (255, 255, 255)
    RED = (255, 50, 50)
    GREEN = (0, 255, 100)
    BLUE = (0, 150, 255)
    YELLOW = (255, 255, 0)
    DARK_GREY = (50, 50, 50)

    # --- Завантаження фону ---
    try:
        background_image = pygame.image.load(os.path.join('image', 'background.png')).convert()
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Помилка: не знайдено background.png. {e}")
        background_image = None

    # --- Завантаження кнопки "Назад" ---
    try:
        arrow_image = pygame.image.load(os.path.join('image', 'back_arrow.png')).convert_alpha()
        arrow_image = pygame.transform.scale(arrow_image, (50, 50))
    except pygame.error as e:
        print(f"Помилка: не знайдено back_arrow.png. {e}")
        arrow_image = pygame.Surface((50, 50), pygame.SRCALPHA)

    # --- Завантаження літака ---
    try:
        player_image = pygame.image.load(os.path.join('image', 'player_ship.png')).convert_alpha()
        player_image = pygame.transform.scale(player_image, (80, 100))
    except pygame.error as e:
        print(f"Помилка: не знайдено ship.png. {e}")
        player_image = pygame.Surface((80, 100), pygame.SRCALPHA)
        pygame.draw.polygon(player_image, BLUE, [(40, 0), (0, 100), (80, 100)])

    # --- Завантаження астероїдів ---
    try:
        asteroid_image = pygame.image.load(os.path.join('image', 'asteroid.png')).convert_alpha()
        asteroid_image = pygame.transform.scale(asteroid_image, (80, 80))
    except pygame.error as e:
        print(f"Помилка: не знайдено asteroid.png. {e}")
        asteroid_image = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(asteroid_image, (100, 100, 100), (40, 40), 40)

    # --- Налаштування гравця ---
    player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 150, 80, 100)
    player_speed = 6
    lasers = []
    laser_speed = -10

    # --- Астероїди ---
    asteroids = []
    asteroid_speed = 3
    for i in range(8):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(-800, -50)
        rect = asteroid_image.get_rect(center=(x, y))
        asteroids.append(rect)

    # --- Прогрес ---
    score = 0
    ASTEROIDS_TO_WIN = 25
    game_over = False
    victory = False
    game_result = False

    button_rect = pygame.Rect(30, 30, 60, 60)

    progress_bar_width = 400
    progress_bar_height = 25
    progress_bar_x = (WIDTH - progress_bar_width) // 2
    progress_bar_y = 65

    def draw_text(text, size, color, x, y):
        font_t = pygame.font.SysFont("timesnewroman", size, bold=True)
        text_surf = font_t.render(text, True, color)
        rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, rect)

    def reset_game():
        nonlocal asteroids, lasers, score, game_over, victory, player
        lasers = []
        score = 0
        game_over = False
        victory = False
        asteroids = []
        for i in range(8):
            x = random.randint(100, WIDTH - 100)
            y = random.randint(-800, -50)
            rect = asteroid_image.get_rect(center=(x, y))
            asteroids.append(rect)
        player.centerx = WIDTH // 2

    running = True
    while running:
        # --- Фон ---
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill((10, 10, 30))

        draw_text("Довгий рівень", 28, WHITE, WIDTH // 2, 30)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE and not game_over and not victory:
                    lasers.append(pygame.Rect(player.centerx - 3, player.top, 6, 20))
                if event.key == pygame.K_RETURN:
                    if game_over:
                        reset_game()
                    elif victory:
                        game_result = True
                        running = False

        # --- Кнопка в меню ---
        if button_rect.collidepoint(mouse_pos) and mouse_click:
            running = False

        # Малювання стрілки
        if button_rect.collidepoint(mouse_pos):
            hover_arrow = pygame.transform.scale(arrow_image, (55, 55))
            rect = hover_arrow.get_rect(center=button_rect.center)
            screen.blit(hover_arrow, rect)
        else:
            rect = arrow_image.get_rect(center=button_rect.center)
            screen.blit(arrow_image, rect)

        # --- Керування ---
        if not game_over and not victory:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= player_speed
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.x += player_speed

        # --- Рух лазерів ---
        for laser in lasers[:]:
            laser.y += laser_speed
            if laser.bottom < 0:
                lasers.remove(laser)

        # --- Рух астероїдів ---
        for asteroid in asteroids[:]:
            asteroid.y += asteroid_speed
            if asteroid.top > HEIGHT:
                asteroids.remove(asteroid)
                x = random.randint(50, WIDTH - 100)
                y = random.randint(-600, -50)
                rect = asteroid_image.get_rect(center=(x, y))
                asteroids.append(rect)
                continue
            if asteroid.colliderect(player):
                game_over = True
            for laser in lasers[:]:
                if asteroid.colliderect(laser):
                    lasers.remove(laser)
                    asteroids.remove(asteroid)
                    score += 1
                    x = random.randint(50, WIDTH - 100)
                    y = random.randint(-800, -50)
                    rect = asteroid_image.get_rect(center=(x, y))
                    asteroids.append(rect)
                    break

        # --- Перевірка перемоги ---
        if score >= ASTEROIDS_TO_WIN and not victory:
            victory = True

        # --- Малювання ---
        if not game_over and not victory:
            screen.blit(player_image, player)
            for laser in lasers:
                pygame.draw.rect(screen, YELLOW, laser)
            for asteroid in asteroids:
                screen.blit(asteroid_image, asteroid)

            # Прогрес-бар
            pygame.draw.rect(screen, DARK_GREY, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
            current_progress = (score / ASTEROIDS_TO_WIN) * progress_bar_width
            pygame.draw.rect(screen, GREEN, (progress_bar_x, progress_bar_y, current_progress, progress_bar_height))
            pygame.draw.rect(screen, WHITE, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)
            draw_text(f"Прогрес: {score}/{ASTEROIDS_TO_WIN}", 22, WHITE, WIDTH // 2, progress_bar_y + 13)

        elif game_over:
            draw_text("Ти програв!", 60, RED, WIDTH // 2, HEIGHT // 2)
            draw_text("Натисни ENTER, щоб спробувати ще раз", 28, WHITE, WIDTH // 2, HEIGHT // 2 + 80)
        elif victory:
            draw_text("РІВЕНЬ ПРОЙДЕНО!", 60, GREEN, WIDTH // 2, HEIGHT // 2)
            draw_text("Натисни ENTER, щоб вийти в меню", 28, WHITE, WIDTH // 2, HEIGHT // 2 + 80)

        pygame.display.flip()
        clock.tick(60)

    return game_result