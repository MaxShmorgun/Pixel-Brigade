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

# --- 70 питань ---
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
    ("Яке місто є столицею Китаю?", ["Пекін", "Шанхай", "Гонконг"], 0),
    ("Скільки континентів на Землі?", ["6", "7", "5"], 1),
    ("Який метал є найлегшим?", ["Алюміній", "Літій", "Магній"], 1),
    ("Хто першим полетів у космос?", ["Гагарін", "Армстронг", "Тітов"], 0),
    ("Який океан найменший?", ["Північний Льодовитий", "Індійський", "Атлантичний"], 0),
    ("Яке місто є столицею Франції?", ["Париж", "Лондон", "Рим"], 0),
    ("Хто винайшов телефон?", ["Белл", "Едісон", "Марконі"], 0),
    ("Яка річка найдовша у світі?", ["Ніл", "Амазонка", "Янцзи"], 1),
    ("Яка планета найближча до Сонця?", ["Меркурій", "Венера", "Марс"], 0),
    ("Який континент найхолодніший?", ["Антарктида", "Європа", "Азія"], 0),
    ("Хто є автором 'Лісової пісні'?", ["Леся Українка", "Франко", "Шевченко"], 0),
    ("Яке місто є столицею Японії?", ["Токіо", "Осака", "Кіото"], 0),
    ("Хто створив електричну лампу?", ["Едісон", "Белл", "Фарадей"], 0),
    ("Яка країна є батьківщиною піци?", ["Італія", "Франція", "Греція"], 0),
    ("Яке місто є столицею США?", ["Вашингтон", "Нью-Йорк", "Лос-Анджелес"], 0),
    ("Який птах може літати назад?", ["Колібрі", "Орел", "Сокіл"], 0),
    ("Який газ потрібен для дихання?", ["Кисень", "Азот", "Гелій"], 0),
    ("Хто винайшов радіо?", ["Марконі", "Белл", "Едісон"], 0),
    ("Яка річка протікає через Київ?", ["Дніпро", "Дністер", "Буг"], 0),
    ("Хто написав 'Кобзар'?", ["Шевченко", "Франко", "Леся Українка"], 0),
    ("Який колір символізує мир?", ["Білий", "Червоний", "Синій"], 0),
    ("Який метал притягується магнітом?", ["Залізо", "Мідь", "Срібло"], 0),
    ("Яке море омиває південь України?", ["Чорне", "Азовське", "Балтійське"], 0),
    ("Яка країна винайшла порох?", ["Китай", "Єгипет", "Греція"], 0),
    ("Хто є автором 'Гамлета'?", ["Шекспір", "Данте", "Мольєр"], 0),
    ("Яке місто називають 'вічним'?", ["Рим", "Афіни", "Париж"], 0),
    ("Скільки зубів має доросла людина?", ["32", "30", "28"], 0),
    ("Хто написав 'Тіні забутих предків'?", ["Коцюбинський", "Франко", "Леся Українка"], 0),
    ("Який океан омиває Австралію?", ["Індійський", "Атлантичний", "Тихий"], 2),
    ("Яка планета названа на честь бога війни?", ["Марс", "Юпітер", "Сатурн"], 0),
    ("Який континент найбільший?", ["Азія", "Африка", "Північна Америка"], 0),
    ("Яка країна є батьківщиною самураїв?", ["Японія", "Китай", "Корея"], 0),
    ("Яка найменша планета Сонячної системи?", ["Меркурій", "Плутон", "Марс"], 0),
    ("Яке місто називають 'Північна Пальміра'?", ["Санкт-Петербург", "Москва", "Мінськ"], 0),
    ("Скільки днів у році?", ["365", "366", "364"], 0),
    ("Хто винайшов комп’ютер?", ["Тюрінг", "Белл", "Ньютон"], 0),
    ("Яке місто є столицею Іспанії?", ["Мадрид", "Барселона", "Севілья"], 0),
    ("Який птах є символом миру?", ["Голуб", "Сокіл", "Ластівка"], 0),
    ("Який орган перекачує кров?", ["Серце", "Печінка", "Легені"], 0),
    ("Який газ робить воду газованою?", ["Вуглекислий", "Кисень", "Азот"], 0),
    ("Хто є автором пісні 'Ще не вмерла Україна'?", ["Вербицький", "Шевченко", "Лисенко"], 0),
    ("Яке місто є столицею Бразилії?", ["Бразиліа", "Ріо-де-Жанейро", "Сан-Паулу"], 0),
    ("Який океан найбільший?", ["Тихий", "Індійський", "Атлантичний"], 0),
    ("Хто написав 'Енеїду'?", ["Котляревський", "Шевченко", "Франко"], 0),
    ("Яка тварина є символом Австралії?", ["Кенгуру", "Коала", "Ему"], 0),
    ("Яка пустеля найбільша у світі?", ["Сахара", "Гобі", "Атакама"], 0),
    ("Хто написав 'Кайдашева сім’я'?", ["Нечуй-Левицький", "Франко", "Коцюбинський"], 0),
    ("Яка країна є батьківщиною футболу?", ["Англія", "Італія", "Іспанія"], 0),
    ("Яке місто є столицею України?", ["Київ", "Львів", "Харків"], 0),
    ("Хто винайшов електрику?", ["Фарадей", "Едісон", "Белл"], 0),
    ("Яка планета названа на честь бога краси?", ["Венера", "Марс", "Юпітер"], 0),
    ("Яка тварина найбільша на Землі?", ["Синій кит", "Слон", "Жираф"], 0),
    ("Яке місто є столицею Німеччини?", ["Берлін", "Мюнхен", "Гамбург"], 0),
    ("Який колір отримують при змішуванні синього і жовтого?", ["Зелений", "Фіолетовий", "Помаранчевий"], 0),
    ("Яка країна відома фараонами?", ["Єгипет", "Ірак", "Іран"], 0),
    ("Скільки супутників у Землі?", ["1", "2", "3"], 0),
    ("Хто написав 'Маленького принца'?", ["Екзюпері", "Гюго", "Верн"], 0),
    ("Яке місто є столицею Польщі?", ["Варшава", "Краків", "Гданськ"], 0),
    ("Яке море є найсолонішим?", ["Червоне", "Мертве", "Середземне"], 1),
]

# --- позиції кнопок ---
button_positions = [(320, 330), (320, 455), (320, 580)]

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
        pygame.draw.rect(screen, (0, 150, 255), rect, 5, border_radius=10)

        full_text = f"{chr(65 + i)}) {opt}"
        text_surf = FONT_SMALL.render(full_text, True, WHITE)
        text_rect = text_surf.get_rect(center=(rect.centerx, rect.centery))
        screen.blit(text_surf, text_rect)

def bonus_quiz(music_volume=0.5, sfx_volume=0.5):
    screen = pygame.display.get_surface()
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    try:
        bg = pygame.image.load("image/fon_quiz.png").convert()
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    except:
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.fill(BACKGROUND_COLOR)

    try:
        exit_img = pygame.image.load("image/back_arrow.png").convert_alpha()
        exit_img = pygame.transform.scale(exit_img, (80, 80))
    except:
        exit_img = pygame.Surface((80, 80))
        exit_img.fill((150, 0, 0))
    exit_rect = exit_img.get_rect(topleft=(20, 20))

    score = 0
    selected = None
    feedback_timer = 0
    current = 0
    pygame.mixer.music.set_volume(music_volume)
        # --- Встановлюємо гучність для всіх звуків ---
    if sound_correct: sound_correct.set_volume(sfx_volume)
    if sound_wrong: sound_wrong.set_volume(sfx_volume)
    if sound_win: sound_win.set_volume(sfx_volume)
    if sound_lose: sound_lose.set_volume(sfx_volume)


    def end_menu(win):
        if win and sound_win: sound_win.play()
        if not win and sound_lose: sound_lose.play()
        while True:
            screen.blit(bg, (0, 0))
            fade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            fade.fill((0, 0, 0, 180))
            screen.blit(fade, (0, 0))
            draw_text_center("Ти переміг!" if win else "Ти програв!", FONT_MAIN, GREEN if win else RED, HEIGHT // 2 - 120)
            draw_text_center(f"Результат: {score}/{len(questions)}", FONT_SMALL, WHITE, HEIGHT // 2 - 50)
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            clock.tick(60)

    running = True
    while running:
        screen.blit(bg, (0, 0))
        screen.blit(exit_img, exit_rect)
        draw_question(current, selected)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if exit_rect.collidepoint(mx, my):
                    return "exit"
                if selected is None:
                    _, _, correct = questions[current]
                    for i in range(3):
                        x, y = button_positions[i]
                        rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
                        if rect.collidepoint(mx, my):
                            selected = i
                            feedback_timer = pygame.time.get_ticks()
                            if selected == correct:
                                score += 1
                                if sound_correct: sound_correct.play()
                            else:
                                if sound_wrong: sound_wrong.play()

        if selected is not None:
            if pygame.time.get_ticks() - feedback_timer > FEEDBACK_DELAY:
                current += 1
                selected = None
                if current >= len(questions):
                    win = score >= 60
                    end_menu(win)
                    return "exit"
        clock.tick(60)
