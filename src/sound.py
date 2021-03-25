import pygame, config

class SoundManager:
    _instance = None

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load("res/sound/theme.mp3")
        pygame.mixer.music.set_volume(config.MUSIC_VOLUME)
        self.shot = pygame.mixer.Sound("res/sound/shot.wav")
        self.shot.set_volume(config.EFFECT_VOLUME)
        self.zom = pygame.mixer.Sound("res/sound/zombie.wav")
        self.zom.set_volume(config.EFFECT_VOLUME)
        self.win = pygame.mixer.Sound("res/sound/win.wav")
        self.win.set_volume(config.EFFECT_VOLUME)
        self.lose = pygame.mixer.Sound("res/sound/lose.wav")
        self.lose.set_volume(config.EFFECT_VOLUME)
        self.splash = pygame.mixer.Sound("res/sound/splash.wav")
        self.splash.set_volume(config.EFFECT_VOLUME)
        self.miss = pygame.mixer.Sound("res/sound/miss.wav")
        self.miss.set_volume(config.EFFECT_VOLUME * 5)

    def instance():
        if SoundManager._instance is None:
            SoundManager._instance = SoundManager()
        return SoundManager._instance

    def onToggleMusic(self):
        if config.ENABLE_MUSIC:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    def playTheme(self):
        if config.ENABLE_MUSIC:
            pygame.mixer.music.play(-1)

    def playShot(self):
        if config.ENABLE_EFFECT:
            self.shot.play()

    def playZom(self):
        if config.ENABLE_EFFECT:
            self.zom.play()

    def playWin(self):
        if config.ENABLE_EFFECT:
            self.win.play()

    def playLose(self):
        if config.ENABLE_EFFECT:
            self.lose.play()

    def playSplash(self):
        if config.ENABLE_EFFECT:
            self.splash.play()

    def playMiss(self):
        if config.ENABLE_EFFECT:
            self.miss.play()

soundManager = SoundManager.instance()