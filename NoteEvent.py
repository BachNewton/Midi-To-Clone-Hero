class NoteEvent:
    def __init__(self, time, pitch, duration, channel):
        self.time = int(time)
        self.pitch = int(pitch)
        self.duration = int(duration)
        self.channel = channel

    def get_chart_line(self):
        button = self.pitch % 5
        time = int(self.time / 2.5)

        return str(time) + ' = N ' + str(button) + ' ' + str(self.duration)