import logging
import os
import random
import threading
from pathlib import Path
from time import sleep

from omxplayer.player import OMXPlayer


logger = logging.getLogger()

VIDEO_MAIN = Path("/home/pi/video/walkinginthestones.mp4")
VIDEO_SEC = Path("/home/pi/video/deeptime.mp4")
AUDIO_DIR = "/home/pi/audio/"


class MediaPlayer:
    def __init__(self):
        self.video_posmain = 0
        self.video_possec = 0
        self.player = None
        self.mp3player = None
        self.waitingForPlayerToFinish = False

    def __del__(self):
        try:
            self.mp3player.quit()
            del self.mp3player
        except:
            pass
        try:
            self.player.quit()
            del self.player
        except:
            pass

    def play_random_audio(self):
        randomfile = random.choice(os.listdir(AUDIO_DIR))
        file = AUDIO_DIR + randomfile
        # Close existing player??
        if self.mp3player != None:
            self.mp3player.quit()
        self.mp3player = OMXPlayer(file, args="--no-osd")

    # This needs to set a callback rather than sleep and block
    def play_media(self):
        if self.waitingForPlayerToFinish == True:
            return

        if self.player and self.player.get_source() == VIDEO_MAIN:
            logger.info(
                "play_media, playing {} for 30 seconds from {} ".format(
                    VIDEO_SEC, self.video_possec
                )
            )
            self.video_posmain = self.player.position()
            self.player.quit()
            self.player = None
            self.player = OMXPlayer(VIDEO_SEC, args="--loop --no-osd")
            self.play_random_audio()
            self.player.seek(self.video_possec)

            def timeoutHandler():
                self.video_possec = self.player.position()
                logger.info(
                    "play_media, playing {} again from {}".format(
                        VIDEO_MAIN, self.video_posmain
                    )
                )
                self.player.quit()
                self.player = None
                self.player = OMXPlayer(VIDEO_MAIN, args="--loop --no-osd")
                sleep(1)
                self.player.seek(self.video_posmain)
                self.waitingForPlayerToFinish = False

            timer = threading.Timer(30.0, timeoutHandler)
            timer.start()
            self.waitingForPlayerToFinish = True
        else:
            logger.info("play_media, playing {}".format(VIDEO_MAIN))
            if self.player != None:
                self.player.quit()
                self.player = None
            self.player = OMXPlayer(VIDEO_MAIN, args="--loop --no-osd")
