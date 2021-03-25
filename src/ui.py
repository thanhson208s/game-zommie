import pygame, math, time, random, subprocess
import config, constants
from sound import *

class UIManager:
    _instance = None

    def __init__(self):
        self.nodes = []

    def addNode(self, node, zOrder=0, name=None):
        node.zOrder = zOrder
        if name is not None:
            node.name = name
        for i, e in enumerate(self.nodes):
            if e.zOrder > node.zOrder:
                self.nodes.insert(i, node)
                node.onEnter()
                return
        self.nodes.append(node)
        node.onEnter()

    def removeNode(self, node):
        self.nodes.remove(node)

    def getNode(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def draw(self, screen):
        for node in self.nodes:
            node.draw(screen)

    def onMouseEvent(self, eventType, mouse):
        hit = False
        zom = None
        for node in reversed(self.nodes):
            if node.onMouseEvent(eventType, mouse):
                if node.name is not None and 'zom' in node.name:
                    hit = True
                    zom = node
                break

        if eventType == pygame.MOUSEMOTION:
            shoot = self.getNode("shoot")
            pos = pygame.mouse.get_pos()
            shoot.x, shoot.y = pos[0], pos[1]
            shoot.setDirty()
        elif eventType == pygame.MOUSEBUTTONDOWN:
            soundManager.playShot()
            shoot = self.getNode("shoot")
            shoot.setSpriteFrame(self.redSpriteFrame)
            if self.gameManager.isRunning():
                self.gameManager.onShot(hit, int(zom.name[3:]) if hit else None, pygame.mouse.get_pos())
        elif eventType == pygame.MOUSEBUTTONUP:
            shoot = self.getNode("shoot")
            shoot.setSpriteFrame(self.greenSpriteFrame)

    def update(self, dt):
        for node in self.nodes:
            node.updateActions(dt)
            if node.scheduled:
                node.update(dt)
    
    def initGame(self, zombieConfig, obstacleConfig, gameManager):
        self.gameManager = gameManager

        for obs in obstacleConfig:
            sprite = Sprite(obs.path)
            sprite.scaleX = sprite.scaleY = obs.scale
            sprite.x, sprite.y = obs.pos.x, obs.pos.y
            sprite.rotate = obs.rotate
            self.addNode(sprite, obs.zOrder)

        for zom in zombieConfig:
            sprite = Sprite("res/zom/0.png")
            sprite.scaleX = sprite.scaleY = zom.scale
            self.addNode(sprite, zom.zOrder, "zom" + str(zom.id))

        hover = LayerColor(pygame.Color(255, 255, 255, 150), config.WIDTH, config.HEIGHT)
        self.addNode(hover, 10, "hover")

        shoot = Sprite("res/shoot/green.png", True)
        shoot.scaleX = shoot.scaleY = 0.03
        self.addNode(shoot, 100, "shoot")

        self.initMenu()
        self.initResource()
        self.initStat()

    def initMenu(self):
        def onButtonRelease(button, uiManager=self):
            if button.name == "btnPlay":
                self.gameManager.startGame()
            elif button.name == "btnBack":
                self.gameManager.resetGame()
            elif button.name == "btnQuit":
                confirmCode = subprocess.call("osascript -e '{}'".format('display dialog \"Stay with me senpai...\" with title \"Are you sure you want to quit?\"'), shell=True)
                if confirmCode == 0:
                    exit()

        btnPlay = Button("res/menu/btnPlay.png")
        btnPlay.x = config.WIDTH/2
        btnPlay.y = 950
        btnPlay.scaleX = btnPlay.scaleY = 0.25
        self.addNode(btnPlay, 20, "btnPlay")
        btnPlay.computeTransform()

        btnScore = Button("res/menu/btnScore.png")
        btnScore.x = config.WIDTH/2
        btnScore.y = 1200
        btnScore.scaleX = btnScore.scaleY = 0.25
        self.addNode(btnScore, 20, "btnScore")
        btnScore.computeTransform()

        btnQuit = Button("res/menu/btnQuit.png")
        btnQuit.x = config.WIDTH/2
        btnQuit.y = 1450
        btnQuit.scaleX = btnQuit.scaleY = 0.25
        self.addNode(btnQuit, 20, "btnQuit")
        btnQuit.computeTransform()

        btnBack = Button("res/menu/btnBack.png")
        btnBack.x = config.WIDTH/2
        btnBack.y = 1400
        btnBack.scaleX = btnBack.scaleY = 0.3
        self.addNode(btnBack, 20, "btnBack")
        btnBack.computeTransform()

        btnPlay.onMouseEnded = btnScore.onMouseEnded = btnQuit.onMouseEnded = btnBack.onMouseEnded = onButtonRelease

        title = Sprite("res/menu/title.png")
        title.x = config.WIDTH/2
        title.y = 500
        title.scaleX = title.scaleY = 0.6
        self.addNode(title, 20, "title")
        title.computeTransform()

        win = Sprite("res/menu/win.png")
        win.x = config.WIDTH/2
        win.y = 300
        win.scaleX = win.scaleY = 0.6
        self.addNode(win, 20, "win")
        win.computeTransform()

        lose = Sprite("res/menu/lose.png")
        lose.x = config.WIDTH/2
        lose.y = 200
        lose.scaleX = lose.scaleY = 0.6
        self.addNode(lose, 20, "lose")
        lose.computeTransform()

        credit = Sprite("res/menu/credit.png")
        credit.x = config.WIDTH/2
        credit.y = 850
        credit.scaleX = credit.scaleY = 0.5
        self.addNode(credit, 20, "credit")
        credit.computeTransform()

    def initStat(self): 
        point = Label("", "monspace", 60, constants.BLACK)
        point.x = config.WIDTH - 30
        point.y = 50
        point.anchorX, point.anchorY = 1, 0.5
        self.addNode(point, 0, "point")
        point.computeTransform()

        hit = Label("", "monspace", 60, constants.GREEN)
        hit.x = config.WIDTH - 30
        hit.y = 100
        hit.anchorX, hit.anchorY = 1, 0.5
        self.addNode(hit, 0, "hit")
        hit.computeTransform()

        miss = Label("", "monspace", 60, constants.RED)
        miss.x = config.WIDTH - 30
        miss.y = 150
        miss.anchorX, miss.anchorY = 1, 0.5
        self.addNode(miss, 0, "miss")
        miss.computeTransform()

        time = Label("", "monspace", 80, (252, 161, 3))
        time.x = 20
        time.y = 60
        time.anchorX, time.anchorY = 0, 0.5
        self.addNode(time, 0, "time")
        time.computeTransform()

        bulletImg = Sprite("res/effect/bullet.png", True)
        bulletImg.x = 24
        bulletImg.y = 130
        bulletImg.anchorX, bulletImg.anchorY = 0, 0.5
        bulletImg.scaleX, bulletImg.scaleY = 0.05, 0.05
        self.addNode(bulletImg, 0)
        bulletImg.computeTransform()

        bullet = Label("", "monspace", 70, constants.BLACK)
        bullet.x = 50
        bullet.y = 150
        bullet.anchorX, bullet.anchorY = 0, 0.5
        self.addNode(bullet, 0, "bullet")
        bullet.computeTransform()

    def initResource(self):
        self.zomAnimation = [pygame.Surface.convert_alpha(pygame.image.load("res/zom/" + str(i) + ".png")) for i in range(6)]
        self.zomAnimationRev = [pygame.Surface.convert_alpha(pygame.image.load("res/zom/" + str(i) + ".png")) for i in reversed(range(6))]
        self.zomDeadSpriteFrame = pygame.Surface.convert_alpha(pygame.image.load("res/zom/dead.png"))
        self.greenSpriteFrame = pygame.Surface.convert_alpha(pygame.image.load("res/shoot/green.png"))
        self.redSpriteFrame = pygame.Surface.convert_alpha(pygame.image.load("res/shoot/red.png"))
        self.bulletHoleSpriteFrame = pygame.Surface.convert_alpha(pygame.image.load("res/effect/hole.png"))
        self.missSpriteFrame = pygame.Surface.convert_alpha(pygame.image.load("res/effect/miss.png"))
        self.bloodAnimation = [pygame.Surface.convert_alpha(pygame.image.load("res/effect/" + str(i) + ".png")) for i in range(6)]

    def resetGame(self, zombieConfig):
        self.getNode('title').visible = True
        self.getNode('btnPlay').visible = True     
        self.getNode('btnScore').visible = True
        self.getNode('btnQuit').visible = True
        self.getNode('hover').visible = True
        self.getNode('lose').visible = False
        self.getNode('win').visible = False
        self.getNode('btnBack').visible = False
        self.getNode('credit').visible = False
        self.setPoint(0)
        self.setHit(0)
        self.setMiss(0)
        self.setTime(config.TOTAL_TIME * 1000)
        self.setBullet(config.TOTAL_BULLET)

        for zomData in zombieConfig:
            zom = self.getNode("zom" + str(zomData.id))
            zom.x, zom.y = zomData.startPos.x, zomData.startPos.y
            zom.rotate = zomData.startRotate
            zom.setDirty()
            zom.stopAllActions()
            zom.runAction(SequenceAction(
                DelayAction(4 + random.random() * 6),
                SpawnAction(
                    RotateToAction(0.15, zomData.endRotate),
                    MoveToAction(0.15, zomData.endPos.x, zomData.endPos.y),
                    SequenceAction(
                        DelayAction(0.15),
                        AnimateAction(0.2, self.zomAnimation)
                    )
                ),
                DelayAction(2 + random.random() * 2),
                SpawnAction(
                    AnimateAction(0.2, self.zomAnimationRev),
                    SequenceAction(
                        DelayAction(0.2),
                        SpawnAction(
                            RotateToAction(0.15, zomData.startRotate),
                            MoveToAction(0.15, zomData.startPos.x, zomData.startPos.y)
                        )
                    )
                ),
                MoveToAction(0.15, zomData.startPos.x, zomData.startPos.y),
                DelayAction(4 + random.random() * 6)
            ).repeatForever())

    def startGame(self, zombieConfig):
        self.getNode('title').visible = False
        self.getNode('btnPlay').visible = False     
        self.getNode('btnScore').visible = False
        self.getNode('btnQuit').visible = False
        self.getNode('hover').visible = False

        for zomData in zombieConfig:
            zom = self.getNode("zom" + str(zomData.id))
            zom.x, zom.y = zomData.startPos.x, zomData.startPos.y
            zom.rotate = zomData.startRotate
            zom.setDirty()
            zom.stopAllActions()

    def stopGame(self):
        self.getNode("hover").visible = True
        if self.gameManager.isWin():
            self.getNode("win").visible = True
        else:
            self.getNode("lose").visible = True
        self.getNode("btnBack").visible = True
        self.getNode("credit").visible = True

    def showZom(self, zomData):
        soundManager.playZom()
        zom = self.getNode("zom" + str(zomData.id))
        zom.x, zom.y = zomData.startPos.x, zomData.startPos.y
        zom.rotate = zomData.startRotate
        zom.setDirty()
        zom.stopAllActions()

        def callback(zom, gameManager=self.gameManager):
            gameManager.onZomHide(int(zom.name[3:]))
        zom.runAction(SequenceAction(
            SpawnAction(
                RotateToAction(0.15, zomData.endRotate),
                MoveToAction(0.15, zomData.endPos.x, zomData.endPos.y),
                SequenceAction(
                    DelayAction(0.15),
                    AnimateAction(0.2, self.zomAnimation)
                )
            ),
            DelayAction(0.5 + random.random() * (0.5 + 0.5 * self.gameManager.getProgress())),
            SpawnAction(
                AnimateAction(0.2, self.zomAnimationRev),
                SequenceAction(
                    DelayAction(0.2),
                    SpawnAction(
                        RotateToAction(0.15, zomData.startRotate),
                        MoveToAction(0.15, zomData.startPos.x, zomData.startPos.y)
                    )
                )
            ),
            CallAction(callback, zom)
        ))

    def onHit(self, zom, pos):
        # def onShot(sprite, gameManager=self.gameManager):
        #     print(sprite.name)
        #     zom = gameManager.getZomById(int(sprite.name[3:]))
        #     print(str(zom.id))
        #     if not zom.isShot:
        #         gameManager.onZomShot(zom.id)
        #         sprite.stopAllActions()
        #         sprite.x, sprite.y = zom.endPos.x, zom.endPos.y
        #         sprite.rotate = zom.endRotate
        #         sprite.setSpriteFrame(self.zomDeadSpriteFrame)
        #         sprite.setDirty()
        #         def callback(sprite=sprite, zom=zom, gameManager=gameManager):
        #             sprite.opacity = 255
        #             sprite.x, sprite.y = zom.startPos.x, zom.startPos.y
        #             sprite.rotate = zom.startRotate
        #             sprite.setDirty()
        #             gameManager.onZomHide(zom.id)
        #         sprite.runAction(SequenceAction(
        #             FadeOutAction(0.25),
        #             CallAction(callback)
        #         ))
        # sprite.onMouseBegan = onShot

        sprite = self.getNode("zom" + str(zom.id))
        sprite.stopAllActions()
        sprite.x, sprite.y = zom.endPos.x, zom.endPos.y
        sprite.rotate = zom.endRotate
        sprite.setSpriteFrame(self.zomDeadSpriteFrame)
        sprite.setDirty()
        def callback(sprite=sprite, zom=zom, gameManager=self.gameManager):
            sprite.opacity = 255
            sprite.x, sprite.y = zom.startPos.x, zom.startPos.y
            sprite.rotate = zom.startRotate
            sprite.setDirty()
            gameManager.onZomHide(zom.id)
        sprite.runAction(SequenceAction(
            FadeOutAction(0.5),
            CallAction(callback)
        ))

        hole = Sprite(self.bulletHoleSpriteFrame, True)
        hole.x = pos[0]
        hole.y = pos[1]
        hole.scaleX = sprite.scaleX * 0.8
        hole.scaleY = sprite.scaleY * 0.8
        hole.setDirty()
        self.addNode(hole, 50)
        hole.runAction(SequenceAction(
            FadeOutAction(0.75),
            RemoveSelfAction()
        ))

        blood = Sprite(self.bloodAnimation[0], True)
        blood.x = pos[0]
        blood.y = pos[1]
        blood.scaleX = sprite.scaleX * 2
        blood.scaleY = sprite.scaleY * 2
        blood.setDirty()
        self.addNode(blood, 150)
        blood.runAction(SequenceAction(
            AnimateAction(0.25, self.bloodAnimation),
            RemoveSelfAction()
        ))

    def onMiss(self, pos):
        miss = Sprite(self.missSpriteFrame, True)
        miss.x = pos[0]
        miss.y = pos[1]
        miss.scaleX = 0.05
        miss.scaleY = 0.05
        miss.setDirty()
        self.addNode(miss, 150)
        miss.runAction(SequenceAction(
            SpawnAction(
                MoveToAction(0.75, pos[0], pos[1] - 50),
                FadeOutAction(0.75)
            ),
            RemoveSelfAction()
        ))

    def setPoint(self, point):
        sprite = self.getNode("point")
        sprite.setString("Point: " + str(point) + "/" + str(config.REQUIRED_POINT))

    def setHit(self, hit):
        sprite = self.getNode("hit")
        sprite.setString("Hit: " + str(hit))

    def setMiss(self, miss):
        sprite = self.getNode("miss")
        sprite.setString("Miss: " + str(miss))

    def setTime(self, time):
        sprite = self.getNode("time")
        s = math.ceil(time/1000)
        m = math.floor(s/60)
        s -= m * 60
        sprite.setString(("0" if m < 10 else "") + str(m) + ":" + ("0" if s < 10 else "") + str(s))

    def setBullet(self, bullets):
        sprite = self.getNode("bullet")
        sprite.setString(str(bullets))

    def effectAddBullet(self, bullets):
        add = Label("+" + str(bullets), "monospace", 40, constants.GREEN)
        add.setBold()
        add.x, add.y = 110, 160
        add.anchorX, add.anchorY = 0, 0.5
        self.addNode(add, 0)
        add.runAction(SequenceAction(
            SpawnAction(
                MoveToAction(0.75, 110, 120),
                FadeOutAction(0.75)
            ),
            RemoveSelfAction()
        ))

    def effectSubBullet(self, bullets):
        sub = Label("-" + str(bullets), "monospace", 40, constants.RED)
        sub.setBold()
        sub.x, sub.y = 110, 160
        sub.anchorX, sub.anchorY = 0, 0.5
        self.addNode(sub, 0)
        sub.runAction(SequenceAction(
            SpawnAction(
                MoveToAction(0.75, 110, 120),
                FadeOutAction(0.75)
            ),
            RemoveSelfAction()
        ))

    def instance():
        if UIManager._instance is None:
            UIManager._instance = UIManager()
        return UIManager._instance

class Node:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.scaleX = 1
        self.scaleY = 1
        self.rotate = 0
        self.anchorX = 0
        self.anchorY = 0
        self.width = 0
        self.height = 0
        self.zOrder = 0
        self.visible = True
        self.opacity = 255
        self.name = None
        self.setDirty()

        self.actions = []
        self.scheduled = False

    def onEnter(self):
        pass

    def setDirty(self, dirty=True):
        self.dirty = dirty

    def draw(self, screen):
        pass

    def computeTransform(self):
        pass

    def onMouseEvent(self, eventType, mouse):
        return False

    def runAction(self, action):
        action.setNode(self)
        self.actions.append(action)

    def stopAllActions(self):
        self.actions = []

    def update(self, dt):
        pass

    def updateActions(self, dt):
        for action in self.actions:
            if action.update(dt):
                self.actions.remove(action)

class Sprite(Node):
    def __init__(self, pathOrSpriteFrame, ignore=False):
        super().__init__()
        if isinstance(pathOrSpriteFrame, str):
            self.spriteFrame = pygame.Surface.convert_alpha(pygame.image.load(pathOrSpriteFrame))
        else:
            self.spriteFrame = pathOrSpriteFrame
        self.width = self.spriteFrame.get_width()
        self.height = self.spriteFrame.get_height()
        self.anchorX, self.anchorY = 0.5, 0.5

        self.ignore = ignore
        self.inMouseEvent = False
        self.mouseBeganPos = None
        self.mouseMovedPos = None
        self.mouseEndedPos = None
        self.onMouseBegan = None
        self.onMouseMoved = None
        self.onMouseEnded = None
        self.onMouseCanceled = None

    def draw(self, screen):
        if self.dirty:
            self.computeTransform()
        if self.visible:
            screen.blit(self.img, (self.x - self.virtualAnchorX * self.virtualWidth, self.y - self.virtualAnchorY * self.virtualHeight))

    def computeTransform(self):
        self.img = pygame.transform.scale(self.spriteFrame, (round(self.width * self.scaleX), round(self.height * self.scaleY)))
        self.img = pygame.transform.rotate(self.img, self.rotate)
        
        anchorVec = pygame.math.Vector2((self.anchorX - 0.5) * self.width * self.scaleX, (self.anchorY - 0.5) * self.height * self.scaleY)
        anchorVec = anchorVec.rotate(self.rotate)
        self.virtualWidth = abs(self.width * self.scaleX * math.cos(self.rotate / 180 * math.pi)) + abs(self.height * self.scaleY * math.sin(self.rotate / 180 * math.pi))
        self.virtualHeight = abs(self.width * self.scaleX * math.sin(self.rotate / 180 * math.pi)) + abs(self.height * self.scaleY * math.cos(self.rotate / 180 * math.pi))
        anchorVec = anchorVec * self.virtualWidth / self.width
        anchorVec += pygame.math.Vector2(0.5 * self.virtualWidth, 0.5 * self.virtualHeight)

        self.virtualAnchorX = anchorVec.x / self.virtualWidth
        self.virtualAnchorY = anchorVec.y / self.virtualHeight
        self.virtualX = self.x - self.virtualAnchorX * self.virtualWidth
        self.virtualY = self.y - self.virtualAnchorY * self.virtualHeight
        self.img.set_alpha(self.opacity)
        self.setDirty(False)
    
    def setSpriteFrame(self, spriteFrame):
        self.spriteFrame = spriteFrame
        self.setDirty()

    def onMouseEvent(self, eventType, mouse):
        if self.ignore:
            return False
        if eventType == pygame.MOUSEBUTTONDOWN:
            if self.visible:
                pos = pygame.math.Vector2(mouse.get_pos())
                pos = (round(pos.x - self.virtualX), round(pos.y - self.virtualY))
                if pos[0] >= 0 and pos[0] < self.img.get_width() and pos[1] >= 0 and pos[1] < self.img.get_height() and self.img.get_at(pos).a > 0:
                    self.inMouseEvent = True
                    self.mouseBeganPos = pygame.math.Vector2(pos)
                    if self.onMouseBegan:
                        self.onMouseBegan(self)
                    return True
                else:
                    return False
        elif eventType == pygame.MOUSEBUTTONUP:
            if self.inMouseEvent:
                pos = pygame.math.Vector2(mouse.get_pos())
                pos = (round(pos.x - self.virtualX), round(pos.y - self.virtualY))
                self.inMouseEvent = False
                self.mouseEndedPos = pygame.math.Vector2(pos)
                if pos[0] >= 0 and pos[0] < self.img.get_width() and pos[1] >= 0 and pos[1] < self.img.get_height() and self.img.get_at(pos).a > 0:
                    if self.onMouseEnded:
                        self.onMouseEnded(self)
                else:
                    if self.onMouseCanceled:
                        self.onMouseCanceled(self)
        elif eventType == pygame.MOUSEMOTION:
            if self.inMouseEvent:
                pos = pygame.math.Vector2(mouse.get_pos())
                pos = (round(pos.x - self.virtualX), round(pos.y - self.virtualY))
                self.mouseMovedPos = pygame.math.Vector2(pos)
                if self.onMouseMoved:
                    self.onMouseMoved(self)
        return False

class LayerColor(Node):
    def __init__(self, color, width, height):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height

        self.inMouseEvent = False
        self.mouseBeganPos = None
        self.mouseMovedPos = None
        self.mouseEndedPos = None
        self.onMouseBegan = None
        self.onMouseMoved = None
        self.onMouseEnded = None
        self.onMouseCanceled = None

    def draw(self, screen):
        if self.dirty:
            self.computeTransform()
        if self.visible:
            screen.blit(self.img, (self.x - self.virtualAnchorX * self.virtualWidth, self.y - self.virtualAnchorY * self.virtualHeight))

    def computeTransform(self):
        self.img = pygame.Surface.convert_alpha(pygame.Surface((self.width, self.height)))
        self.img.fill(self.color)

        anchorVec = pygame.math.Vector2((self.anchorX - 0.5) * self.width * self.scaleX, (self.anchorY - 0.5) * self.height * self.scaleY)
        anchorVec = anchorVec.rotate(self.rotate)
        self.virtualWidth = abs(self.width * self.scaleX * math.cos(self.rotate / 180 * math.pi)) + abs(self.height * self.scaleY * math.sin(self.rotate / 180 * math.pi))
        self.virtualHeight = abs(self.width * self.scaleX * math.sin(self.rotate / 180 * math.pi)) + abs(self.height * self.scaleY * math.cos(self.rotate / 180 * math.pi))
        anchorVec = anchorVec * self.virtualWidth / self.width
        anchorVec += pygame.math.Vector2(0.5 * self.virtualWidth, 0.5 * self.virtualHeight)

        self.virtualAnchorX = anchorVec.x / self.virtualWidth
        self.virtualAnchorY = anchorVec.y / self.virtualHeight
        self.virtualX = self.x - self.virtualAnchorX * self.virtualWidth
        self.virtualY = self.y - self.virtualAnchorY * self.virtualHeight
        self.img.set_alpha(self.opacity)
        self.setDirty(False)

    def onMouseEvent(self, eventType, mouse):
        if eventType == pygame.MOUSEBUTTONDOWN:
            if self.visible:
                pos = pygame.math.Vector2(mouse.get_pos())
                pos = (round(pos.x - self.virtualX), round(pos.y - self.virtualY))
                if pos[0] >= 0 and pos[0] < self.img.get_width() and pos[1] >= 0 and pos[1] < self.img.get_height() and self.img.get_at(pos).a > 0:
                    self.inMouseEvent = True
                    self.mouseBeganPos = pygame.math.Vector2(pos)
                    if self.onMouseBegan:
                        self.onMouseBegan(self)
                else:
                    return False
        elif eventType == pygame.MOUSEBUTTONUP:
            if self.inMouseEvent:
                pos = pygame.math.Vector2(mouse.get_pos())
                pos = (round(pos.x - self.virtualX), round(pos.y - self.virtualY))
                self.inMouseEvent = False
                self.mouseEndedPos = pygame.math.Vector2(pos)
                if pos[0] >= 0 and pos[0] < self.img.get_width() and pos[1] >= 0 and pos[1] < self.img.get_height() and self.img.get_at(pos).a > 0:
                    if self.onMouseEnded:
                        self.onMouseEnded(self)
                else:
                    if self.onMouseCanceled:
                        self.onMouseCanceled(self)
        elif eventType == pygame.MOUSEMOTION:
            if self.inMouseEvent:
                pos = pygame.math.Vector2(mouse.get_pos())
                pos = (round(pos.x - self.virtualX), round(pos.y - self.virtualY))
                self.mouseMovedPos = pygame.math.Vector2(pos)
                if self.onMouseMoved:
                    self.onMouseMoved(self)
        return False

class Button(Node):
    def __init__(self, path):
        super().__init__()
        self.spriteFrame = pygame.Surface.convert_alpha(pygame.image.load(path))
        self.width = self.spriteFrame.get_width()
        self.height = self.spriteFrame.get_height()
        self.anchorX, self.anchorY = 0.5, 0.5
        self.focusScale = 1.1
        self.isFocus = False
        
        self.inMouseEvent = False
        self.mouseBeganPos = None
        self.mouseMovedPos = None
        self.mouseEndedPos = None
        self.onMouseBegan = None
        self.onMouseMoved = None
        self.onMouseEnded = None
        self.onMouseCanceled = None

    def draw(self, screen):
        if self.dirty:
            self.computeTransform()
        if self.visible:
            screen.blit(self.img, (self.x - self.virtualAnchorX * self.virtualWidth, self.y - self.virtualAnchorY * self.virtualHeight))

    def computeTransform(self):
        extraScale = self.focusScale if self.isFocus else 1
        scaleX = self.scaleX * extraScale
        scaleY = self.scaleY * extraScale
        self.img = pygame.transform.scale(self.spriteFrame, (round(self.width * scaleX), round(self.height * scaleX)))
        self.img = pygame.transform.rotate(self.img, self.rotate)
        
        anchorVec = pygame.math.Vector2((self.anchorX - 0.5) * self.width * scaleX, (self.anchorY - 0.5) * self.height * scaleY)
        anchorVec = anchorVec.rotate(self.rotate)
        self.virtualWidth = abs(self.width * scaleX * math.cos(self.rotate / 180 * math.pi)) + abs(self.height * scaleY * math.sin(self.rotate / 180 * math.pi))
        self.virtualHeight = abs(self.width * scaleX * math.sin(self.rotate / 180 * math.pi)) + abs(self.height * scaleY * math.cos(self.rotate / 180 * math.pi))
        anchorVec = anchorVec * self.virtualWidth / self.width
        anchorVec += pygame.math.Vector2(0.5 * self.virtualWidth, 0.5 * self.virtualHeight)

        self.virtualAnchorX = anchorVec.x / self.virtualWidth
        self.virtualAnchorY = anchorVec.y / self.virtualHeight
        self.virtualX = self.x - self.virtualAnchorX * self.virtualWidth
        self.virtualY = self.y - self.virtualAnchorY * self.virtualHeight
        self.img.set_alpha(self.opacity)
        self.setDirty(False)

    def setSpriteFrame(self, path):
        self.spriteFrame = pygame.Surface.convert_alpha(pygame.image.load(path))
        self.setDirty()

    def onMouseEvent(self, eventType, mouse):
        if eventType == pygame.MOUSEBUTTONDOWN:
            if self.visible:
                pos = pygame.math.Vector2(mouse.get_pos())
                pos = (round(pos.x - self.virtualX), round(pos.y - self.virtualY))
                if pos[0] >= 0 and pos[0] < self.img.get_width() and pos[1] >= 0 and pos[1] < self.img.get_height() and self.img.get_at(pos).a > 0:
                    self.inMouseEvent = True
                    self.mouseBeganPos = pygame.math.Vector2(pos)
                    if self.onMouseBegan:
                        self.onMouseBegan(self)
                else:
                    return False
        elif eventType == pygame.MOUSEBUTTONUP:
            if self.inMouseEvent:
                pos = pygame.math.Vector2(mouse.get_pos())
                pos = (round(pos.x - self.virtualX), round(pos.y - self.virtualY))
                self.inMouseEvent = False
                self.mouseEndedPos = pygame.math.Vector2(pos)
                if pos[0] >= 0 and pos[0] < self.img.get_width() and pos[1] >= 0 and pos[1] < self.img.get_height() and self.img.get_at(pos).a > 0:
                    print(self.name + " ended")
                    if self.onMouseEnded:
                        self.onMouseEnded(self)
                else:
                    print(self.name + " canceled")
                    if self.onMouseCanceled:
                        self.onMouseCanceled(self)
        elif eventType == pygame.MOUSEMOTION:
            pos = pygame.math.Vector2(mouse.get_pos())
            pos = (round(pos.x - self.virtualX), round(pos.y - self.virtualY))
            if self.inMouseEvent:
                self.mouseMovedPos = pygame.math.Vector2(pos)
                if self.onMouseMoved:
                    self.onMouseMoved(self)
            if pos[0] >= 0 and pos[0] < self.img.get_width() and pos[1] >= 0 and pos[1] < self.img.get_height() and self.img.get_at(pos).a > 0:
                if not self.isFocus:
                    self.setDirty()
                self.isFocus = True
            else:
                if self.isFocus:
                    self.setDirty()
                self.isFocus = False
        return False
            
class Label(Node):
    def __init__(self, text, fontName="monospace", fontSize=20, color=constants.BLACK):
        super().__init__()
        self.anchorX, self.anchorY = 0.5, 0.5
        self.text = text
        self.fontName = fontName
        self.fontSize = fontSize
        self.color = color
        self.font = pygame.font.SysFont(self.fontName, self.fontSize)

    def draw(self, screen):
        if self.text != "":
            if self.dirty:
                self.computeTransform()
            if self.visible:
                screen.blit(self.img, (self.x - self.virtualAnchorX * self.virtualWidth, self.y - self.virtualAnchorY * self.virtualHeight))

    def computeTransform(self):
        if self.text != "":
            self.spriteFrame = self.font.render(self.text, False, self.color)
            self.width = self.spriteFrame.get_width()
            self.height = self.spriteFrame.get_height()
            self.img = pygame.transform.scale(self.spriteFrame, (round(self.width * self.scaleX), round(self.height * self.scaleY)))
            self.img = pygame.transform.rotate(self.img, self.rotate)
            
            anchorVec = pygame.math.Vector2((self.anchorX - 0.5) * self.width * self.scaleX, (self.anchorY - 0.5) * self.height * self.scaleY)
            anchorVec = anchorVec.rotate(self.rotate)
            self.virtualWidth = abs(self.width * self.scaleX * math.cos(self.rotate / 180 * math.pi)) + abs(self.height * self.scaleY * math.sin(self.rotate / 180 * math.pi))
            self.virtualHeight = abs(self.width * self.scaleX * math.sin(self.rotate / 180 * math.pi)) + abs(self.height * self.scaleY * math.cos(self.rotate / 180 * math.pi))
            anchorVec = anchorVec * self.virtualWidth / self.width
            anchorVec += pygame.math.Vector2(0.5 * self.virtualWidth, 0.5 * self.virtualHeight)

            self.virtualAnchorX = anchorVec.x / self.virtualWidth
            self.virtualAnchorY = anchorVec.y / self.virtualHeight
            self.virtualX = self.x - self.virtualAnchorX * self.virtualWidth
            self.virtualY = self.y - self.virtualAnchorY * self.virtualHeight
            self.img.set_alpha(self.opacity)
        self.setDirty(False)

    def setString(self, text):
        self.text = text
        self.setDirty()

    def setBold(self, bold=True):
        self.font.set_bold(bold)
        self.setDirty()

    def setItalic(self, italic=True):
        self.font.set_italic(italic)
        self.setDirty()

class Action:
    def __init__(self, time=0):
        self.time = time * 1000
        self.timer = 0
        self.rep = 0

    def setNode(self, node):
        self.node = node
        self.timer = 0

    def repeat(self, rep):
        self.rep = rep
        return self

    def repeatForever(self):
        return self.repeat(-1)

    def update(self, dt):
        pass

class MoveToAction(Action):
    def __init__(self, time, x, y):
        super().__init__(time)
        self.endX = x
        self.endY = y

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            self.timer = 0
            self.node.x = self.endX
            self.node.y = self.endY
            if self.rep == 0:
                self.node.setDirty()
                return True
            elif self.rep > 0:
                self.rep -= 1
        else:
            temp = pygame.math.Vector2(self.node.x - self.endX, self.node.y - self.endY)
            temp = temp / (self.time - self.timer + dt) * (self.time - self.timer)
            self.node.x = temp.x + self.endX
            self.node.y = temp.y + self.endY
        self.node.setDirty()
        return False

class ScaleToAction(Action):
    def __init__(self, time, x, y):
        super().__init__(time)
        self.endScaleX = x
        self.endScaleY = y

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            self.timer = 0
            self.node.scaleX = self.endScaleX
            self.node.ScaleY = self.endScaleY
            if self.rep == 0:
                self.node.setDirty()
                return True
            elif self.rep > 0:
                self.rep -= 1
        else:
            temp = pygame.math.Vector2(self.node.scaleX - self.endScaleX, self.node.scaleY - self.endScaleY)
            temp = temp / (self.time - self.timer + dt) * (self.time - self.timer)
            self.node.scaleX = temp.x + self.endScaleX
            self.node.scaleY = temp.y + self.endScaleY
        self.node.setDirty()
        return False

class RotateToAction(Action):
    def __init__(self, time, rotate):
        super().__init__(time)
        self.endRotate = rotate

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            self.timer = 0
            self.node.rotate = self.endRotate
            if self.rep == 0:
                self.node.setDirty()
                return True
            elif self.rep > 0:
                self.rep -= 1
        else:
            temp = (self.node.rotate - self.endRotate) * (self.time - self.timer)/(self.time - self.timer + dt)
            self.node.rotate = temp + self.endRotate
        self.node.setDirty()
        return False

class FadeToAction(Action):
    def __init__(self, time, opacity):
        super().__init__(time)
        self.endOpacity = opacity

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            self.timer = 0
            self.node.opacity = self.endOpacity
            if self.rep == 0:
                self.node.setDirty()
                return True
            elif self.rep > 0:
                self.rep -= 1
        else:
            temp = (self.node.opacity - self.endOpacity) * (self.time - self.timer)/(self.time - self.timer + dt)
            self.node.opacity = temp + self.endOpacity
        self.node.setDirty()
        return False

class FadeInAction(FadeToAction):
    def __init__(self, time):
        super().__init__(time, 255)

class FadeOutAction(FadeToAction):
    def __init__(self, time):
        super().__init__(time, 0)

class DelayAction(Action):
    def __init__(self, time):
        super().__init__(time)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            self.timer = 0
            if self.rep == 0:
                return True
            elif self.rep > 0:
                self.rep -= 1
        return False

class AnimateAction(Action):
    def __init__(self, time, spriteFrames):
        super().__init__(time)
        self.spriteFrames = spriteFrames

    def update(self, dt):
        if len(self.spriteFrames) == 0:
            return True

        self.timer += dt
        if self.timer >= self.time:
            self.timer = 0
            self.node.spriteFrame = self.spriteFrames[-1]
            if self.rep == 0:
                self.node.setDirty()
                return True
            elif self.rep > 0:
                self.rep -= 1
        else:
            index = math.floor(len(self.spriteFrames) * self.timer/self.time)
            self.node.spriteFrame = self.spriteFrames[index]
        self.node.setDirty()
        return False

class HideAction(Action):
    def __init__(self):
        super().__init__()
    
    def update(self, dt):
        self.node.visible = False
        return True

class ShowAction(Action):
    def __init__(self):
        super().__init__()
    
    def update(self, dt):
        self.node.visible = True
        return True

class RemoveSelfAction(Action):
    def __init__(self):
        super().__init__()
    
    def update(self, dt):
        UIManager.instance().removeNode(self.node)
        return True

class CallAction(Action):
    def __init__(self, func, *arg):
        super().__init__()
        self.func = func
        self.arg = arg

    def update(self, dt):
        self.func(*self.arg)
        return True
    
class SequenceAction(Action):
    def __init__(self, *argv):
        super().__init__()
        self.actions = []
        self.index = 0
        for arg in argv:
            self.actions.append(arg)

    def setNode(self, node):
        super().setNode(node)
        self.index = 0
        for action in self.actions:
            action.setNode(node)

    def update(self, dt):
        if len(self.actions) == 0:
            return True
        action = self.actions[self.index]
        if action.update(dt):
            self.index += 1
            if self.index >= len(self.actions):
                self.index = 0
                if self.rep == 0:
                    return True
                elif self.rep > 0:
                    self.rep -= 1
        return False

class SpawnAction(Action):
    def __init__(self, *argv):
        super().__init__()
        self.actions = []
        self.checkList = []
        for arg in argv:
            self.actions.append(arg)
            self.checkList.append(False)

    def setNode(self, node):
        super().setNode(node)
        for i in range(len(self.checkList)):
            self.checkList[i] = False
        for action in self.actions:
            action.setNode(node)

    def update(self, dt):
        if len(self.actions) == 0:
            return True
        for i, action in enumerate(self.actions):
            if not self.checkList[i]:
                if action.update(dt):
                    self.checkList[i] = True
        if sum([(1 if check else 0) for check in self.checkList]) == len(self.checkList):
            for i in range(len(self.checkList)):
                self.checkList[i] = False
            if self.rep == 0:
                return True
            elif self.rep > 0:
                self.rep -= 1
        return False