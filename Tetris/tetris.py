import pygame
import random
import sys
import json
import os

pygame.init()

# --- KONSTANTY ---
ROWS, COLS = 20, 10
FPS = 60
RESOLUTIONS = [(300, 640), (400, 840), (600, 1240), (1920, 1080)]

BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
MENU_BG = (30, 30, 30)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER = (100, 100, 100)

COLORS = [
    (0, 255, 255),
    (0, 0, 255),
    (255, 165, 0),
    (255, 255, 0),
    (0, 255, 0),
    (128, 0, 128),
    (255, 0, 0),
]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]]
]

# --- absolutní cesta pro highscore, funguje i u exe ---
HIGHSCORE_FILE = os.path.join(os.path.dirname(sys.argv[0]), "highscores.json")

# --- FUNKCE PRO HIGHSCORE ---
def load_highscores():
    if not os.path.exists(HIGHSCORE_FILE):
        return {}
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_highscores(scores):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(scores, f, indent=4)

# --- FUNKCE PRO ZADÁNÍ JMÉNA ---
def ask_name(screen, width, height):
    font = pygame.font.SysFont("arial", 36)
    name = ""
    input_active = True
    clock = pygame.time.Clock()
    while input_active:
        screen.fill(MENU_BG)
        text_surface = font.render("Zadej své jméno: " + name, True, WHITE)
        rect = text_surface.get_rect(center=(width//2, height//2))
        screen.blit(text_surface, rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12 and event.unicode.isalnum():
                    name += event.unicode
        clock.tick(60)
    return name

# --- TŘÍDY A FUNKCE PRO KOSTKY ---
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0
    def image(self):
        return self.shape[self.rotation % len(self.shape)]
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

def new_piece():
    shape = random.choice(SHAPES)
    rotations = [shape]
    for _ in range(3):
        shape = list(zip(*shape[::-1]))
        rotations.append([list(row) for row in shape])
    return Piece(3, 0, rotations)

def valid_space(piece, grid):
    shape = piece.image()
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                new_x = piece.x + j
                new_y = piece.y + i
                if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                    return False
                if new_y >= 0 and grid[new_y][new_x] != BLACK:
                    return False
    return True

def place_piece(piece, grid):
    shape = piece.image()
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                grid[piece.y + i][piece.x + j] = piece.color

def clear_rows(grid):
    full_rows = [i for i, row in enumerate(grid) if all(cell != BLACK for cell in row)]
    for i in full_rows:
        del grid[i]
        grid.insert(0, [BLACK for _ in range(COLS)])
    return len(full_rows)

# --- KRESLENÍ ---
def draw_grid(screen, grid, block_size, offset_x, offset_y):
    for i in range(ROWS):
        for j in range(COLS):
            rect = (offset_x + j*block_size, offset_y + i*block_size, block_size, block_size)
            pygame.draw.rect(screen, grid[i][j], rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_text(screen, text, size, color, x, y, center=True):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, True, color)
    rect = label.get_rect(center=(x,y)) if center else label.get_rect(topleft=(x,y))
    screen.blit(label, rect)
    return rect

def button(screen, text, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    color = BUTTON_HOVER if (x<mouse[0]<x+w and y<mouse[1]<y+h) else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x,y,w,h), border_radius=10)
    draw_text(screen, text, 24, WHITE, x+w//2, y+h//2)
    if click and (x<mouse[0]<x+w and y<mouse[1]<y+h):
        if action:
            pygame.time.wait(150)
            action()

# --- HRA ---
def play_game(screen, width, height, fullscreen=False):
    board_height = height - 100
    block_size = board_height // ROWS
    board_width = block_size * COLS
    offset_x = (width - board_width)//2
    offset_y = 60

    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    current_piece = new_piece()
    next_piece = new_piece()

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.6
    score = 0
    move_cooldown = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        fall_time += dt
        move_cooldown += dt

        keys = pygame.key.get_pressed()
        # horizontální pohyb WSAD + šipky
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if move_cooldown>120:
                current_piece.x -= 1
                if not valid_space(current_piece, grid): current_piece.x +=1
                move_cooldown=0
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if move_cooldown>120:
                current_piece.x += 1
                if not valid_space(current_piece, grid): current_piece.x -=1
                move_cooldown=0
        # pád
        speed_factor = 0.1 if keys[pygame.K_DOWN] or keys[pygame.K_s] else 1.0
        if fall_time/1000 >= fall_speed*speed_factor:
            fall_time=0
            current_piece.y+=1
            if not valid_space(current_piece, grid):
                current_piece.y-=1
                place_piece(current_piece, grid)
                score += clear_rows(grid)*100
                current_piece = next_piece
                next_piece = new_piece()
                if not valid_space(current_piece, grid):
                    # game over → jméno + návrat do menu
                    name = ask_name(screen, width, height)
                    highscores = load_highscores()
                    if name in highscores:
                        if score > highscores[name]:
                            highscores[name] = score
                    else:
                        highscores[name] = score
                    save_highscores(highscores)
                    return

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_r:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotation-=1
                elif event.key==pygame.K_ESCAPE:
                    return

        # zrychlování po každých 1000 bodech
        fall_speed = max(0.1, 0.6 - (score // 1000) * 0.05)

        # kreslení
        screen.fill(GRAY)
        draw_text(screen, f"Score: {score}", 26, WHITE, offset_x, 20, center=False)
        temp_grid = [row[:] for row in grid]
        shape = current_piece.image()
        for i,row in enumerate(shape):
            for j,cell in enumerate(row):
                if cell:
                    x=current_piece.x+j
                    y=current_piece.y+i
                    if y>=0:
                        temp_grid[y][x]=current_piece.color
        draw_grid(screen,temp_grid,block_size,offset_x,offset_y)
        pygame.display.update()

# --- MENU ---
def main_menu():
    current_res=0
    fullscreen=False
    width,height=RESOLUTIONS[current_res]
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Tetris")
    clock=pygame.time.Clock()
    state="menu"

    def start_game(): nonlocal state; state="play"
    def open_settings(): nonlocal state; state="settings"
    def go_back(): nonlocal state; state="menu"

    running=True
    while running:
        screen.fill(MENU_BG)
        clock.tick(60)

        if state=="menu":
            draw_text(screen,"TETRIS",54,WHITE,width//2,150)
            button(screen,"HRÁT",width//2-90,320,180,60,start_game)
            button(screen,"NASTAVENÍ",width//2-90,410,180,60,open_settings)
            button(screen,"KONEC",width//2-90,500,180,60,pygame.quit)
        elif state=="settings":
            draw_text(screen,"NASTAVENÍ",42,WHITE,width//2,120)
            draw_text(screen,"Rozlišení:",28,WHITE,width//2,220)
            for i,res in enumerate(RESOLUTIONS):
                color=WHITE if i==current_res else (180,180,180)
                rect=draw_text(screen,f"{res[0]}x{res[1]}",26,color,width//2,270+i*40)
                if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    current_res=i
                    width,height=RESOLUTIONS[current_res]
                    flags=pygame.FULLSCREEN if fullscreen else 0
                    screen=pygame.display.set_mode((width,height),flags)
                    pygame.time.wait(150)
            draw_text(screen,"Fullscreen:",28,WHITE,width//2,420)
            rect=draw_text(screen,"ZAP" if fullscreen else "VYP",26,(0,255,0) if fullscreen else (200,80,80),width//2,460)
            if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                fullscreen=not fullscreen
                flags=pygame.FULLSCREEN if fullscreen else 0
                screen=pygame.display.set_mode((width,height),flags)
                pygame.time.wait(150)
            button(screen,"ZPĚT",width//2-80,550,160,50,go_back)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False

        if state=="play":
            play_game(screen,width,height,fullscreen)
            state="menu"

    pygame.quit()

if __name__=="__main__":
    main_menu()
