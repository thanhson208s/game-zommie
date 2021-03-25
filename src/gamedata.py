import pygame, math, time, json, random, subprocess
import constants, config
from ui import *
from sound import *

class GameManager:
    _instance = None
    STATE_READY = 0
    STATE_RUN = 1
    STATE_WIN = 2
    STATE_LOSE = 3
    STATE_PAUSE = 4

    def __init__(self):
        self.state = None
        self.zombieConfig = None
        self.obstacleConfig = None
        self.point = None
        self.remainTime = None
        self.numShot = None
        self.numHit = None
        self.numMiss = None
        self.bullets = None

        self.numShow = None
        self.zomSpawnTimer = None

    def initGame(self):
        try:
            json_file = open('/Users/lap14008/Programming/Game Programming/zommie/conf/zombies.json')
        except:
            print('No zombie config')
            exit()
        data = json.load(json_file)
        self.zombieConfig = []
        for item in data:
            self.zombieConfig.append(Zombie(item["id"], item["scale"], item["zOrder"], item["point"], item["startPos"], item["endPos"], item["startRotate"], item["endRotate"]))

        try:
            json_file = open('/Users/lap14008/Programming/Game Programming/zommie/conf/obstacles.json')
        except:
            print('No obstacle config')
            exit()
        data = json.load(json_file)
        self.obstacleConfig = []
        for item in data:
            self.obstacleConfig.append(Obstacle(item["path"], item["scale"], item["zOrder"], item["pos"], item["rotate"]))

        UIManager.instance().initGame(self.zombieConfig, self.obstacleConfig, self)

        self.resetGame()

    def resetGame(self):
        self.state = GameManager.STATE_READY
        self.point = 0
        self.remainTime = config.TOTAL_TIME * 1000
        self.numShot = 0
        self.numHit = 0
        self.numMiss = 0
        self.bullets = config.TOTAL_BULLET

        UIManager.instance().resetGame(self.zombieConfig)

    def startGame(self):
        self.state = GameManager.STATE_RUN
        self.numShow = 0
        for zom in self.zombieConfig:
            zom.startGame()

        self.zomSpawnTimer = 0

        UIManager.instance().startGame(self.zombieConfig)

    def stopGame(self):
        if self.state == GameManager.STATE_RUN:
            if self.point >= config.REQUIRED_POINT:
                self.state = GameManager.STATE_WIN
                soundManager.playWin()
            else:
                self.state = GameManager.STATE_LOSE
                soundManager.playLose()
        
            UIManager.instance().stopGame()

    def instance():
        if GameManager._instance is None:
            GameManager._instance = GameManager()
        return GameManager._instance

    def update(self, dt):
        if self.state == GameManager.STATE_RUN:
            self.zomSpawnTimer += dt
            if self.zomSpawnTimer >= config.SPAWN_DURATION * 1000:
                self.zomSpawnTimer -= config.SPAWN_DURATION * 1000
                self.spawnZom()
            self.remainTime -= dt
            if self.remainTime <= 0:
                self.remainTime = 0
                print("Out of time!")
                self.stopGame()
            UIManager.instance().setTime(self.remainTime)
        
        UIManager.instance().update(dt)

    def spawnZom(self):
        rate = 0
        if self.numShow < config.MIN_ZOM:
            rate = 0.9
        elif self.numShow < config.MAX_ZOM:
            rate = 0.5
        elif self.numShow < len(self.zombieConfig):
            rate = 0.1
        else:
            rate = 0
        if rate != 0 and rate > random.random():
            availableZom = [zom for zom in self.zombieConfig if zom.state == Zombie.STATE_HIDE]
            zom = random.choice(availableZom)
            zom.state = Zombie.STATE_SHOW
            zom.isShot = False
            self.numShow += 1
            UIManager.instance().showZom(zom)

    def onZomHide(self, id):
        for zom in self.zombieConfig:
            if zom.id == id:
                zom.state = Zombie.STATE_HIDE
                self.numShow -= 1
                if not zom.isShot:
                    self.bullets -= 1
                    UIManager.instance().effectSubBullet(1)
                    if self.bullets <= 0:
                        self.bullets = 0
                        print("Out of bullets!")
                        self.stopGame() 
                    UIManager.instance().setBullet(self.bullets)
                break

    def onShot(self, hit, id, pos):
        self.numShot += 1
        self.bullets -= 1

        zom = None
        if self.bullets == 0:
            print("Out of bullets!")
            self.stopGame()
        if hit:
            zom = self.getZomById(id)
            if not zom.isShot:
                zom.isShot = True
                hit = True
            else:
                hit = False
        else:
            hit = False
        if hit:
            self.bullets += config.BONUS_HIT
            self.numHit += 1
            self.point += zom.point
            UIManager.instance().onHit(zom, pos)
            UIManager.instance().setHit(self.numHit)
            UIManager.instance().setPoint(self.point)
            UIManager.instance().effectAddBullet(config.BONUS_HIT)
        else:
            self.bullets -= config.BONUS_MISS
            if self.bullets <= 0:
                self.bullets = 0
                print("Out of bullets!")
                self.stopGame()
            self.numMiss += 1
            UIManager.instance().onMiss(pos)
            UIManager.instance().setMiss(self.numMiss)
            UIManager.instance().effectSubBullet(config.BONUS_MISS)

        UIManager.instance().setBullet(self.bullets)

    def getZomById(self, id):
        for zom in self.zombieConfig:
            if zom.id == id:
                return zom
        return None

    def isRunning(self):
        return self.state == GameManager.STATE_RUN

    def isWin(self):
        return self.state == GameManager.STATE_WIN

    def getProgress(self):
        return self.remainTime / (config.TOTAL_TIME * 1000)
    
class Zombie:
    STATE_HIDE = 0
    STATE_SHOW = 1

    def __init__(self, id, scale, zOrder, point, startPos, endPos, startRotate, endRotate):
        self.id = id
        self.scale = scale
        self.zOrder = zOrder
        self.point = point
        self.startPos = pygame.math.Vector2(startPos)
        self.endPos = pygame.math.Vector2(endPos)
        self.startRotate = startRotate
        self.endRotate = endRotate

        self.state = -1

    def startGame(self):
        self.state = Zombie.STATE_HIDE
        self.isShot = False

class Obstacle:
    def __init__(self, path, scale, zOrder, pos, rotate):
        self.path = path
        self.scale = scale
        self.zOrder = zOrder
        self.pos = pygame.math.Vector2(pos)
        self.rotate = rotate