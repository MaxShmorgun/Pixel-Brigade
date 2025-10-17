import pygame
import sys
import easy_level
import json 

pygame.init()
pygame.mixer.init()

# --- Налаштування збереження ---
SAVE_FILE = "save_data.json" # Файл, де буде зберігатися прогрес

# --- Параметри екрану ---
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Brigade")

# --- Зображення ---
background = pygame.image.load("image/menu_bg.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

settings_icon = pygame.image.load("image/settings.png")
settings_icon = pygame.transform.scale(settings_icon, (50, 50))
settings_rect = settings_icon.get_rect(topright=(WIDTH - 10, 10))

# <<< ЗОБРАЖЕННЯ ЗАМКА >>>
try:
    lock_icon = pygame.image.load("image/lock.png") 
    lock_icon = pygame.transform.scale(lock_icon, (100, 100))
except pygame.error:
    lock_icon = pygame.Surface((100, 100), pygame.SRCALPHA)
    lock_icon.fill((255, 0, 0, 0))
    pygame.draw.rect(lock_icon, (255, 0, 0, 200), (0, 0, 100, 100), border_radius=10)


# --- Зображення рівнів ---
level_images = {
    "easy": pygame.image.load("image/level_easy.jpg"),
    "medium": pygame.image.load("image/level_medium.jpg"),
    "hard": pygame.image.load("image/level_hard.jpg")
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

# <<< СИСТЕМА ПРОГРЕСУ РІВНІВ (Змінюється функцією load_progress) >>>
DEFAULT_PROGRESS = {
    "easy": True,
    "medium": False,
    "hard": False
}
level_progress = DEFAULT_PROGRESS # Початкове значення

# --- Функції збереження/завантаження ---
def load_progress():
    """Завантажує прогрес з файлу, або повертає стандартний, якщо файл не знайдено."""
    global level_progress
    try:
        with open(SAVE_FILE, 'r') as f:
            level_progress = json.load(f)
        print("Прогрес гри успішно завантажено.")
    except FileNotFoundError:
        print("Файл збереження не знайдено. Використовується стандартний прогрес.")
        level_progress = DEFAULT_PROGRESS.copy()
    except json.JSONDecodeError:
        print("Помилка читання файлу збереження. Використовується стандартний прогрес.")
        level_progress = DEFAULT_PROGRESS.copy()

def save_progress():
    """Зберігає поточний прогрес у файл."""
    global level_progress
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(level_progress, f, indent=4)
        print("Прогрес гри успішно збережено.")
    except Exception as e:
        print(f"Помилка при збереженні прогресу: {e}")

# --- Функції УПРАВЛІННЯ ПРОГРЕСОМ (МОДИФІКОВАНО) ---
def unlock_next_level(current_level_key):
    """Розблоковує наступний рівень та зберігає прогрес."""
    global level_progress
    levels_order = ["easy", "medium", "hard"]
    
    try:
        current_index = levels_order.index(current_level_key)
        next_index = current_index + 1
        
        if next_index < len(levels_order):
            next_level_key = levels_order[next_index]
            
            if not level_progress[next_level_key]:
                level_progress[next_level_key] = True 
                print(f"Рівень {next_level_key} розблоковано!")
                # <<< ЗБЕРЕЖЕННЯ ПІСЛЯ РОЗБЛОКУВАННЯ >>>
                save_progress() 
            
    except ValueError:
        pass


# --- Інші Функції (Без змін) ---
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, rect)

def draw_button(text, x, y, width, height):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, width, height)
    
    color = GRAY
    if rect.collidepoint(mouse):
        color = BLUE
        if click[0] == 1:
            pygame.time.wait(150)
            return True
        
    pygame.draw.rect(screen, color, rect, border_radius=10)
    draw_text(text, font_button, WHITE, screen, x + width // 2, y + height // 2)
    return False

def main_menu():
    screen.blit(background, (0, 0))
    screen.blit(settings_icon, settings_rect)

    if draw_button("▶ Почати гру", WIDTH // 2 - 130, 380, 260, 60):
        return LEVEL_SELECT
    if draw_button("📜 Правила", WIDTH // 2 - 130, 470, 260, 60):
        return RULES
    if draw_button("❌ Вийти", WIDTH // 2 - 130, 560, 260, 60):
        # Можливо, варто викликати save_progress() тут, але краще робити це автоматично при розблокуванні.
        pygame.quit()
        sys.exit()
    pygame.display.update()
    return MENU

def level_select_menu():
    screen.blit(background, (0, 0))

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150)) 
    screen.blit(overlay, (0, 0))

    draw_text("Вибір рівня", font_title, WHITE, screen, WIDTH // 2, 120)

    levels = [
        {"key": "easy", "name": "Легкий", "unlocked": level_progress["easy"]},
        {"key": "medium", "name": "Середній", "unlocked": level_progress["medium"]},
        {"key": "hard", "name": "Важкий", "unlocked": level_progress["hard"]},
    ]

    if not hasattr(level_select_menu, "current_index"):
        level_select_menu.current_index = 0

    current_level = levels[level_select_menu.current_index]

    original_img = level_images[current_level["key"]]
    stretched_size = (450, 250)
    img = pygame.transform.scale(original_img, stretched_size)
    
    rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(img, rect)

    color = BLUE if current_level["unlocked"] else GRAY
    pygame.draw.rect(screen, color, rect, 6, border_radius=10)
    draw_text(current_level["name"], font_button, WHITE, screen, WIDTH // 2, rect.bottom + 40)
    
    # <<< ВІДОБРАЖЕННЯ ЗАМКА >>>
    if not current_level["unlocked"]:
        lock_overlay = pygame.Surface(stretched_size, pygame.SRCALPHA)
        lock_overlay.fill((0, 0, 0, 180)) 
        screen.blit(lock_overlay, rect)

        lock_rect = lock_icon.get_rect(center=rect.center)
        screen.blit(lock_icon, lock_rect)
        
        draw_text("🔒 Заблоковано", font_button, WHITE, screen, WIDTH // 2, HEIGHT - 180 + 30)


    # --- Кнопки-горталки ---
    left_arrow = font_button.render("←", True, WHITE)
    right_arrow = font_button.render("→", True, WHITE)
    left_rect = left_arrow.get_rect(center=(WIDTH // 2 - 350, HEIGHT // 2 - 50)) 
    right_rect = right_arrow.get_rect(center=(WIDTH // 2 + 350, HEIGHT // 2 - 50)) 
    screen.blit(left_arrow, left_rect)
    screen.blit(right_arrow, right_rect)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Гортання рівнів
    if left_rect.collidepoint(mouse) and click[0]:
        pygame.time.wait(200)
        level_select_menu.current_index = (level_select_menu.current_index - 1) % len(levels)
    elif right_rect.collidepoint(mouse) and click[0]:
        pygame.time.wait(200)
        level_select_menu.current_index = (level_select_menu.current_index + 1) % len(levels)

    # --- Кнопка "Грати" ---
    if current_level["unlocked"]:
        if draw_button("▶ Грати", WIDTH // 2 - 100, HEIGHT - 180, 200, 60):
            pygame.time.wait(150)
            
            level_passed = False 
            
            if current_level["key"] == "easy":
                level_passed = easy_level.easy_level() 
            
            if level_passed:
                unlock_next_level(current_level["key"])
                
            return MENU
    
    # --- Кнопка Назад ---
    if draw_button("↩ Назад", WIDTH // 2 - 130, HEIGHT - 90, 260, 60):
        return MENU

    pygame.display.update()
    return LEVEL_SELECT


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

    # Слайдер гучності
    slider_x = panel.left + 100
    slider_y = panel.top + 160
    slider_w = 300
    pygame.draw.rect(screen, WHITE, (slider_x, slider_y, slider_w, 6))
    handle_x = int(slider_x + volume_music * slider_w)
    pygame.draw.circle(screen, YELLOW, (handle_x, slider_y + 3), 10)
    text = rules_font.render(f"Гучність: {int(volume_music * 100)}%", True, WHITE)
    screen.blit(text, (panel.centerx - text.get_width() // 2, slider_y - 40))

    # Кнопка Назад
    back_rect = pygame.Rect(panel.centerx - 60, panel.bottom - 80, 120, 50)
    pygame.draw.rect(screen, (0, 0, 0), back_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, back_rect, 2, border_radius=10)
    back_text = font_button.render("Назад", True, WHITE)
    screen.blit(back_text, back_text.get_rect(center=back_rect.center))

    pygame.display.update()
    return pygame.Rect(slider_x, slider_y - 10, slider_w, 30), back_rect


load_progress() 

# --- Основний цикл ---
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