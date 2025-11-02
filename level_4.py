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
    def load_sound(name):
        try:
            s = pygame.mixer.Sound(os.path.join('music', name))
            s.set_volume(sfx_vol)
            return s
        except Exception:
            return None

    shoot_sound = load_sound('shoot.wav')
    hit_sound = load_sound('hit.mp3')
    win_sound = load_sound('win.mp3')
    lose_sound = load_sound('lose.wav')
    boss_hit_sound = load_sound('boss_hit.wav')

    try:
        pygame.mixer.music.load(os.path.join('music', 'engine_loop.wav')) 
        pygame.mixer.music.set_volume(music_vol)
    except Exception:
        print("Warning: 'music/engine_loop.wav' not found.")

    # --- Гравець ---
    player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 150, 80, 100)
    player_speed = 10
    lasers = []
    laser_speed = -14

    # --- Астероїди ---
    asteroids = []
    asteroid_speed = 7
    for _ in range(12):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(-1200, -50)
        asteroids.append(asteroid_image.get_rect(center=(x, y)))

    # --- Бос ---
    boss = None
    boss_health = 0
    boss_speed = 2
    boss_dir = 1
    boss_shots = []
    boss_shot_speed = 7
    boss_last_shot = 0
    boss_shot_interval = 900
    boss_asteroids = []
    boss_asteroid_timer = 0
    boss_asteroid_interval = 2500  # інтервал кидання астероїдів

    # --- Прогрес ---
    score = 0
    ASTEROIDS_TO_WIN = 10  # 🟩 тепер 75 для перемоги
    game_over = False
    victory = False
    level_passed = False
    boss_spawned = False

    # --- Текст ---
    def draw_text(text, size, color, x, y):
        font_t = pygame.font.SysFont("timesnewroman", size, bold=True)
        surf = font_t.render(text, True, color)
        rect = surf.get_rect(center=(x, y))
        screen.blit(surf, rect)

    def draw_button(text, x, y, w, h):
        mouse = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, w, h)
        color = HOVER if rect.collidepoint(mouse) else DARK_GREY
        pygame.draw.rect(screen, color, rect, border_radius=12)
        draw_text(text, 32, WHITE, x + w // 2, y + h // 2)
        return rect

    def reset_game():
        nonlocal asteroids, lasers, score, game_over, victory, player
        nonlocal boss, boss_health, boss_spawned, boss_shots, boss_asteroids
        lasers.clear()
        asteroids.clear()
        score = 0
        game_over = False
        victory = False
        boss = None
        boss_health = 0
        boss_spawned = False
        boss_shots.clear()
        boss_asteroids.clear()
        for _ in range(12):
            x = random.randint(100, WIDTH - 100)
            y = random.randint(-1200, -50)
            asteroids.append(asteroid_image.get_rect(center=(x, y)))
        player.centerx = WIDTH // 2
        pygame.mixer.music.play(loops=-1)

    pygame.mixer.music.play(loops=-1)

    running = True
    while running:
        screen.blit(background_image, (0, 0)) if background_image else screen.fill((10, 10, 30))
        draw_text("Третій рівень", 28, WHITE, WIDTH // 2, 30)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                if e.key == pygame.K_SPACE and not game_over and not victory:
                    lasers.append(pygame.Rect(player.centerx - 3, player.top, 6, 20))
                    if shoot_sound: shoot_sound.play()

        # --- Кнопка Назад ---
        rect = arrow_image.get_rect(center=button_rect.center)
        screen.blit(pygame.transform.scale(arrow_image, (55, 55)) if button_rect.collidepoint(mouse) else arrow_image, rect)
        if button_rect.collidepoint(mouse) and click:
            running = False

        if not game_over and not victory:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.left > 0: player.x -= player_speed
            if keys[pygame.K_RIGHT] and player.right < WIDTH: player.x += player_speed

            # рух лазерів
            for l in lasers[:]:
                l.y += laser_speed
                if l.bottom < 0: lasers.remove(l)

            # рух астероїдів
            for a in asteroids[:]:
                a.y += asteroid_speed
                if a.top > HEIGHT:
                    asteroids.remove(a)
                    x = random.randint(50, WIDTH - 100)
                    y = random.randint(-800, -50)
                    asteroids.append(asteroid_image.get_rect(center=(x, y)))
                    continue
                if a.colliderect(player):
                    game_over = True
                    pygame.mixer.music.stop()
                    if lose_sound: lose_sound.play()
                for l in lasers[:]:
                    if a.colliderect(l):
                        lasers.remove(l)
                        asteroids.remove(a)
                        score += 1
                        if hit_sound: hit_sound.play()
                        if not boss_spawned:
                            x = random.randint(50, WIDTH - 100)
                            y = random.randint(-1200, -50)
                            asteroids.append(asteroid_image.get_rect(center=(x, y)))
                        break

            # --- Виклик боса ---
            if score >= ASTEROIDS_TO_WIN and not boss_spawned:
                boss_spawned = True
                asteroids.clear()
                boss = boss_image.get_rect(center=(WIDTH // 2, -150))
                boss_health = 80
                boss_last_shot = pygame.time.get_ticks()
                pygame.mixer.music.stop()

            # --- Логіка боса ---
            if boss_spawned and boss:
                if boss.top < 120: boss.y += 2
                else:
                    boss.x += boss_dir * boss_speed
                    if boss.left < 50 or boss.right > WIDTH - 50: boss_dir *= -1

                now = pygame.time.get_ticks()

                # 🧨 частіша стрільба — багато пуль одночасно
                if now - boss_last_shot > boss_shot_interval:
                    boss_last_shot = now
                    bx, by = boss.centerx, boss.bottom
                    for offset in [-80, -40, 0, 40, 80]:
                        boss_shots.append(pygame.Rect(bx + offset, by, 10, 20))
                    boss_shot_interval = random.randint(500, 900)

                # 🌑 бос кидає астероїди згори
                if now - boss_asteroid_timer > boss_asteroid_interval:
                    boss_asteroid_timer = now
                    for _ in range(random.randint(2, 4)):
                        x = random.randint(100, WIDTH - 100)
                        a = asteroid_image.get_rect(center=(x, boss.bottom + 50))
                        boss_asteroids.append(a)

                # рух снарядів
                for b in boss_shots[:]:
                    b.y += boss_shot_speed
                    if b.top > HEIGHT:
                        boss_shots.remove(b)
                    elif b.colliderect(player):
                        game_over = True
                        pygame.mixer.music.stop()
                        if lose_sound: lose_sound.play()

                # рух бос-астероїдів
                for ba in boss_asteroids[:]:
                    ba.y += 8
                    if ba.top > HEIGHT: boss_asteroids.remove(ba)
                    if ba.colliderect(player):
                        game_over = True
                        pygame.mixer.music.stop()
                        if lose_sound: lose_sound.play()

                # попадання по босу
                for l in lasers[:]:
                    if boss.colliderect(l):
                        lasers.remove(l)
                        boss_health -= 1
                        if boss_hit_sound: boss_hit_sound.play()
                        if boss_health <= 0:
                            victory = True
                            pygame.mixer.music.stop()
                            if win_sound: win_sound.play()
                            boss_shots.clear()
                            boss_asteroids.clear()
                            break

        # --- Малювання ---
        if not game_over and not victory:
            screen.blit(player_image, player)
            for l in lasers: pygame.draw.rect(screen, YELLOW, l)
            for a in asteroids: screen.blit(asteroid_image, a)
            if boss_spawned and boss:
                screen.blit(boss_image, boss)
                for b in boss_shots: pygame.draw.rect(screen, (255, 120, 0), b)
                for ba in boss_asteroids: screen.blit(asteroid_image, ba)
                # HP Bar
                hp_w, hp_h = 220, 18
                hp_x, hp_y = boss.centerx - hp_w // 2, boss.top - 26
                pygame.draw.rect(screen, DARK_GREY, (hp_x, hp_y, hp_w, hp_h), border_radius=8)
                fill = max(0, int((boss_health / 80) * hp_w))
                pygame.draw.rect(screen, RED, (hp_x, hp_y, fill, hp_h), border_radius=8)
                pygame.draw.rect(screen, WHITE, (hp_x, hp_y, hp_w, hp_h), 2, border_radius=8)

            # прогрес-бар
            bar_w, bar_h = 400, 25
            bar_x, bar_y = (WIDTH - bar_w)//2, 65
            pygame.draw.rect(screen, DARK_GREY, (bar_x, bar_y, bar_w, bar_h))
            cur = (score / ASTEROIDS_TO_WIN) * bar_w
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, cur, bar_h))
            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 2)
            draw_text(f"Прогрес: {score}/{ASTEROIDS_TO_WIN}", 22, WHITE, WIDTH//2, bar_y + 13)
        else:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            if game_over:
                draw_text("Ти програв!", 60, RED, WIDTH//2, HEIGHT//2 - 60)
            else:
                draw_text("РІВЕНЬ ПРОЙДЕНО!", 60, GREEN, WIDTH//2, HEIGHT//2 - 60)

            restart = draw_button("🔁 Почати знову", WIDTH//2 - 150, HEIGHT//2 + 30, 300, 60)
            menu = draw_button("🏠 Вийти в меню", WIDTH//2 - 150, HEIGHT//2 + 110, 300, 60)
            if click:
                if restart.collidepoint(mouse): reset_game()
                if menu.collidepoint(mouse):
                    if victory: level_passed = True
                    running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    return level_passed
