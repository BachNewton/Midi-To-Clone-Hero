class NoteEvent:
    def __init__(self, time, pitch, duration, channel):
        self.time = int(time)
        self.pitch = int(pitch)
        self.duration = int(duration)
        self.channel = int(channel) - 1

    def get_chart_line(self, time_scale):
        button = self.pitch % 5
        time = int(self.time / time_scale)

        return str(time) + ' = N ' + str(button) + ' ' + str(self.duration)