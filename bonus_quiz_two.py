import pygame
import sys
import os

pygame.font.init()
pygame.mixer.init()

# --- Налаштування ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BACKGROUND_COLOR = (30, 30, 40)

FONT_MAIN = pygame.font.Font(None, 64)
FONT_SMALL = pygame.font.Font(None, 48)

BUTTON_WIDTH = 555
BUTTON_HEIGHT = 60
FEEDBACK_DELAY = 800  # мс

# --- Завантаження звуків ---
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        print(f"⚠️ Не вдалося завантажити звук: {path}")
        return None

sound_correct = load_sound("music/correct.wav")
sound_wrong = load_sound("music/wrong.mp3")
sound_win = load_sound("music/win.mp3")
sound_lose = load_sound("music/lose.wav")

# --- Нові 30 питань ---
questions = [
    ("Який континент є найбільшим за площею?", ["Африка", "Азія", "Європа"], 1),
    ("Який океан є найглибшим у світі?", ["Індійський", "Тихий", "Атлантичний"], 1),
    ("Яке місто є столицею Канади?", ["Оттава", "Торонто", "Монреаль"], 0),
    ("Яка тварина може літати, але не є птахом?", ["Бджола", "Летюча миша", "Кажан"], 1),
    ("Хто винайшов телефон?", ["Белл", "Едісон", "Марконі"], 0),
    ("Яка країна першою відправила людину в космос?", ["США", "СРСР", "Китай"], 1),
    ("Яка найвища гора у світі?", ["Еверест", "Кіліманджаро", "Монблан"], 0),
    ("Скільки градусів у прямому куті?", ["90", "60", "180"], 0),
    ("Яка речовина робить листя зеленим?", ["Хлорофіл", "Кисень", "Глюкоза"], 0),
    ("Який орган у людини перекачує кров?", ["Мозок", "Легені", "Серце"], 2),
    ("Хто написав «Кобзар»?", ["Шевченко", "Франко", "Леся Українка"], 0),
    ("Який газ утворюється при диханні людини?", ["Кисень", "Вуглекислий газ", "Азот"], 1),
    ("Який прилад показує час?", ["Компас", "Годинник", "Барометр"], 1),
    ("Хто відкрив закон всесвітнього тяжіння?", ["Ньютон", "Ейнштейн", "Галілей"], 0),
    ("Яка планета відома як 'червона'?", ["Марс", "Венера", "Юпітер"], 0),
    ("Яке місто називають 'містом вітрів'?", ["Чикаго", "Нью-Йорк", "Вашингтон"], 0),
    ("Який метал використовують для виготовлення фольги?", ["Залізо", "Алюміній", "Мідь"], 1),
    ("Який континент найхолодніший?", ["Антарктида", "Європа", "Північна Америка"], 0),
    ("Яка річка є найдовшою у світі?", ["Амазонка", "Ніл", "Янцзи"], 1),
    ("Яке тіло обертається навколо планети?", ["Комета", "Супутник", "Метеорит"], 1),
    ("Скільки кольорів у веселці?", ["7", "6", "8"], 0),
    ("Яка тварина відкладає яйця, але є ссавцем?", ["Єхидна", "Кенгуру", "Кіт"], 0),
    ("Яка країна відома створенням пірамід?", ["Індія", "Єгипет", "Ірак"], 1),
    ("Який винахід дозволив людям бачити дуже дрібні об’єкти?", ["Телескоп", "Мікроскоп", "Радар"], 1),
    ("Який газ становить більшість атмосфери Землі?", ["Азот", "Кисень", "Водень"], 0),
    ("Яке небесне тіло є зорею?", ["Сонце", "Місяць", "Венера"], 0),
    ("Яка планета має найбільшу кількість супутників?", ["Сатурн", "Юпітер", "Марс"], 1),
    ("Яке місто є столицею Японії?", ["Осака", "Токіо", "Кіото"], 1),
    ("Який процес називається перетворенням води у пару?", ["Кипіння", "Конденсація", "Випаровування"], 2),
    ("Яка наука вивчає живі організми?", ["Фізика", "Біологія", "Хімія"], 1),
]

button_positions = [
    (320, 330),
    (320, 455),
    (320, 580),
]

def draw_text_center(text, font, color, y):
    screen = pygame.display.get_surface()
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(txt, rect)

def draw_question(q_index, selected):
    screen = pygame.display.get_surface()
    q, options, correct = questions[q_index]

    draw_text_center(f"Питання {q_index + 1}/{len(questions)}", FONT_SMALL, WHITE, 80)
    question_rect = pygame.Rect(300, 170, 600, 120)

    words = q.replace('\n', ' ').split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if FONT_MAIN.size(test_line)[0] > question_rect.width - 40:
            lines.append(current_line.strip())
            current_line = word + " "
        else:
            current_line = test_line
    lines.append(current_line.strip())

    line_height = FONT_MAIN.get_height()
    total_height = len(lines) * line_height
    start_y = question_rect.y + (question_rect.height - total_height) // 2

    for i, line in enumerate(lines):
        text_surf = FONT_MAIN.render(line, True, WHITE)
        text_rect = text_surf.get_rect(center=(question_rect.centerx, start_y + i * line_height))
        screen.blit(text_surf, text_rect)

    mouse = pygame.mouse.get_pos()
    for i, opt in enumerate(options):
        x, y = button_positions[i]
        rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)

        if selected is None:
            current_color = (0, 80, 150, 180) if rect.collidepoint(mouse) else (0, 50, 100, 140)
        else:
            if i == selected:
                current_color = GREEN if i == correct else RED
            else:
                current_color = (0, 50, 100, 140)

        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill(current_color)
        screen.blit(s, rect.topleft)
        border_color = (0, 150, 255)
        if selected is not None and i == selected:
            border_color = current_color[:3]
        pygame.draw.rect(screen, border_color, rect, 5, border_radius=10)

        full_text = f"{chr(65 + i)}) {opt}"
        text_surf = FONT_SMALL.render(full_text, True, WHITE)
        text_rect = text_surf.get_rect(center=(rect.centerx, rect.centery))
        screen.blit(text_surf, text_rect)

def bonus_quiz(music_volume=0.5, sfx_volume=0.5):
    screen = pygame.display.get_surface()
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    try:
        background_image = pygame.image.load("image/fon_quiz.png").convert()
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    except:
        background_image = pygame.Surface((WIDTH, HEIGHT))
        background_image.fill(BACKGROUND_COLOR)

    try:
        exit_img = pygame.image.load("image/back_arrow.png").convert_alpha()
        exit_img = pygame.transform.scale(exit_img, (80, 80))
    except:
        exit_img = pygame.Surface((80, 80))
        exit_img.fill((150, 0, 0))
    exit_rect = exit_img.get_rect(topleft=(20, 20))

    current_question = 0
    selected = None
    score = 0
    feedback_timer = 0
    pygame.mixer.music.set_volume(music_volume)

    def draw_button_end_menu(text, x, y, width, height):
        mouse = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, width, height)
        color = (50, 50, 50)
        if rect.collidepoint(mouse):
            color = (120, 120, 255)
        pygame.draw.rect(screen, color, rect, border_radius=12)
        txt = FONT_SMALL.render(text, True, WHITE)
        txt_rect = txt.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(txt, txt_rect)
        return rect

    def end_menu(win, bg_image):
        if win and sound_win: sound_win.play()
        if not win and sound_lose: sound_lose.play()
        while True:
            screen.blit(bg_image, (0, 0))
            fade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            fade.fill((0, 0, 0, 180))
            screen.blit(fade, (0, 0))

            text = "Ти переміг!" if win else "Ти програв!"
            color = GREEN if win else RED
            draw_text_center(text, FONT_MAIN, color, HEIGHT // 2 - 120)
            draw_text_center(f"Результат: {score}/{len(questions)}", FONT_SMALL, WHITE, HEIGHT // 2 - 50)

            restart = draw_button_end_menu("🔁 Почати знову", WIDTH // 2 - 150, HEIGHT // 2 + 20, 300, 60)
            back = draw_button_end_menu("🏠 Вийти в меню", WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 60)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if restart.collidepoint(mx, my):
                        return "restart"
                    if back.collidepoint(mx, my):
                        return "exit"
            clock.tick(60)

    running = True
    while running:
        screen.blit(background_image, (0, 0))
        screen.blit(exit_img, exit_rect)
        draw_question(current_question, selected)
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if exit_rect.collidepoint(mx, my):
                    return "exit"

                if selected is None:
                    _, _, correct_index = questions[current_question]
                    for i in range(3):
                        x, y = button_positions[i]
                        rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
                        if rect.collidepoint(mx, my):
                            selected = i
                            feedback_timer = pygame.time.get_ticks()
                            if selected == correct_index:
                                score += 1
                                if sound_correct: sound_correct.play()
                            else:
                                if sound_wrong: sound_wrong.play()

        if selected is not None:
            draw_question(current_question, selected)
            screen.blit(exit_img, exit_rect)
            pygame.display.flip()
            if pygame.time.get_ticks() - feedback_timer > FEEDBACK_DELAY:
                current_question += 1
                selected = None
                if current_question >= len(questions):
                    res = end_menu(score >= 20, background_image)
                    if res == "restart":
                        return bonus_quiz(music_volume, sfx_volume)
                    else:
                        return "exit"
