from os import path
import time
import pygame

# colors
BACKGROUND = (186, 212, 206)  # blue-ish background
LINE_COLOR = (0, 0, 0)  # black lines
NUM_COLOR = (249, 180, 171)  # pink numbers
FILL_COLOR = (38, 78, 112)  # dark blue; when number is filled

WIDTH = 40
HEIGHT = 40
MARGIN = 5

empty = [[0 for x in range(9)] for y in range(9)]
orig_grid = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
solving_grid = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
solved_grid = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

def draw_board_lines(screen):
    # draw Grid Lines
    gap = screen.get_rect().width / 9
    for i in range(10):
        if i % 3 == 0 and i != 0:
            thick = 4
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * gap), (screen.get_rect().width, i * gap), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * gap, 0), (i * gap, screen.get_rect().height), thick)

def fill_board(screen, grid):
    for row in range(9):
        for column in range(9):
            if grid[row][column] == 0:
                continue  # do not print zeros
            if empty[row][column] == 1:
                color = (64, 120, 183)
            else:
                color = FILL_COLOR
            v = font.render(str(grid[row][column]), False, NUM_COLOR)
            cube = pygame.draw.rect(screen,
                                    color,
                                    [(screen.get_rect().width / 9) * column,
                                     (screen.get_rect().height / 9) * row,
                                     (screen.get_rect().width / 9),
                                     (screen.get_rect().height / 9)])
            screen.blit(v, (cube.centerx - 5, cube.centery - 14))

"""
BUTTON
"""
class Button():
    def __init__(self, x, y, image, window):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.window = window
        self.clicked = False

    def draw(self, window):
        p = pygame.mouse.get_pos()
        if self.rect.collidepoint(p):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button onto screen
        window.blit(self.image, (self.rect.x, self.rect.y))


"""
SOLVER
"""

def solve(board):
    # base case
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False


def valid(board, num, pos):
    # check row (pos[0] = row, pos[1] = col)
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None

def check():
    solve(solved_grid)
    for row in range(9):
        for column in range(9):
            if solving_grid[row][column] == solved_grid[row][column]:
                empty[row][column] = 0
            else:
                empty[row][column] = 1

pygame.init()

WINDOW_SIZE = [700, 650]
screen = pygame.display.set_mode(WINDOW_SIZE)
grid_space = pygame.Surface((420, 420))
grid_rect = grid_space.get_rect()

# fonts
font = pygame.font.Font(path.join('Attack Of Monster.ttf'), size=27)  # for numbers
pix_font = pygame.font.Font(path.join('Attack Of Monster.ttf'), size=25)  # for timer

# load in images for buttons
check_img = pygame.image.load(path.join('sprites', 'check.png')).convert_alpha()
reset_img = pygame.image.load(path.join('sprites', 'reset.png')).convert_alpha()
solve_img = pygame.image.load(path.join('sprites', 'solve.png')).convert_alpha()

# create buttons from Button class
check_button = Button(570, 150, check_img, screen)
reset_button = Button(570, 250, reset_img, screen)
solve_button = Button(570, 350, solve_img, screen)

pygame.display.set_caption("funky sudoku")

done = False
pos = (0, 0)
input = False
val = 0

"""
MAIN LOOP
"""

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # change x/y screen coordinates to grid coordinates
            col = (pos[0] - 100) // (WIDTH + MARGIN)
            r = (pos[1] - 100) // (HEIGHT + MARGIN)
            if r <= 8 and col <= 8:
                empty[r][col] = 1
                print("Click ", pos, "Grid coordinates: ", r, col)
            fill_board(grid_space, solving_grid)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                val = 1
            if event.key == pygame.K_2:
                val = 2
            if event.key == pygame.K_3:
                val = 3
            if event.key == pygame.K_4:
                val = 4
            if event.key == pygame.K_5:
                val = 5
            if event.key == pygame.K_6:
                val = 6
            if event.key == pygame.K_7:
                val = 7
            if event.key == pygame.K_8:
                val = 8
            if event.key == pygame.K_9:
                val = 9
            if event.key == pygame.K_RETURN:
                pos = pygame.mouse.get_pos()
                col = (pos[0] - 100) // (WIDTH + MARGIN)
                r = (pos[1] - 100) // (HEIGHT + MARGIN)
                if r <= 8 and col <= 8:
                    solving_grid[r][col] = val

    check_button.draw(screen)
    reset_button.draw(screen)
    solve_button.draw(screen)
    pygame.display.update()

    if check_button.clicked:
        check()
        check_button.clicked = False

    if solve_button.clicked:
        solving_grid = solved_grid
        solve_button.clicked = False

    if reset_button.clicked:
        empty = [[0 for x in range(9)] for y in range(9)]
        solving_grid = orig_grid
        reset_button.clicked = False
        time.sleep(0.05)

    screen.fill(BACKGROUND)
    grid_space.fill(BACKGROUND)
    value = font.render("", True, BACKGROUND)

    # draw the grid
    fill_board(grid_space, solving_grid)
    draw_board_lines(grid_space)
    screen.blit(grid_space, (100, 100))

pygame.quit()
