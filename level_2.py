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
    except pygame.error:
        background_image = None

    # --- Завантаження кнопки “Назад” ---
    try:
        arrow_image = pygame.image.load(os.path.join('image', 'back_arrow.png')).convert_alpha()
        arrow_image = pygame.transform.scale(arrow_image, (50, 50))
    except pygame.error:
        arrow_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.polygon(arrow_image, WHITE, [(40, 5), (10, 25), (40, 45)])

    button_rect = pygame.Rect(30, 30, 60, 60)

    # --- Завантаження літака ---
    try:
        player_image = pygame.image.load(os.path.join('image', 'player_ship.png')).convert_alpha()
        player_image = pygame.transform.scale(player_image, (80, 100))
    except pygame.error:
        player_image = pygame.Surface((80, 100), pygame.SRCALPHA)
        pygame.draw.polygon(player_image, BLUE, [(40, 0), (0, 100), (80, 100)])

    # --- Завантаження астероїда ---
    try:
        asteroid_image = pygame.image.load(os.path.join('image', 'asteroid.png')).convert_alpha()
        asteroid_image = pygame.transform.scale(asteroid_image, (80, 80))
    except pygame.error:
        asteroid_image = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(asteroid_image, (100, 100, 100), (40, 40), 40)

    # --- Завантаження звуків ---
    try:
        shoot_sound = pygame.mixer.Sound(os.path.join('music', 'shoot.wav'))
        shoot_sound.set_volume(sfx_vol)
    except pygame.error:
        shoot_sound = None

    try:
        hit_sound = pygame.mixer.Sound(os.path.join('music', 'hit.mp3'))
        hit_sound.set_volume(sfx_vol)
    except pygame.error:
        hit_sound = None

    try:
        win_sound = pygame.mixer.Sound(os.path.join('music', 'win.mp3'))
        win_sound.set_volume(sfx_vol)
    except pygame.error:
        win_sound = None

    try:
        lose_sound = pygame.mixer.Sound(os.path.join('music', 'lose.wav'))
        lose_sound.set_volume(sfx_vol)
    except pygame.error:
        lose_sound = None

    try:
        pygame.mixer.music.load(os.path.join('music', 'engine_loop.wav')) 
        pygame.mixer.music.set_volume(music_vol)
    except pygame.error:
        print("Warning: 'music/engine_loop.wav' not found.")

    # --- Гравець ---
    player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 150, 80, 100)
    player_speed = 8        # 🚀 Швидше
    lasers = []
    laser_speed = -10

    # --- Астероїди ---
    asteroids = []
    asteroid_speed = 5      # 💥 Швидші
    for _ in range(10):     # Трохи більше одночасно
        x = random.randint(100, WIDTH - 100)
        y = random.randint(-800, -50)
        rect = asteroid_image.get_rect(center=(x, y))
        asteroids.append(rect)

    # --- Прогрес ---
    score = 0
    ASTEROIDS_TO_WIN = 50   # 🎯 Більше потрібно збити
    game_over = False
    victory = False
    level_passed = False

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
        lasers = []
        score = 0
        game_over = False
        victory = False
        asteroids = []
        for _ in range(10):
            x = random.randint(100, WIDTH - 100)
            y = random.randint(-800, -50)
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
        
        draw_text("Другий рівень", 28, WHITE, WIDTH // 2, 30)
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

            for laser in lasers[:]:
                laser.y += laser_speed
                if laser.bottom < 0:
                    lasers.remove(laser)

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
                    pygame.mixer.music.stop()
                    if lose_sound:
                        lose_sound.play()
                        
                for laser in lasers[:]:
                    if asteroid.colliderect(laser):
                        lasers.remove(laser)
                        asteroids.remove(asteroid)
                        score += 1
                        if hit_sound:
                            hit_sound.play()
                        x = random.randint(50, WIDTH - 100)
                        y = random.randint(-800, -50)
                        rect = asteroid_image.get_rect(center=(x, y))
                        asteroids.append(rect)
                        break

            if score >= ASTEROIDS_TO_WIN:
                victory = True
                pygame.mixer.music.stop()
                if win_sound:
                    win_sound.play()

        # --- Малювання ---
        if not game_over and not victory:
            screen.blit(player_image, player)
            for laser in lasers:
                pygame.draw.rect(screen, YELLOW, laser)
            for asteroid in asteroids:
                screen.blit(asteroid_image, asteroid)

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
if __name__ == "__main__":
    pygame.init()
    hard_level(0.5, 0.5)
    pygame.quit()