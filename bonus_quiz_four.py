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

# --- Нові 55 питань ---
questions = [
    ("Яка планета є найбільшою у Сонячній системі?", ["Юпітер", "Сатурн", "Марс"], 0),
    ("Хто написав роман '1984'?", ["Оруелл", "Гемінґвей", "Діккенс"], 0),
    ("Який океан є найглибшим?", ["Тихий", "Атлантичний", "Індійський"], 0),
    ("Скільки сердець має восьминіг?", ["1", "2", "3"], 2),
    ("Який газ переважає в атмосфері Землі?", ["Азот", "Кисень", "Вуглекислий газ"], 0),
    ("Яка найвища гора у світі?", ["Еверест", "Кіліманджаро", "Монблан"], 0),
    ("Скільки кольорів у веселці?", ["6", "7", "8"], 1),
    ("Хто створив картину 'Мона Ліза'?", ["Леонардо да Вінчі", "Мікеланджело", "Рафаель"], 0),
    ("Яке місто є столицею Канади?", ["Оттава", "Торонто", "Монреаль"], 0),
    ("Хто відкрив Америку?", ["Колумб", "Магеллан", "Кук"], 0),
    ("Яка найменша планета Сонячної системи?", ["Меркурій", "Марс", "Плутон"], 0),
    ("Хто є автором пісні 'Ще не вмерла Україна'?", ["Вербицький", "Шевченко", "Лисенко"], 0),
    ("Яке місто є столицею Китаю?", ["Пекін", "Шанхай", "Гонконг"], 0),
    ("Скільки континентів на Землі?", ["6", "7", "5"], 1),
    ("Яка країна винайшла компас?", ["Китай", "Єгипет", "Греція"], 0),
    ("Хто першим полетів у космос?", ["Юрій Гагарін", "Ніл Армстронг", "Базз Олдрін"], 0),
    ("Який метал є найлегшим?", ["Алюміній", "Літій", "Магній"], 1),
    ("Яке море не має виходу в океан?", ["Каспійське", "Балтійське", "Чорне"], 0),
    ("Хто написав 'Кайдашева сім’я'?", ["Нечуй-Левицький", "Франко", "Коцюбинський"], 0),
    ("Який організм виробляє кисень?", ["Рослини", "Тварини", "Гриби"], 0),
    ("Яка тварина є символом Австралії?", ["Кенгуру", "Ему", "Коала"], 0),
    ("Хто створив електричну лампу?", ["Едісон", "Белл", "Фарадей"], 0),
    ("Яке місто є столицею Іспанії?", ["Мадрид", "Барселона", "Севілья"], 0),
    ("Який континент найхолодніший?", ["Антарктида", "Європа", "Азія"], 0),
    ("Скільки пальців на руках у людини?", ["10", "8", "12"], 0),
    ("Хто написав 'Катерину'?", ["Шевченко", "Франко", "Леся Українка"], 0),
    ("Яка планета названа на честь бога війни?", ["Марс", "Юпітер", "Сатурн"], 0),
    ("Яке місто є столицею Бразилії?", ["Бразиліа", "Ріо-де-Жанейро", "Сан-Паулу"], 0),
    ("Який птах є символом миру?", ["Голуб", "Сокіл", "Ластівка"], 0),
    ("Яка річка найдовша у світі?", ["Ніл", "Амазонка", "Янцзи"], 1),
    ("Хто є автором 'Лісової пісні'?", ["Леся Українка", "Франко", "Шевченко"], 0),
    ("Яка країна є батьківщиною піци?", ["Італія", "Франція", "Греція"], 0),
    ("Який континент найбільший?", ["Азія", "Африка", "Північна Америка"], 0),
    ("Яке місто називають 'вічним'?", ["Рим", "Афіни", "Париж"], 0),
    ("Який орган перекачує кров у тілі людини?", ["Серце", "Легені", "Печінка"], 0),
    ("Яке місто є столицею України?", ["Київ", "Львів", "Харків"], 0),
    ("Хто є автором 'Гамлета'?", ["Шекспір", "Данте", "Мольєр"], 0),
    ("Який метал притягується магнітом?", ["Залізо", "Мідь", "Срібло"], 0),
    ("Скільки днів у році?", ["365", "366", "360"], 0),
    ("Хто винайшов телефон?", ["Белл", "Едісон", "Марконі"], 0),
    ("Яке місто є столицею США?", ["Вашингтон", "Нью-Йорк", "Чикаго"], 0),
    ("Яка найбільша пустеля у світі?", ["Сахара", "Гобі", "Атакама"], 0),
    ("Який колір символізує любов?", ["Червоний", "Білий", "Синій"], 0),
    ("Який газ потрібен для дихання?", ["Кисень", "Азот", "Вуглекислий газ"], 0),
    ("Яке місто є столицею Японії?", ["Токіо", "Осака", "Кіото"], 0),
    ("Хто написав 'Енеїду'?", ["Котляревський", "Шевченко", "Франко"], 0),
    ("Яке море омиває південь України?", ["Чорне", "Азовське", "Біле"], 0),
    ("Яке місто називають 'Північна Пальміра'?", ["Санкт-Петербург", "Москва", "Мінськ"], 0),
    ("Яка країна є батьківщиною самураїв?", ["Японія", "Китай", "Корея"], 0),
    ("Хто винайшов радіо?", ["Марконі", "Белл", "Едісон"], 0),
    ("Який птах може літати назад?", ["Колібрі", "Орел", "Сокіл"], 0),
    ("Який океан найменший?", ["Північний Льодовитий", "Індійський", "Атлантичний"], 0),
    ("Скільки зубів має доросла людина?", ["32", "30", "28"], 0),
    ("Хто написав роман 'Тіні забутих предків'?", ["Коцюбинський", "Франко", "Леся Українка"], 0),
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
                    # ✅ Тепер потрібно 45 правильних із 55
                    res = end_menu(score >= 45, background_image)
                    if res == "restart":
                        return bonus_quiz(music_volume, sfx_volume)
                    else:
                        return "exit"
