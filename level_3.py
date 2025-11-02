import pygame
import sys
import random
import os

def hard_level(music_vol, sfx_vol): 
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
    HOVER = (120, 120, 255)

    # --- Завантаження фону ---
    try:
        background_image = pygame.image.load(os.path.join('image', 'background.png')).convert()
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    except Exception:
        background_image = None

    # --- Завантаження кнопки “Назад” ---
    try:
        arrow_image = pygame.image.load(os.path.join('image', 'back_arrow.png')).convert_alpha()
        arrow_image = pygame.transform.scale(arrow_image, (50, 50))
    except Exception:
        arrow_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.polygon(arrow_image, WHITE, [(40, 5), (10, 25), (40, 45)])

    button_rect = pygame.Rect(30, 30, 60, 60)

    # --- Завантаження літака ---
    try:
        player_image = pygame.image.load(os.path.join('image', 'player_ship.png')).convert_alpha()
        player_image = pygame.transform.scale(player_image, (80, 100))
    except Exception:
        player_image = pygame.Surface((80, 100), pygame.SRCALPHA)
        pygame.draw.polygon(player_image, BLUE, [(40, 0), (0, 100), (80, 100)])

    # --- Завантаження астероїда ---
    try:
        asteroid_image = pygame.image.load(os.path.join('image', 'asteroid.png')).convert_alpha()
        asteroid_image = pygame.transform.scale(asteroid_image, (80, 80))
    except Exception:
        asteroid_image = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(asteroid_image, (100, 100, 100), (40, 40), 40)

    # --- Завантаження боса ---
    try:
        boss_image = pygame.image.load(os.path.join('image', 'boss.png')).convert_alpha()
        boss_image = pygame.transform.scale(boss_image, (300, 200))
    except Exception:
        boss_image = pygame.Surface((300, 200), pygame.SRCALPHA)
        pygame.draw.rect(boss_image, (180, 50, 50), boss_image.get_rect(), border_radius=12)

    # --- Завантаження звуків ---
    try:
        shoot_sound = pygame.mixer.Sound(os.path.join('music', 'shoot.wav'))
        shoot_sound.set_volume(sfx_vol)
    except Exception:
        shoot_sound = None

    try:
        hit_sound = pygame.mixer.Sound(os.path.join('music', 'hit.mp3'))
        hit_sound.set_volume(sfx_vol)
    except Exception:
        hit_sound = None

    try:
        win_sound = pygame.mixer.Sound(os.path.join('music', 'win.mp3'))
        win_sound.set_volume(sfx_vol)
    except Exception:
        win_sound = None

    try:
        lose_sound = pygame.mixer.Sound(os.path.join('music', 'lose.wav'))
        lose_sound.set_volume(sfx_vol)
    except Exception:
        lose_sound = None

    try:
        boss_hit_sound = pygame.mixer.Sound(os.path.join('music', 'boss_hit.wav'))
        boss_hit_sound.set_volume(sfx_vol)
    except Exception:
        boss_hit_sound = None

    try:
        pygame.mixer.music.load(os.path.join('music', 'engine_loop.wav')) 
        pygame.mixer.music.set_volume(music_vol)
    except Exception:
        print("Warning: 'music/engine_loop.wav' not found.")

    # --- Гравець ---
    player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 150, 80, 100)
    player_speed = 10        # 🚀 Швидкість гравця збільшена
    lasers = []
    laser_speed = -14        # швидші лазери

    # --- Астероїди ---
    asteroids = []
    asteroid_speed = 7      # 💥 Швидші астероїди
    for _ in range(12):      # трохи більше одночасно
        x = random.randint(100, WIDTH - 100)
        y = random.randint(-1200, -50)
        rect = asteroid_image.get_rect(center=(x, y))
        asteroids.append(rect)

    # --- Бос (поки невидимий) ---
    boss = None
    boss_health = 0
    boss_speed = 2
    boss_dir = 1
    boss_shots = []
    boss_shot_speed = 6
    boss_last_shot = 0
    boss_shot_interval = 1200  # мс - можна робити випадковим

    # --- Прогрес ---
    score = 0
    ASTEROIDS_TO_WIN = 50  
    game_over = False
    victory = False
    level_passed = False
    boss_spawned = False

    # --- Текст ---
    def draw_text(text, size, color, x, y):
        font_t = pygame.font.SysFont("timesnewroman", size, bold=True)
        text_surf = font_t.render(text, True, color)
        rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, rect)

    def draw_button(text, x, y, width, height):
        mouse = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, width, height)
        color = DARK_GREY
        if rect.collidepoint(mouse):
            color = HOVER
        pygame.draw.rect(screen, color, rect, border_radius=12)
        draw_text(text, 32, WHITE, x + width // 2, y + height // 2)
        return rect

    def reset_game():
        nonlocal asteroids, lasers, score, game_over, victory, player
        nonlocal boss, boss_health, boss_spawned, boss_shots
        lasers = []
        score = 0
        game_over = False
        victory = False
        boss = None
        boss_health = 0
        boss_spawned = False
        boss_shots = []
        asteroids = []
        for _ in range(12):
            x = random.randint(100, WIDTH - 100)
            y = random.randint(-1200, -50)
            rect = asteroid_image.get_rect(center=(x, y))
            asteroids.append(rect)
        player.centerx = WIDTH // 2
        pygame.mixer.music.play(loops=-1)

    pygame.mixer.music.play(loops=-1)
    
    running = True
    while running:
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill((10, 10, 30))
        
        draw_text("Третій рівень", 28, WHITE, WIDTH // 2, 30)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # --- Події ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE and not game_over and not victory:
                    # постріл гравця
                    lasers.append(pygame.Rect(player.centerx - 3, player.top, 6, 20))
                    if shoot_sound:
                        shoot_sound.play()

        # --- Кнопка Назад ---
        if button_rect.collidepoint(mouse_pos):
            hover_arrow = pygame.transform.scale(arrow_image, (55, 55))
            rect = hover_arrow.get_rect(center=button_rect.center)
            screen.blit(hover_arrow, rect)
            if mouse_click:
                running = False
        else:
            rect = arrow_image.get_rect(center=button_rect.center)
            screen.blit(arrow_image, rect)

        # --- Ігрова логіка ---
        if not game_over and not victory:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= player_speed
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.x += player_speed

            # рух лазерів гравця
            for laser in lasers[:]:
                laser.y += laser_speed
                if laser.bottom < 0:
                    lasers.remove(laser)

            # Якщо бос з'явився — астероїди зупиняємо (або видалимо)
            if boss_spawned:
                asteroids = []

            # рух астероїдів
            for asteroid in asteroids[:]:
                asteroid.y += asteroid_speed
                if asteroid.top > HEIGHT:
                    # астероїд пройшов — респавнимо
                    asteroids.remove(asteroid)
                    x = random.randint(50, WIDTH - 100)
                    y = random.randint(-800, -50)
                    rect = asteroid_image.get_rect(center=(x, y))
                    asteroids.append(rect)
                    continue
                # астероїд вдаряє гравця
                if asteroid.colliderect(player):
                    game_over = True
                    pygame.mixer.music.stop()
                    if lose_sound:
                        lose_sound.play()
                # перевірка попадання лазерів в астероїди
                for laser in lasers[:]:
                    if asteroid.colliderect(laser):
                        try:
                            lasers.remove(laser)
                        except ValueError:
                            pass
                        try:
                            asteroids.remove(asteroid)
                        except ValueError:
                            pass
                        score += 1
                        if hit_sound:
                            hit_sound.play()
                        # респавн астероїда (тільки якщо бос ще не викликаний)
                        if not boss_spawned:
                            x = random.randint(50, WIDTH - 100)
                            y = random.randint(-1200, -50)
                            rect = asteroid_image.get_rect(center=(x, y))
                            asteroids.append(rect)
                        break

            # Коли досягли потрібної кількості — НЕ одразу перемога,
            # а викликаємо боса: очищаємо астероїди і з'являється бос
            if score >= ASTEROIDS_TO_WIN and not boss_spawned:
                boss_spawned = True
                # Очистити астероїди
                asteroids = []
                # Створити боса
                boss = boss_image.get_rect(center=(WIDTH // 2, -150))
                boss_health = 60  # HP боса (регулюй)
                boss_shots = []
                boss_last_shot = pygame.time.get_ticks()
                pygame.mixer.music.stop()
                # (за бажанням) зіграти окрему мелодію або ефект
                # наприклад, win_sound поки не граємо — гра триває
                # трохи "підскоку" боса
                # нічого більше тут не робимо — логіка появи нижче

            # Бос логіка (рух та стрільба)
            if boss_spawned and boss is not None:
                # Під'їзд боса зверху вниз до позиції
                if boss.top < 120:
                    boss.y += 2
                else:
                    # рух по горизонталі
                    boss.x += boss_dir * boss_speed
                    if boss.left < 50 or boss.right > WIDTH - 50:
                        boss_dir *= -1

                # бос стріляє з інтервалом
                now = pygame.time.get_ticks()
                if now - boss_last_shot > boss_shot_interval:
                    boss_last_shot = now
                    # створити кілька снарядів або один
                    bx = boss.centerx
                    by = boss.bottom
                    # центральний снаряд
                    boss_shots.append(pygame.Rect(bx - 6, by, 12, 18))
                    # бокові снаряди
                    boss_shots.append(pygame.Rect(bx - 80, by + 20, 10, 16))
                    boss_shots.append(pygame.Rect(bx + 64, by + 20, 10, 16))
                    # варіація інтервалу
                    boss_shot_interval = random.randint(700, 1400)

                # рух снарядів боса
                for bshot in boss_shots[:]:
                    bshot.y += boss_shot_speed
                    # снаряд влучив в гравця?
                    if bshot.colliderect(player):
                        game_over = True
                        pygame.mixer.music.stop()
                        if lose_sound:
                            lose_sound.play()
                    if bshot.top > HEIGHT:
                        try:
                            boss_shots.remove(bshot)
                        except ValueError:
                            pass

                # перевірка попадання лазерів в боса
                for laser in lasers[:]:
                    if boss.colliderect(laser):
                        try:
                            lasers.remove(laser)
                        except ValueError:
                            pass
                        boss_health -= 1
                        if boss_hit_sound:
                            boss_hit_sound.play()
                        # відштовхування або анімація можна додати тут
                        if boss_health <= 0:
                            victory = True
                            pygame.mixer.music.stop()
                            if win_sound:
                                win_sound.play()
                            # очистити снаряди боса
                            boss_shots = []
                            break

            # Перевірка колізії гравець <-> снаряд боса вже вище
            # Перевірка колізії гравець <-> астероїд вже вище

        # --- Малювання ---
        if not game_over and not victory:
            screen.blit(player_image, player)
            for laser in lasers:
                pygame.draw.rect(screen, YELLOW, laser)
            for asteroid in asteroids:
                screen.blit(asteroid_image, asteroid)

            # малюємо боса та його HP, якщо з'явився
            if boss_spawned and boss is not None:
                screen.blit(boss_image, boss)
                # HP bar під боссом
                hp_w = 220
                hp_h = 18
                hp_x = boss.centerx - hp_w // 2
                hp_y = boss.top - 26
                pygame.draw.rect(screen, DARK_GREY, (hp_x, hp_y, hp_w, hp_h), border_radius=8)
                hp_fill = max(0, int((boss_health / 60) * hp_w))
                pygame.draw.rect(screen, RED, (hp_x, hp_y, hp_fill, hp_h), border_radius=8)
                pygame.draw.rect(screen, WHITE, (hp_x, hp_y, hp_w, hp_h), 2, border_radius=8)

                # малюємо снаряди боса
                for bshot in boss_shots:
                    pygame.draw.rect(screen, (255, 120, 0), bshot)

            # прогрес-бар
            progress_bar_width = 400
            progress_bar_height = 25
            progress_bar_x = (WIDTH - progress_bar_width) // 2
            progress_bar_y = 65
            pygame.draw.rect(screen, DARK_GREY, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
            current_progress = (score / ASTEROIDS_TO_WIN) * progress_bar_width
            pygame.draw.rect(screen, GREEN, (progress_bar_x, progress_bar_y, current_progress, progress_bar_height))
            pygame.draw.rect(screen, WHITE, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)
            draw_text(f"Прогрес: {score}/{ASTEROIDS_TO_WIN}", 22, WHITE, WIDTH // 2, progress_bar_y + 13)

        else:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            if game_over:
                draw_text("Ти програв!", 60, RED, WIDTH // 2, HEIGHT // 2 - 60)
            elif victory:
                draw_text("РІВЕНЬ ПРОЙДЕНО!", 60, GREEN, WIDTH // 2, HEIGHT // 2 - 60)

            restart_rect = draw_button("🔁 Почати знову", WIDTH // 2 - 150, HEIGHT // 2 + 30, 300, 60)
            menu_rect = draw_button("🏠 Вийти в меню", WIDTH // 2 - 150, HEIGHT // 2 + 110, 300, 60)

            if mouse_click:
                if restart_rect.collidepoint(mouse_pos):
                    reset_game()
                if menu_rect.collidepoint(mouse_pos):
                    if victory:
                        level_passed = True
                    running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    return level_passed

