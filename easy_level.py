import pygame
import sys
import random

def easy_level():
    # Отримуємо існуючий екран
    try:
        screen = pygame.display.get_surface()
        WIDTH, HEIGHT = screen.get_size()
    except:
        WIDTH, HEIGHT = 1200, 800
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixel Brigade")


    clock = pygame.time.Clock()
    font = pygame.font.SysFont("timesnewroman", 36)

    # --- Кольори ---
    WHITE = (255, 255, 255)
    RED = (255, 50, 50)
    GREEN = (0, 255, 100)
    BLUE = (0, 150, 255)
    YELLOW = (255, 255, 0)
    DARK_GREY = (50, 50, 50)
    BUTTON_COLOR = (80, 80, 200)
    BUTTON_HOVER = (120, 120, 255)

    # --- Налаштування гравця ---
    player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 100, 50, 50)
    player_speed = 6
    lasers = []
    laser_speed = -10

    # --- Налаштування ворогів ---
    enemy_list = []
    enemy_speed = 3
    MAX_ENEMIES_ON_SCREEN = 8

    # --- Налаштування рівня ---
    score = 0
    ENEMIES_TO_WIN = 25
    game_over = False
    victory = False
    
    # Змінна, що зберігає остаточний результат гри
    game_result = False # True = перемога, False = програш/вихід

    # --- Кнопка виходу в меню ---
    button_rect = pygame.Rect(30, 30, 180, 60)

    # --- Прогрес-бар ---
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
        nonlocal enemy_list, lasers, score, game_over, victory, player
        lasers = []
        score = 0
        game_over = False
        victory = False
        enemy_list = []
        player.centerx = WIDTH // 2

    running = True
    while running:
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
                
                # Обробка натискання ENTER після завершення гри
                if event.key == pygame.K_RETURN:
                    if game_over:
                        reset_game()
                    elif victory:
                        # <<< ВИПРАВЛЕНО: Рядок `nonlocal` видалено >>>
                        game_result = True # Встановлюємо результат як True (перемога)
                        running = False    # Виходимо з циклу

        # --- Кнопка "В меню" ---
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER, button_rect, border_radius=10)
            if mouse_click:
                running = False  # Вихід у меню 
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)
        draw_text("В меню", 28, WHITE, button_rect.centerx, button_rect.centery)

        # --- Керування гравцем ---
        keys = pygame.key.get_pressed()
        if not game_over and not victory:
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= player_speed
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.x += player_speed

        # --- Створення нових ворогів ---
        if not game_over and not victory and len(enemy_list) < MAX_ENEMIES_ON_SCREEN:
            x = random.randint(50, WIDTH - 100)
            y = random.randint(-800, -50)
            enemy_list.append(pygame.Rect(x, y, 50, 50))

        # --- Оновлення позицій та колізії ---
        for laser in lasers[:]:
            laser.y += laser_speed
            if laser.bottom < 0:
                lasers.remove(laser)

        for enemy in enemy_list[:]:
            enemy.y += enemy_speed
            if enemy.top > HEIGHT:
                enemy_list.remove(enemy)
                continue
            if enemy.colliderect(player):
                game_over = True 
            for laser in lasers[:]:
                if enemy.colliderect(laser):
                    lasers.remove(laser)
                    enemy_list.remove(enemy)
                    score += 1
                    break

        # --- Перевірка перемоги ---
        if score >= ENEMIES_TO_WIN and not victory:
            victory = True

        # --- Малювання ---
        if not game_over and not victory:
            pygame.draw.rect(screen, BLUE, player)
            for laser in lasers:
                pygame.draw.rect(screen, YELLOW, laser)
            for enemy in enemy_list:
                pygame.draw.rect(screen, RED, enemy)

            # Прогрес-бар
            pygame.draw.rect(screen, DARK_GREY, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
            current_progress = (score / ENEMIES_TO_WIN) * progress_bar_width
            pygame.draw.rect(screen, GREEN, (progress_bar_x, progress_bar_y, current_progress, progress_bar_height))
            pygame.draw.rect(screen, WHITE, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)
            draw_text(f"Прогрес: {score}/{ENEMIES_TO_WIN}", 22, WHITE, WIDTH // 2, progress_bar_y + 13)

        elif game_over:
            draw_text("Ти програв!", 60, RED, WIDTH // 2, HEIGHT // 2)
            draw_text("Натисни ENTER, щоб спробувати ще раз", 28, WHITE, WIDTH // 2, HEIGHT // 2 + 80)
        elif victory:
            draw_text("РІВЕНЬ ПРОЙДЕНО!", 60, GREEN, WIDTH // 2, HEIGHT // 2)
            draw_text("Натисни ENTER, щоб вийти в меню", 28, WHITE, WIDTH // 2, HEIGHT // 2 + 80)

        pygame.display.flip()
        clock.tick(60)
    
    # Повертає True (якщо перемога) або False (якщо програш/вихід)
    return game_result