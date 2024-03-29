import tkinter as tk
from operator import itemgetter
import json
import ctypes
from ctypes import windll
from tkinter import ttk
from tkinter.messagebox import askyesno
import sys, time, random
import os
from random import randrange
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import requests
import urllib.request 

username = "Unnamed"
import pygame
import pygame_menu
def usernamedefiner(value):
    global username
    print('Userinput')
    username = value
    print('Username: {0}'.format(username)) 
    print('Value: {0}'.format(value))
difficulty = 'EASY'
# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
DIFFICULTYGAME = 25
Fullscreen = False
# Window size
frame_size_x = 600
frame_size_y = 600
# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[Client] Game successfully initialised')
    print()
os.environ['SDL_VIDEO_CENTERED'] = '1'
surface = pygame.display.set_mode((600, 400))

version='1.4'
serverip='http://15.236.97.173:1337/scores'
# Initialise game window
def connect(host=serverip):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False
# test
print('Server responding' if connect() else 'Server not responding')
if connect():
    ONLINEMODE = True
else:
    ONLINEMODE = False

def Pressound():
    pygame.mixer.music.load('Assets/Press.wav')
    pygame.mixer.music.play(1)
def gameoversound():
    pygame.mixer.music.load('Assets/Gameover.ogg')
    pygame.mixer.music.play(1)


# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
ABOUT = ['Version {0}'.format(version),
         'Author: @{0}'.format("Enzogaming59430"),
         '',  # new lineq
         'Email: {0}'.format('enzo_ignaes@hotmail.com')]
DIFFICULTY = ['EASY']
FPS = 60
WINDOW_SIZE = (800, 600)

# noinspection PyTypeChecker
clock = None  # type: pygame.time.Clock
# noinspection PyTypeChecker
main_menu = None  # type: pygame_menu.Menu
# noinspection PyTypeChecker
surface = None  # type: pygame.Surface

background_image = pygame_menu.baseimage.BaseImage(
    image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_WALLPAPER
)

# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def change_difficulty(value, difficulty):
    
    """
    Change difficulty of the game.

    :param value: Tuple containing the data of the selected object
    :type value: tuple
    :param difficulty: Optional parameter passed as argument to add_selector
    :type difficulty: str
    :return: None
    """
    
    selected, index = value
    print('Selected difficulty: "{0}" ({1}) at index {2}'.format(selected, difficulty, index))
    DIFFICULTY[0] = difficulty

def change_online(value, onlinemode):
    global ONLINEMODE
    """
    Change difficulty of the game.

    :param value: Tuple containing the data of the selected object
    :type value: tuple
    :param difficulty: Optional parameter passed as argument to add_selector
    :type difficulty: str
    :return: None
    """
    if onlinemode == 'first':
        ONLINEMODE = True
    elif onlinemode == 'last':
        ONLINEMODE = False
    selected, index = value
    print('Selected online: "{0}" ({1}) at index {2}'.format(selected, onlinemode, index))
def change_fullscreen(value, onlinemode):
    global Fullscreen
    """
    Change difficulty of the game.

    :param value: Tuple containing the data of the selected object
    :type value: tuple
    :param difficulty: Optional parameter passed as argument to add_selector
    :type difficulty: str
    :return: None
    """
    if onlinemode == 'first':
        ctypes.windll.user32.SetProcessDPIAware()
        true_res = (windll.user32.GetSystemMetrics(0),windll.user32.GetSystemMetrics(1))
        pygame.display.set_mode(true_res,pygame.Fullscreen)
        Fullscreen = True
    elif onlinemode == 'last':
        pygame.display.set_mode((600,400), pygame.RESIZABLE)
        Fullscreen = False
    selected, index = value
    print('Selected online: "{0}" ({1}) at index {2}'.format(selected, onlinemode, index))
def random_color():
    """
    Return a random color.

    :return: Color tuple
    :rtype: tuple
    """
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)

def EnglishGame():
    pygame.mixer.init()
    if Fullscreen == False:
        game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
    else:
        game_window = (frame_size_x, frame_size_y)
    
    # Colors (R, G, B)
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)
    
    
    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()
    
    
    # Game variables
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
    
    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True
    
    direction = 'RIGHT'
    change_to = direction
    
    score = 0

    
    # Game Over
    def game_over():
        
        repr(score).encode('utf-8')
        pygame.mixer.music.stop()
        gameoversound()
        my_font = pygame.font.Font('Assets\pixelart.ttf', 90)
        game_over_surface = my_font.render('Game over', True, white)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
        game_window.fill(black)
        game_window.blit(game_over_surface, game_over_rect)
        show_score(0, red, 'Assets\pixelart.ttf', 40)
        pygame.display.flip()
        time.sleep(5)
        if ONLINEMODE == True:
            response = requests.get(url=serverip + '?_sort=score:desc')
            print(score)
            print(username)
            print(DIFFICULTY)
            requests.post(url=serverip, json={"score": score, "name": username, "difficulty": DIFFICULTY})
        elif ONLINEMODE == False:
            json_obj = {}
            json_obj['json'] = []
            json_obj['json'].append({
                'Username' : username,
                'Score' : score
                })
            with open('Scores.json','w') as jsonFile:
                json.dump(json_obj, jsonFile)
        mainEnglish()
    
    
    # Score
    def show_score(choice, color, font, size):
        score_font = pygame.font.Font(font, size)
        score_surface = score_font.render('Score ' + str(score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (frame_size_x/10, 15)
        else:
            score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
        game_window.blit(score_surface, score_rect)
        # pygame.display.flip()
    
    
    pygame.mixer.music.load('Assets/Whitty.wav')
    pygame.mixer.music.play(-1)
    # Main logic
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w') or event.key == ord('z'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a') or event.key == ord('q'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
    
        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
    
        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10
    
        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()
    
        # Spawning food on the screen
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True
    
        # GFX
        game_window.fill(black)
        for pos in snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    
        # Snake food
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    
        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
            game_over()
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
            game_over()
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()
        show_score(1, white, 'Assets\pixelart.ttf', 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(DIFFICULTYGAME)

def FrenchGame():
    pygame.mixer.init()
    game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
    
    # Colors (R, G, B)
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)
    
    
    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()
    
    
    # Game variables
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
    
    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True
    
    direction = 'RIGHT'
    change_to = direction
    
    score = 0

    
    # Game Over
    def game_over():
        
        repr(score).encode('utf-8')
        pygame.mixer.music.stop()
        gameoversound()
        my_font = pygame.font.SysFont('Assets\pixelart.ttf', 90)
        game_over_surface = my_font.render('Game over', True, white)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
        game_window.fill(black)
        game_window.blit(game_over_surface, game_over_rect)
        show_score(0, red, 'fois', 20)
        pygame.display.flip()
        time.sleep(5)
        if ONLINEMODE == True:
            response = requests.get(url=serverip + '?_sort=score:desc')
            print(score)
            print(username)
            print(DIFFICULTY)
            requests.post(url=serverip, json={"score": score, "name": username, "difficulty": DIFFICULTY})
        elif ONLINEMODE == False:
            json_obj = {}
            json_obj['json'] = []
            json_obj['json'].append({
                'Username' : username,
                'Score' : score
                })
            with open('Scores.json','w') as jsonFile:
                json.dump(json_obj, jsonFile)
        mainEnglish()
    
    
    # Score
    def show_score(choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (frame_size_x/10, 15)
        else:
            score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
        game_window.blit(score_surface, score_rect)
        # pygame.display.flip()
    
    
    pygame.mixer.music.load('Assets/Whitty.wav')
    pygame.mixer.music.play(-1)
    # Main logic
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w') or event.key == ord('z'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a') or event.key == ord('q'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
    
        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
    
        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10
    
        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()
    
        # Spawning food on the screen
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True
    
        # GFX
        game_window.fill(black)
        for pos in snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    
        # Snake food
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    
        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
            game_over()
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
            game_over()
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()
        show_score(1, white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(DIFFICULTYGAME)

def play_functionenglish(difficulty, font, test=False):
    assert isinstance(difficulty, (tuple, list))
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)
    # Define globals
    global DIFFICULTYGAME
    global main_menu
    global clock
    #print(DIFFICULTYGAME)
    if difficulty == 'EASY':
        print(DIFFICULTYGAME)
        print('Returned Easy')
        DIFFICULTYGAME = 10
        print(DIFFICULTYGAME)
    elif difficulty == 'MEDIUM':
        print(DIFFICULTYGAME)
        print('Returned Medium')
        DIFFICULTYGAME = 25
        print(DIFFICULTYGAME)
    elif difficulty == 'HARD':
        print(DIFFICULTYGAME)
        print('Returned Hard')
        DIFFICULTYGAME = 40
        print(DIFFICULTYGAME)
        
    else:
        raise Exception('Unknown difficulty {0}'.format(difficulty))
    print(DIFFICULTYGAME)
    EnglishGame()
def play_functionfrench(difficulty, font, test=False):
    assert isinstance(difficulty, (tuple, list))
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)
    # Define globals
    global DIFFICULTYGAME
    global main_menu
    global clock
    #print(DIFFICULTYGAME)
    if difficulty == 'EASY':
        print(DIFFICULTYGAME)
        print('Returned Easy')
        DIFFICULTYGAME = 10
        print(DIFFICULTYGAME)
    elif difficulty == 'MEDIUM':
        print(DIFFICULTYGAME)
        print('Returned Medium')
        DIFFICULTYGAME = 25
        print(DIFFICULTYGAME)
    elif difficulty == 'HARD':
        print(DIFFICULTYGAME)
        print('Returned Hard')
        DIFFICULTYGAME = 40
        print(DIFFICULTYGAME)
        
    else:
        raise Exception('Unknown difficulty {0}'.format(difficulty))
    print(DIFFICULTYGAME)
    FrenchGame()
def main_background():
    """
    Function used by menus, draw on background while menu is active.

    :return: None
    """
    background_image.draw(surface)
def mainEnglish(test=False):
    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global clock
    global main_menu
    global surface

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    surface = pygame.display.set_mode((WINDOW_SIZE), pygame.RESIZABLE)
    pygame.display.set_caption('Snake game')
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus: Play Menu
    # -------------------------------------------------------------------------
    play_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        title='Play Menu',
        width=WINDOW_SIZE[0] * 0.75
    )

    submenu_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    submenu_theme.widget_font_size = 15
    play_submenu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.5,
        theme=submenu_theme,
        title='Submenu',
        width=WINDOW_SIZE[0] * 0.7
    )
    for i in range(30):
        play_submenu.add_button('Back {0}'.format(i), pygame_menu.events.BACK)
    play_submenu.add_button('Return to main menu', pygame_menu.events.RESET)
    Pressound()
    play_menu.add_button('Start',  # When pressing return -> play(DIFFICULTY[0], font)
                         play_functionenglish,
                         DIFFICULTY,
                         pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
    play_menu.add_text_input(
        'Username: ',
        default='John',
        onreturn=usernamedefiner,
        textinput_id='Username'
    )
    play_menu.add_selector('Select difficulty ',
                           [('1 - Easy', 'EASY'),
                            ('2 - Medium', 'MEDIUM'),
                            ('3 - Hard', 'HARD')],
                           onchange=change_difficulty,
                           selector_id='select_difficulty')
    play_menu.add_selector('Online',
                           [('True', 'first'),
                            ('False', 'last')],
                           onchange=change_online,
                           selector_id='online_mode')
    play_menu.add_button('Return to main menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus:About
    # -------------------------------------------------------------------------
    about_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    about_theme.widget_margin = (0, 0)

    about_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        theme=about_theme,
        title='About',
        width=WINDOW_SIZE[0] * 0.6
    )

    for m in ABOUT:
        about_menu.add_label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
    Pressound()
    about_menu.add_label('')
    about_menu.add_button('Return to menu', pygame_menu.events.BACK)
    options_theme = pygame_menu.themes.THEME_DARK.copy()
    options_theme.widget_margin = (0, 0)

    options_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        theme=options_theme,
        title='Options',
        width=WINDOW_SIZE[0] * 0.6
    )
    Pressound()
    options_menu.add_selector('Fullscreen',
                        [('True', 'first'),
                        ('False', 'last')],
                        onchange=change_fullscreen,
                        selector_id='fullscreen_mode')
    options_menu.add_label('')
    options_menu.add_button('Return to menu', pygame_menu.events.BACK)
    # -------------------------------------------------------------------------
    # Create menus: Main
    # -------------------------------------------------------------------------
    main_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    main_theme.menubar_close_button = False  # Disable close button

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        theme=main_theme,
        title='Main Menu',
        width=WINDOW_SIZE[0] * 0.6
    )

    main_menu.add_button('Play', play_menu)
    main_menu.add_button('About', about_menu)
    main_menu.add_button('Options', options_menu)
    main_menu.add_button('Quit', pygame_menu.events.EXIT)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break
        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break
        
def mainFrench(test=False):
    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global clock
    global main_menu
    global surface

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('SERPANT (tres original)')
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus: Play Menu
    # -------------------------------------------------------------------------
    play_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        title='Menu du jeu',
        width=WINDOW_SIZE[0] * 0.75
    )

    submenu_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    submenu_theme.widget_font_size = 15
    play_submenu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.5,
        theme=submenu_theme,
        title='Submenu',
        width=WINDOW_SIZE[0] * 0.7
    )
    for i in range(30):
        play_submenu.add_button('Back {0}'.format(i), pygame_menu.events.BACK)
    play_submenu.add_button('Retourner au menu pricipal', pygame_menu.events.RESET)
    Pressound()
    play_menu.add_button('Jouer',  # When pressing return -> play(DIFFICULTY[0], font)
                         play_functionenglish,
                         DIFFICULTY,
                         pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
    play_menu.add_text_input(
        "Nom d'utilisateur: ",
        default='UwU',
        onreturn=usernamedefiner,
        textinput_id='Username'
    )
    play_menu.add_selector('Select difficulty ',
                           [('1 - Facile', 'EASY'),
                            ('2 - Moyen', 'MEDIUM'),
                            ('3 - Difficile', 'HARD')],
                           onchange=change_difficulty,
                           selector_id='select_difficulty')
    play_menu.add_selector('Online ',
                           [('Vrai', 'first'),
                            ('False', 'last')],
                           onchange=change_online,
                           selector_id='online_mode')
    play_menu.add_button('Return to main menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus:About
    # -------------------------------------------------------------------------
    about_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    about_theme.widget_margin = (0, 0)

    about_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        theme=about_theme,
        title='A propos',
        width=WINDOW_SIZE[0] * 0.6
    )

    for m in ABOUT:
        about_menu.add_label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
    Pressound()
    about_menu.add_label('')
    about_menu.add_button('retourner au menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: Main
    # -------------------------------------------------------------------------
    main_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    main_theme.menubar_close_button = False  # Disable close button

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        theme=main_theme,
        title='Menu pricipal',
        width=WINDOW_SIZE[0] * 0.6
    )

    main_menu.add_button('Jouer', play_menu)
    main_menu.add_button('A propos', about_menu)
    main_menu.add_button('Quiter', pygame_menu.events.EXIT)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break
        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break
menu = pygame_menu.Menu(
    height=400,
    theme=pygame_menu.themes.THEME_DARK,
    title='Welcome',
    width=600
)
# def mainSecret():
#     print()
menu.add_button('English', mainEnglish)
menu.add_button('Français', mainFrench)
# menu.add_button('VARIABLES', mainSecret)
menu.add_button('Quit', pygame_menu.events.EXIT)
pygame.display.set_caption('Selecting language')


surface = pygame.display.set_mode((600, 400))
if __name__ == '__main__':
    menu.mainloop(surface)