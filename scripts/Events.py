import py_midicsv
from scripts.TempoEvent import TempoEvent
from scripts.NoteEvent import NoteEvent

class Events:
    TIME_SCALE_BASE = 192

    def __init__(self, input_folder, file_name):
        print('Getting events from midi file:\n\t', file_name)

        midi_lines = py_midicsv.midi_to_csv(input_folder + file_name)

        note_events = []
        tempo_events = []
        time_scale = 1

        for midi_line in midi_lines:
            elements = midi_line.split(', ')
            elements[-1] = elements[-1].rstrip()  # Removes trailing new line on last element

            element_type = elements[2]

            if element_type == 'Header':
                time_scale = self.get_time_scale(elements)
            elif element_type == 'Tempo':
                tempo_events.append(self.get_tempo_event(elements))
            elif element_type == 'Note_on_c':
                note_events.append(self.get_note_event(elements))


        self.tempo_events = tempo_events
        self.note_events = note_events
        self.time_scale = time_scale

    @staticmethod
    def get_tempo_event(elements):
        return TempoEvent(elements[1], elements[3])

    @staticmethod
    def get_note_event(elements):
        return NoteEvent(elements[1], elements[4], elements[5], elements[0])

    def get_time_scale(self, elements):
        return int(elements[5]) / self.TIME_SCALE_BASE
