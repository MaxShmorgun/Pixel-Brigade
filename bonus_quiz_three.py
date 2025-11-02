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

# --- Нові 45 питань ---
questions = [
    ("Яка планета Сонячної системи найближча до Сонця?", ["Меркурій", "Венера", "Земля"], 0),
    ("Хто написав роман 'Гаррі Поттер'?", ["Джоан Роулінг", "Стівен Кінг", "Толкін"], 0),
    ("Скільки континентів на Землі?", ["6", "7", "5"], 1),
    ("Який організм виробляє кисень?", ["Риби", "Дерева", "Тварини"], 1),
    ("Яка країна вигадала піцу?", ["Італія", "Франція", "Іспанія"], 0),
    ("Скільки секунд у хвилині?", ["50", "60", "100"], 1),
    ("Яка столиця Польщі?", ["Прага", "Варшава", "Краків"], 1),
    ("Хто написав 'Заповіт'?", ["Шевченко", "Франко", "Коцюбинський"], 0),
    ("Яка найбільша тварина на Землі?", ["Слон", "Білий ведмідь", "Синій кит"], 2),
    ("Яка речовина робить небо блакитним?", ["Азот", "Кисень", "Розсіювання світла"], 2),
    ("Яке місто є столицею Франції?", ["Париж", "Берлін", "Рим"], 0),
    ("Який колір утворюється при змішуванні синього та жовтого?", ["Зелений", "Фіолетовий", "Помаранчевий"], 0),
    ("Який винахід допоміг людям літати?", ["Парашут", "Літак", "Повітряна куля"], 1),
    ("Яке море є найсолонішим у світі?", ["Червоне", "Мертве", "Середземне"], 1),
    ("Скільки днів у високосному році?", ["364", "366", "365"], 1),
    ("Хто є автором 'Ромео і Джульєтти'?", ["Шекспір", "Пушкін", "Данте"], 0),
    ("Яке місто називають 'Столицею Світу'?", ["Київ", "Лондон", "Варшава"], 1),
    ("Який птах може літати назад?", ["Колібрі", "Орел", "Голуб"], 0),
    ("Яке дерево дає жолуді?", ["Клен", "Дуб", "Сосна"], 1),
    ("Хто першим ступив на Місяць?", ["Юрій Гагарін", "Ніл Армстронг", "Базз Олдрін"], 1),
    ("Яка планета названа на честь бога моря?", ["Марс", "Нептун", "Юпітер"], 1),
    ("Яке місто є столицею Туреччини?", ["Анкара", "Стамбул", "Ізмір"], 0),
    ("Який метал є найціннішим?", ["Срібло", "Золото", "Платина"], 2),
    ("Скільки ніг у павука?", ["6", "8", "10"], 1),
    ("Який материк найменший?", ["Австралія", "Європа", "Антарктида"], 0),
    ("Яка річка протікає через Єгипет?", ["Ніл", "Амазонка", "Дунай"], 0),
    ("Яке море омиває Україну?", ["Чорне", "Балтійське", "Біле"], 0),
    ("Хто є автором 'Лісової пісні'?", ["Франко", "Леся Українка", "Шевченко"], 1),
    ("Який прилад використовують для вимірювання температури?", ["Термометр", "Барометр", "Компас"], 0),
    ("Який газ людина вдихає?", ["Азот", "Кисень", "Вуглекислий газ"], 1),
    ("Яке місто називають 'вічним'?", ["Рим", "Афіни", "Париж"], 0),
    ("Хто винайшов електричну лампу?", ["Едісон", "Белл", "Фарадей"], 0),
    ("Який океан найбільший?", ["Тихий", "Атлантичний", "Індійський"], 0),
    ("Яка країна є батьківщиною самураїв?", ["Китай", "Японія", "Корея"], 1),
    ("Яка планета має кільця?", ["Марс", "Сатурн", "Венера"], 1),
    ("Скільки зубів у дорослої людини?", ["28", "30", "32"], 2),
    ("Яка тварина є символом мудрості?", ["Сова", "Кіт", "Слон"], 0),
    ("Який процес називають диханням?", ["Поглинання кисню", "Виділення тепла", "Зростання"], 0),
    ("Яке місто є столицею Німеччини?", ["Берлін", "Мюнхен", "Гамбург"], 0),
    ("Який континент найтепліший?", ["Африка", "Азія", "Південна Америка"], 0),
    ("Хто створив теорію відносності?", ["Ейнштейн", "Ньютон", "Галілей"], 0),
    ("Яке явище супроводжується блискавкою?", ["Дощ", "Гроза", "Туман"], 1),
    ("Який прилад показує напрям?", ["Компас", "Телескоп", "Мікроскоп"], 0),
    ("Який метал притягується магнітом?", ["Залізо", "Мідь", "Алюміній"], 0),
    ("Який колір символізує мир?", ["Білий", "Чорний", "Червоний"], 0),
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
                    # ✅ Тепер потрібно 35 правильних із 45
                    res = end_menu(score >= 35, background_image)
                    if res == "restart":
                        return bonus_quiz(music_volume, sfx_volume)
                    else:
                        return "exit"
