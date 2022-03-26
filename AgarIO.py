import pygame
import random
import math
# Dimension Definitions
SCREEN_WIDTH, SCREEN_HEIGHT = (800,500)
PLATFORM_WIDTH, PLATFORM_HEIGHT = (3000,3000)


NAME = "Agar.io"
VERSION = "1.0"

# Pygame initialization
pygame.init()
pygame.display.set_caption("{} - v{}".format(NAME, VERSION))
clock = pygame.time.Clock()

font = pygame.font.SysFont('Ubuntu',20,True)

big_font = pygame.font.SysFont('Ubuntu',24,True)

# Surface Definitions
MAIN_SURFACE = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
# Surface((width, height), flags=0, depth=0, masks=None) -> Surface
SCOREBOARD_SURFACE = pygame.Surface((95,25),pygame.SRCALPHA)
LEADERBOARD_SURFACE = pygame.Surface((155,278),pygame.SRCALPHA)


def getDistance(a, b):
    """ Определяет расстояние между двумя точками
    """
    diffX = math.fabs(a[0]-b[0])
    diffY = math.fabs(a[1]-b[1])
    return ((diffX**2)+(diffY**2))**(0.5)


# def drawText(message,pos,color=(255,255,255)):
#     """ Отрисовка текста на мэйн
#     """
#     MAIN_SURFACE.blit(font.render(message,1,color),pos)


class Paint:
    def __init__(self):
        self.paintings = []

    def add(self, col):
        self.paintings.append(col)

    def paint(self):
        for draw_elem in self.paintings:
            draw_elem.draw()


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.H = SCREEN_HEIGHT
        self.W = SCREEN_WIDTH
        self.zoom = 0.5

    def centre(self,blobOrPos):
        """Makes sure that the given object will be at the center of player's view.
        Zoom is taken into account as well.
        """
        if isinstance(blobOrPos, Player):
            x, y = blobOrPos.x, blobOrPos.y
            self.x = (x - (x*self.zoom)) - x + (SCREEN_WIDTH/2)
            self.y = (y - (y*self.zoom)) - y + (SCREEN_HEIGHT/2)
        elif type(blobOrPos) == tuple:
            self.x, self.y = blobOrPos


    def update(self, target):
        self.zoom = 100/(target.mass)+0.3
        self.centre(player)


class Drawable:
    """Абстрактный класс для объединения дочерних классов в единый интерфейс
    """

    def __init__(self, surface, camera):
        self.surface = surface
        self.camera = camera

    def draw(self):
        pass


class Grid(Drawable):
    """Показывает сетку
    """

    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.color = (255,255,255)

    def draw(self):
        # A grid is a set of horizontal and prependicular lines
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        for i in range(0,2001,25):
            pygame.draw.line(self.surface,  self.color, (x, i*zoom + y), (2001*zoom + x, i*zoom + y), 2)
            pygame.draw.line(self.surface, self.color, (i*zoom + x, y), (i*zoom + x, 2001*zoom + y), 2)


class Cell(Drawable): # Ячейка массы
    """Used to represent the fundamental entity of game.
    A cell can be considered as a quantom of mass.
    It can be eaten by other entities.
    """
    CELL_COLORS = [
    (80,252,54),
    (36,244,255),
    (243,31,46),
    (4,39,243),
    (254,6,178),
    (255,211,7),
    (216,6,254),
    (145,255,7),
    (7,255,182),
    (255,6,86),
    (147,7,255),
    (255, 210, 210)]

    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.x = random.randint(20,1980)
        self.y = random.randint(20,1980)
        self.mass = 7
        self.color = random.choice(Cell.CELL_COLORS)

    def draw(self):
        """Draws a cell as a simple circle.
        """
        zoom = self.camera.zoom
        x,y = self.camera.x, self.camera.y
        center = (int(self.x*zoom + x), int(self.y*zoom + y))
        pygame.draw.circle(self.surface, self.color, center, int(self.mass*zoom))


class CellList(Drawable):
    """Для котнроля частиц и их количества на экране
    """

    def __init__(self, surface, camera, numOfCells):
        super().__init__(surface, camera)
        self.count = numOfCells
        self.list = []
        for i in range(self.count):
            self.list.append(Cell(self.surface, self.camera))

    def draw(self):
        for cell in self.list:
            cell.draw()


# Инициализация сущностей (камера, сетка, ячейки, и т.д.)
cam = Camera()

grid = Grid(MAIN_SURFACE, cam)
cells = CellList(MAIN_SURFACE, cam, 1500)
player = Player(MAIN_SURFACE, cam)

# Отрисовка
painter = Paint()

# Добавляем на полотно
painter.add(grid)
painter.add(cells)
painter.add(player)

if __name__ == '__main__':
    # Игровой цикл
    while True:
        clock.tick(80)  # Частота кадров не превышает 80

        # Проверка на действия (события) от игрока
        for event in pygame.event.get():
            if(event.type == pygame.KEYDOWN):
                # Закрытие программы
                if(event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()
                if(event.key == pygame.K_SPACE):
                    player.split()
                if(event.key == pygame.K_w):
                    player.feed()
                if(event.key == pygame.K_w):
                    player.speedrun()
            # Закрытие программы
            if(event.type == pygame.QUIT):
                pygame.quit()
                quit()

        player.move()
        player.collisionDetection(cells.list)
        cam.update(player)
        MAIN_SURFACE.fill((40,40,40))
        painter.paint()
        # Start calculating next frame
        pygame.display.flip()