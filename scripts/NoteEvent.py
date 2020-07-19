class NoteEvent:
    def __init__(self, time, pitch, velocity, channel):
        self.time = int(time)
        self.pitch = int(pitch)
        self.isOnEvent = velocity != '0'
        self.channel = channel
        self.isDrumNote = channel == '9'

    def get_chart_line(self, time_scale, button, duration):
        time = int(self.time / time_scale)

        return str(time) + ' = N ' + str(button) + ' ' + str(duration)
