import py_midicsv
import os
from scripts.TempoEvent import TempoEvent
from scripts.NoteEvent import NoteEvent
from scripts.Events import Events
from scripts.Charter import Charter

CHARTER = Charter()


def main():
    input_folder = 'input/'
    print('Finding midi files inside:', input_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.mid'):
            events = get_events(input_folder, file_name)
            song_name = get_song_name(file_name)
            output = CHARTER.get_output(song_name, events)
            write_output_to_file(song_name, output)


def get_song_name(file_name):
    return file_name[:-4]


def get_events(input_folder, file_name):
    print('Getting events from midi file:', file_name)

    midi_lines = py_midicsv.midi_to_csv(input_folder + file_name)

    notes_events = []
    tempo_events = []
    time_scale = 1

    for midi_line in midi_lines:
        elements = midi_line.split(', ')
        elements[-1] = elements[-1].rstrip() # Removes trailing new line on last element

        element_type = elements[2]

        if element_type == 'Header':
            time_scale = get_time_scale(elements)
        elif element_type == 'Tempo':
            tempo_events.append(get_tempo_event(elements))
        elif element_type == 'Note_on_c' and elements[5] != '0': # Only note 'ON' events
             notes_events.append(get_note_event(elements))

    return Events(tempo_events, notes_events, time_scale)


def get_tempo_event(elements):
    return TempoEvent(elements[1], elements[3])


def get_note_event(elements):
    return NoteEvent(elements[1], elements[4], '0', elements[0])


def get_time_scale(elements):
    return int(elements[5]) / 192


def write_output_to_file(song_name, output):
    file_name = 'output/' + song_name + '.chart'
    print('Writing chart output to file:', file_name)

    with open(file_name, 'w') as f:
        f.write(output)


if __name__ == '__main__':
    main()
