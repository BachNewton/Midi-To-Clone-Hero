class NoteEvent:
    def __init__(self, time, pitch, velocity, channel, track):
        self.time = int(time)
        self.pitch = int(pitch)
        self.isOnEvent = velocity != '0'
        self.channel = channel
        self.isDrumNote = channel == '9'  # Channel 9 is always dedicated to drums
        self.track = track

    def get_chart_line(self, time_scale, button, duration):
        time = int(self.time / time_scale)

        # If the button is a drum's cymbal
        if button in [66, 67, 68]:
            preface = str(time) + ' = N ' + str(button) + ' 0\n'
            button = 2 if button == 66 else button
            button = 3 if button == 67 else button
            button = 4 if button == 68 else button
        else:
            preface = ''

        return preface + str(time) + ' = N ' + str(button) + ' ' + str(duration)
