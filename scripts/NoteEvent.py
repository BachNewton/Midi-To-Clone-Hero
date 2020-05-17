class NoteEvent:
    def __init__(self, time, pitch, velocity, channel):
        self.time = int(time)
        self.pitch = int(pitch)
        self.isOnEvent = False if velocity == '0' else True
        self.channel = int(channel) - 1

    def get_chart_line(self, time_scale, duration):
        button = self.pitch % 5
        time = int(self.time / time_scale)

        return str(time) + ' = N ' + str(button) + ' ' + str(duration)
