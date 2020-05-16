class TempoEvent:
    SIXTY_BILLION = 60000000000.0

    def __init__(self, time, tempo):
        self.time = int(time)
        self.tempo = int(tempo)

    def get_chart_line(self, time_scale):
        time = int(self.time / time_scale)
        tempo = int(self.SIXTY_BILLION / self.tempo)

        return str(time) + ' = B ' + str(tempo)