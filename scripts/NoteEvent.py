class NoteEvent:
    def __init__(self, time, pitch, velocity, channel):
        self.time = int(time)
        self.pitch = int(pitch)
        self.isOnEvent = velocity != '0'
        self.channel = int(channel) - 1

    def get_chart_line(self, time_scale, duration):
        button = self.pitch % 5
        time = int(self.time / time_scale)

        return str(time) + ' = N ' + str(button) + ' ' + str(duration)
