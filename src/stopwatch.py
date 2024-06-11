import time


class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        self.visible = True

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True

    def pause_toggle(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False
        else:
            self.start_time = time.time() - self.elapsed_time
            self.running = True

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def hide_show(self):
        self.visible = not self.visible

    def get_elapsed_time(self):
        if not self.visible:
            return ""
        if self.running:
            self.elapsed_time = time.time() - self.start_time
        return self.format_time(self.elapsed_time)

    @staticmethod
    def format_time(elapsed):
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)

        if hours > 0:
            return f"{hours}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"
