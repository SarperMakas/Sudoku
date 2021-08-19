"""Sudoku Game"""
import pygame, ctypes, numpy as np, random


class Sudoku:
    """Sudoku Class For Game"""
    def __init__(self):
        """Initialize game and pygame"""
        pygame.init()
        # define sqSize, sqNumber and gap
        self.sqNumber = 9
        self.user = ctypes.windll.user32
        self.sqSize = int(self.user.GetSystemMetrics(0)/20)
        self.gap = int(self.user.GetSystemMetrics(0)/100)

        # define width, height and screen
        self.SIZE = self.sqNumber * self.sqSize + self.gap*4
        self.screen = pygame.display.set_mode((self.SIZE, self.SIZE))
        pygame.display.set_caption("Sudoku")

        # font and text
        self.fontSize = self.SIZE
        self.font = pygame.font.Font("Roboto-Bold.ttf", 22)
        self.text = None

        # clock, running and FPS
        self.FPS = 30
        self.running = True
        self.clock = pygame.time.Clock()

        # colors
        self.bgColor = [70 for _ in range(3)]
        self.SqColor = [180 for _ in range(3)]
        self.borderColors = [[self.bgColor for _ in range(9)] for _ in range(9)]
        self.hover = [255, 0, 0]

        self.fontColor = np.full((9, 9), 110)

        # click
        self.isClick = False
        self.pos = []

        # row, cols, x, y and rect
        self.row = self.col = self.x = self.y = 0
        self.colGap = self.rowGap = 1
        self.rect = None

        # sudoku
        self.limit = 35
        self.unable = []
        self.sudoku = self.GenerateSudoku()
        self.table = self.deleteSqs()

    def GenerateSudoku(self):
        """Generate Sudoku"""
        sudoku = np.full((9, 9), 0)
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # generate first line
        for col in range(self.sqNumber):
            num = random.choice(numbers)
            sudoku[0, col] = num
            numbers.remove(num)
        # numbers
        nums = [[1, 0, 3, 0, 3, 6], [1, 3, 6, 0, 6, 10], [1, 6, 10, 0, 0, 3],
                [2, 0, 3, 1, 3, 6], [2, 3, 6, 1, 6, 10], [2, 6, 10, 1, 0, 3],]
        # use for loop
        for num in nums:
            sudoku[num[0], num[1]:num[2]] = sudoku[num[3], num[4]: num[5]]
        # numbers
        nums = [[3, 6, 0, 0, 3, 1], [3, 6, 1, 0, 3, 2], [3, 6, 2, 0, 3, 0],
                [3, 6, 3, 0, 3, 4], [3, 6, 4, 0, 3, 5], [3, 6, 5, 0, 3, 3],
                [3, 6, 6, 0, 3, 7], [3, 6, 7, 0, 3, 8], [3, 6, 8, 0, 3, 6],

                [6, 10, 0, 3, 6, 1], [6, 10, 1, 3, 6, 2], [6, 10, 2, 3, 6, 0],
                [6, 10, 3, 3, 6, 4], [6, 10, 4, 3, 6, 5], [6, 10, 5, 3, 6, 3],
                [6, 10, 6, 3, 6, 7], [6, 10, 7, 3, 6, 8], [6, 10, 8, 3, 6, 6]]
        # use for loop
        for num in nums:
            sudoku[num[0]:num[1], num[2]] = sudoku[num[3]:num[4], num[5]]

        return sudoku

    def deleteSqs(self):
        """deleting some sqs from the sudoku table"""
        sudoku = self.sudoku.copy()
        num = 81
        while num > self.limit:
            num = 0
            # generate row and col
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            # count 0's
            sudoku[row, col] = 0
            for row in range(self.sqNumber):
                for col in range(self.sqNumber):
                    if sudoku[row, col] != 0: num += 1

        # check unable numbers
        for row in range(self.sqNumber):
            for col in range(self.sqNumber):
                if sudoku[row, col] != 0:
                    self.unable.append([row, col])
                    self.fontColor[row, col] = 60

        return sudoku

    def click(self, rect):
        """Check user click"""
        x, y = pygame.mouse.get_pos()
        if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom and self.isClick is True:
            self.borderColors = [[self.bgColor for _ in range(9)] for _ in range(9)]
            self.pos = [self.row, self.col, self.rect]

    def Generate(self):
        """generate x, y and rect"""
        # defining x, y and rects
        self.x = self.col * self.sqSize + self.gap * self.colGap
        self.y = self.row * self.sqSize + self.gap * self.rowGap
        self.rect = pygame.rect.Rect((self.x, self.y), (self.sqSize, self.sqSize))
        # create texts
        if self.table[self.row, self.col] != 0:
            self.text = self.font.render(f"{self.table[self.row, self.col]}", True,  [self.fontColor[self.row, self.col]]*3)
        else:
            self.text = self.font.render("", True, [self.fontColor[self.row, self.col]]*3)

    def drawGrids(self):
        """drawing grids"""
        # col => x, row => y
        self.rowGap = 1
        for self.row in range(self.sqNumber):
            self.colGap = 1
            for self.col in range(self.sqNumber):
                self.Generate()
                # drawing rects
                pygame.draw.rect(self.screen, self.SqColor, self.rect)
                pygame.draw.rect(self.screen, self.borderColors[self.row][self.col], self.rect, width=3)
                rect = self.text.get_rect(center=self.rect.center)
                self.click(self.rect)
                self.screen.blit(self.text, rect)


                # increase col gap
                if self.col + 1 == 3 or self.col + 1 == 6:
                    self.colGap += 1
            # increase row gap
            if self.row + 1 == 3 or self.row + 1 == 6:
                self.rowGap += 1

    def drawHover(self):
        """drawing hover effect"""
        try:
            # create the rect and draw width again
            self.rect = pygame.rect.Rect((self.pos[2].x, self.pos[2].y), (self.sqSize, self.sqSize))
            pygame.draw.rect(self.screen, self.hover, self.rect, width=3)
        except IndexError:
            pass

    def press(self, value):
        """check key presses"""
        numList = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
        numDict = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6,
                   pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9}
        # write to screen
        if value in numList and [self.pos[0], self.pos[1]] not in self.unable:
            self.table[self.pos[0], self.pos[1]] = numDict[value]
        elif value == pygame.K_SPACE:
            self.check()

    def check(self):
        """check sudoku if the user did correct"""
        for row in range(self.sqNumber):
            for col in range(self.sqNumber):
                # check if the user did correct
                if self.sudoku[row, col] == self.table[row, col]:
                    self.fontColor[row, col] = 255
                else:
                    self.fontColor[row, col] = 0
                    self.table[row, col] = self.sudoku[row, col]

    def event(self):
        """Event loop"""
        # event
        for event in pygame.event.get():
            # exit from game
            if event.type == pygame.QUIT:
                self.running = False
            # select
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.isClick = True
            else:
                self.isClick = False
            # writing
            if event.type == pygame.KEYDOWN:
                self.press(event.key)

    def run(self):
        """Main look of the game"""
        while self.running:
            # FPS
            self.clock.tick(self.FPS)
            self.event()  # events

            self.draw()  # drawing screen

    def draw(self):
        """Draw Game"""
        self.screen.fill(self.bgColor)
        self.drawGrids()
        self.drawHover()
        pygame.display.flip()


if __name__ == '__main__':
    """Start game"""
    Sudoku().run()
