import contextlib
import os
import threading
from pydub.playback import play


def play_sound_basic(sound):
    with open(os.devnull, 'w') as target_file:
        with contextlib.redirect_stderr(target_file):
            play(sound)


def play_sound_async(sound):
    def _play():
        play_sound_basic(sound)

    threading.Thread(target=_play, daemon=True).start()
