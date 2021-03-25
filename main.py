import sys, pygame, math, subprocess, time

sys.path.insert(1, 'src/')
import constants, config
from gamedata import *
from ui import *
from sound import *

pygame.init()
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
pygame.display.set_caption("Zommie 1.0")
# === GLOBAL OBJECTS === #
clock = pygame.time.Clock()

screen = pygame.display.set_mode(config.SIZE, flags=pygame.SCALED|pygame.RESIZABLE)
gameManager = GameManager.instance()
uiManager = UIManager.instance()
# === GLOBAL OBJECTS === #

# === Init global data === #
running = True
timer = 0
# === Init global data === #

# === Utilities === #

# === Utilities === #

# === Game Scene === #
def initGameScene():

    #add layer color
    menuBg = LayerColor(constants.BLACK, config.WIDTH, config.HEIGHT)
    uiManager.addNode(menuBg, 10)
    menuBg.opacity = 150
# === Game Scene === #

# === main loop === #
gameManager.initGame()
soundManager.playTheme()
while running:
    clock.tick(60)
    screen.fill(constants.WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type in [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
            uiManager.onMouseEvent(event.type, pygame.mouse)

    timer += clock.get_time()
    while timer >= config.FRAME_TIME:
        gameManager.update(config.FRAME_TIME)
        timer -= config.FRAME_TIME

    uiManager.draw(screen)
    pygame.display.flip()