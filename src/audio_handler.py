import threading
from audioplayer import AudioPlayer


def play_sound_basic(sound):
    AudioPlayer(sound).play(block=True)  # for some reason, block=False doesn't play sound, so threading used


def play_sound(sound):
    def _play():
        play_sound_basic(sound)

    threading.Thread(target=_play, daemon=True).start()
