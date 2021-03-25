import pygame, config

class SoundManager:
    _instance = None

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load("res/sound/theme.mp3")
        pygame.mixer.music.set_volume(config.MUSIC_VOLUME)
        self.shot = pygame.mixer.Sound("res/sound/shot.wav")
        self.zom = pygame.mixer.Sound("res/sound/zombie.wav")
        self.win = pygame.mixer.Sound("res/sound/win.wav")
        self.lose = pygame.mixer.Sound("res/sound/lose.wav")

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

soundManager = SoundManager.instance()