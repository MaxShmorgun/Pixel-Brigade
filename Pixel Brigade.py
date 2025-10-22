import pygame
import sys
import easy_level
import json 

pygame.init()
pygame.mixer.init()

# --- Збереження ---
SAVE_FILE = "save_data.json"

# --- Екран ---
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Brigade")

# --- Зображення ---
background = pygame.image.load("image/menu_bg.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

settings_icon = pygame.image.load("image/settings.png")
settings_icon = pygame.transform.scale(settings_icon, (50, 50))
settings_rect = settings_icon.get_rect(topright=(WIDTH - 10, 10))

# --- Замок ---
try:
    lock_icon = pygame.image.load("image/lock.png")
    lock_icon = pygame.transform.scale(lock_icon, (100, 100))
except pygame.error:
    lock_icon = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.rect(lock_icon, (255, 0, 0, 200), (0, 0, 100, 100), border_radius=10)

# --- Прев’ю рівнів ---
level_images = {
    "level_1": pygame.image.load("avatar/level_1.png"),
    "level_2": pygame.image.load("avatar/level_2.png"),
    "level_3": pygame.image.load("avatar/level_3.png"),
    "level_4": pygame.image.load("avatar/level_4.png"),
    "level_5": pygame.image.load("avatar/level_5.png"),
    "level_6": pygame.image.load("avatar/level_6.png"),
    "level_7": pygame.image.load("avatar/level_7.png"),
    "level_8": pygame.image.load("avatar/level_8.png"),
    "level_9": pygame.image.load("avatar/level_9.png"),
    "level_10": pygame.image.load("avatar/level_10.png")
}

# --- Шрифти ---
font_title = pygame.font.SysFont("timesnewroman", 80, bold=True)
font_button = pygame.font.SysFont("timesnewroman", 40)
rules_font = pygame.font.SysFont("timesnewroman", 30)

# --- Кольори ---
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
BLUE = (70, 130, 255)
YELLOW = (255, 180, 0)

# --- Аудіо ---
pygame.mixer.music.load("music/menu.mp3")
volume_music = 0.5
pygame.mixer.music.set_volume(volume_music)
pygame.mixer.music.play(-1)

# --- Стан ---
MENU = "menu"
LEVEL_SELECT = "level_select"
RULES = "rules"
SETTINGS = "settings"
state = MENU

slider_dragging = False
show_settings = False

# --- Прогрес ---
DEFAULT_PROGRESS = {
    "level_1": True,
    "level_2": False,
    "level_3": False,
    "level_4": False,
    "level_5": False,
    "level_6": False,
    "level_7": False,
    "level_8": False,
    "level_9": False,
    "level_10": False
}
level_progress = DEFAULT_PROGRESS.copy()

# --- Функції збереження ---
def load_progress():
    global level_progress
    try:
        with open(SAVE_FILE, 'r') as f:
            level_progress = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        level_progress = DEFAULT_PROGRESS.copy()

def save_progress():
    with open(SAVE_FILE, 'w') as f:
        json.dump(level_progress, f, indent=4)

def unlock_next_level(current_key):
    global level_progress
    keys_order = ["level_1", "level_2", "level_3", "level_4", "level_5", "level_6", "level_7", "level_8", "level_9", "level_10"]
    try:
        current_index = keys_order.index(current_key)
        next_index = current_index + 1
        if next_index < len(keys_order):
            next_key = keys_order[next_index]
            if not level_progress[next_key]:
                level_progress[next_key] = True
                save_progress()
    except ValueError:
        pass

# --- Допоміжні ---
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, rect)

def draw_button(text, x, y, width, height):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, width, height)

    color = BLUE if rect.collidepoint(mouse) else GRAY
    pygame.draw.rect(screen, color, rect, border_radius=10)
    draw_text(text, font_button, WHITE, screen, x + width // 2, y + height // 2)

    if rect.collidepoint(mouse) and click[0]:
        pygame.time.wait(150)
        return True
    return False

# --- Меню ---
def main_menu():
    screen.blit(background, (0, 0))
    screen.blit(settings_icon, settings_rect)

    if draw_button("▶ Почати гру", WIDTH // 2 - 130, 380, 260, 60):
        return LEVEL_SELECT
    if draw_button("📜 Правила", WIDTH // 2 - 130, 470, 260, 60):
        return RULES
    if draw_button("❌ Вийти", WIDTH // 2 - 130, 560, 260, 60):
        pygame.quit()
        sys.exit()
    pygame.display.update()
    return MENU

# --- Меню вибору рівня ---
def level_select_menu():
    screen.blit(background, (0, 0))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    draw_text("Вибір рівня", font_title, WHITE, screen, WIDTH // 2, 120)

    levels = [
        {"key": "level_1", "name": "Легкий", "unlocked": level_progress["level_1"]},
        {"key": "level_2", "name": "Середній", "unlocked": level_progress["level_2"]},
        {"key": "level_3", "name": "Важкий", "unlocked": level_progress["level_3"]},
        {"key": "level_4", "name": "Рівень 4", "unlocked": level_progress["level_4"]},
        {"key": "level_5", "name": "Рівень 5", "unlocked": level_progress["level_5"]},
        {"key": "level_6", "name": "Рівень 6", "unlocked": level_progress["level_6"]},
        {"key": "level_7", "name": "Рівень 7", "unlocked": level_progress["level_7"]},
        {"key": "level_8", "name": "Рівень 8", "unlocked": level_progress["level_8"]},
        {"key": "level_9", "name": "Рівень 9", "unlocked": level_progress["level_9"]},
        {"key": "level_10", "name": "Рівень 10", "unlocked": level_progress["level_10"]},
    ]

    if not hasattr(level_select_menu, "current_index"):
        level_select_menu.current_index = 0

    current_level = levels[level_select_menu.current_index]
    key = current_level["key"]

    img = pygame.transform.scale(level_images[key], (450, 250))
    rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(img, rect)

    color = BLUE if current_level["unlocked"] else GRAY
    pygame.draw.rect(screen, color, rect, 6, border_radius=10)
    draw_text(current_level["name"], font_button, WHITE, screen, WIDTH // 2, rect.bottom + 40)

    # Заблоковано
    if not current_level["unlocked"]:
        lock_overlay = pygame.Surface((450, 250), pygame.SRCALPHA)
        lock_overlay.fill((0, 0, 0, 180))
        screen.blit(lock_overlay, rect)
        lock_rect = lock_icon.get_rect(center=rect.center)
        screen.blit(lock_icon, lock_rect)
        draw_text("🔒 Заблоковано", font_button, WHITE, screen, WIDTH // 2, HEIGHT - 180 + 30)

    # Гортання
    left_arrow = font_button.render("←", True, WHITE)
    right_arrow = font_button.render("→", True, WHITE)
    left_rect = left_arrow.get_rect(center=(WIDTH // 2 - 350, HEIGHT // 2 - 50))
    right_rect = right_arrow.get_rect(center=(WIDTH // 2 + 350, HEIGHT // 2 - 50))
    screen.blit(left_arrow, left_rect)
    screen.blit(right_arrow, right_rect)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if left_rect.collidepoint(mouse) and click[0]:
        pygame.time.wait(200)
        level_select_menu.current_index = (level_select_menu.current_index - 1) % len(levels)
    elif right_rect.collidepoint(mouse) and click[0]:
        pygame.time.wait(200)
        level_select_menu.current_index = (level_select_menu.current_index + 1) % len(levels)

    # Грати
    if current_level["unlocked"]:
        if draw_button("▶ Грати", WIDTH // 2 - 100, HEIGHT - 180, 200, 60):
            level_passed = easy_level.easy_level()  # поки що один і той самий рівень для всіх
            if level_passed:
                unlock_next_level(key)
            return MENU

    # Назад
    if draw_button("↩ Назад", WIDTH // 2 - 130, HEIGHT - 90, 260, 60):
        return MENU

    pygame.display.update()
    return LEVEL_SELECT

# --- Правила ---
def show_rules():
    screen.fill((20, 20, 40))
    draw_text("Правила гри", font_title, WHITE, screen, WIDTH // 2, 150)
    rules = [
        "1. Керуй персонажем і стріляй по ворогах.",
        "2. Після перемоги відкривається новий рівень.",
        "3. Натисни ESC, щоб повернутися в меню."
    ]
    for i, line in enumerate(rules):
        draw_text(line, rules_font, WHITE, screen, WIDTH // 2, 300 + i * 40)
    if draw_button("↩ Назад", WIDTH // 2 - 130, HEIGHT - 90, 260, 60):
        return MENU
    pygame.display.update()
    return RULES

# --- Налаштування ---
def draw_settings_menu():
    global volume_music
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    panel = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 200, 500, 400)
    pygame.draw.rect(screen, (30, 30, 30), panel, border_radius=15)
    pygame.draw.rect(screen, WHITE, panel, 2, border_radius=15)

    title = font_button.render("Налаштування", True, WHITE)
    screen.blit(title, (panel.centerx - title.get_width() // 2, panel.top + 40))

    # Слайдер
    slider_x = panel.left + 100
    slider_y = panel.top + 160
    slider_w = 300
    pygame.draw.rect(screen, WHITE, (slider_x, slider_y, slider_w, 6))
    handle_x = int(slider_x + volume_music * slider_w)
    pygame.draw.circle(screen, YELLOW, (handle_x, slider_y + 3), 10)
    text = rules_font.render(f"Гучність: {int(volume_music * 100)}%", True, WHITE)
    screen.blit(text, (panel.centerx - text.get_width() // 2, slider_y - 40))

    # Назад
    back_rect = pygame.Rect(panel.centerx - 60, panel.bottom - 80, 120, 50)
    pygame.draw.rect(screen, (0, 0, 0), back_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, back_rect, 2, border_radius=10)
    back_text = font_button.render("Назад", True, WHITE)
    screen.blit(back_text, back_text.get_rect(center=back_rect.center))

    pygame.display.update()
    return pygame.Rect(slider_x, slider_y - 10, slider_w, 30), back_rect

# --- Головний цикл ---
load_progress()
clock = pygame.time.Clock()
slider_rect, back_rect = None, None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if show_settings:
                    if slider_rect and slider_rect.collidepoint(event.pos):
                        slider_dragging = True
                    elif back_rect and back_rect.collidepoint(event.pos):
                        show_settings = False
                elif settings_rect.collidepoint(event.pos):
                    show_settings = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                slider_dragging = False
        elif event.type == pygame.MOUSEMOTION and slider_dragging and show_settings:
            slider_x = slider_rect.left
            slider_w = slider_rect.width
            rel_x = event.pos[0] - slider_x
            volume_music = max(0.0, min(1.0, rel_x / slider_w))
            pygame.mixer.music.set_volume(volume_music)

    if show_settings:
        slider_rect, back_rect = draw_settings_menu()
    else:
        if state == MENU:
            state = main_menu()
        elif state == LEVEL_SELECT:
            state = level_select_menu()
        elif state == RULES:
            state = show_rules()

    clock.tick(60)