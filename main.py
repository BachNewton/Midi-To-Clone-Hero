import py_midicsv


def main():
    events = py_midicsv.midi_to_csv("input.mid")

    notes = []
    temp_changes = []

    for event in events:
        parts = event.split(', ')

        if parts[2] == 'Tempo':
            temp_changes.append({
                'time': parts[1],
                'speed': parts[3][:len(parts[2]) - 1]
            })
        elif parts[2] == 'Note_on_c' and parts[5] != '0\n':
            notes.append({
                'time': parts[1],
                'note': parts[4],
            })

    create_chart(temp_changes, notes)


def create_chart(temp_changes, notes):
    a = """[Song]
{
  Name = "Midi to Chart Song"
  Offset = 0
  Resolution = 192
  Player2 = bass
  Difficulty = 0
  PreviewStart = 0
  PreviewEnd = 0
  Genre = "rock"
  MediaType = "cd"
}
[SyncTrack]
{
  0 = TS 4
"""
    b = """}
[Events]
{
}
"""

    tempo_lines = []

    for tempo in temp_changes:
        time = str(int(int(tempo['time']) / 2.5))
        percentage = 600000.0 / int(tempo['speed'])
        speed = str(int(percentage * 1000))  # 100000
        line = time + ' = B ' + speed + '\n'
        tempo_lines.append(line)

    track_names = [
        'ExpertSingle',
        'ExpertDoubleGuitar',
        'ExpertDoubleBass',
        'ExpertDoubleRhythm',
        'ExpertKeyboard',
        'HardSingle',
        'HardDoubleGuitar',
        'HardDoubleBass',
        'HardDoubleRhythm',
        'HardKeyboard',
        'MediumSingle',
        'MediumDoubleGuitar',
        'MediumDoubleBass',
        'MediumDoubleRhythm',
        'MediumKeyboard'
    ]

    tracks = {
        'ExpertSingle': [],
        'ExpertDoubleGuitar': [],
        'ExpertDoubleBass': [],
        'ExpertDoubleRhythm': [],
        'ExpertKeyboard': [],
        'HardSingle': [],
        'HardDoubleGuitar': [],
        'HardDoubleBass': [],
        'HardDoubleRhythm': [],
        'HardKeyboard': [],
        'MediumSingle': [],
        'MediumDoubleGuitar': [],
        'MediumDoubleBass': [],
        'MediumDoubleRhythm': [],
        'MediumKeyboard': []
    }

    for note in notes:
        button = note_to_button(note['note'])
        time = str(int(int(note['time']) / 2.5))

        line = time + ' = N ' + button + ' 0\n'
        track_name = track_names[0]
        tracks[track_name].append(line)

    with open('output.chart', 'w') as f:
        f.write(a)
        f.writelines(tempo_lines)
        f.write(b)

        for track_name in tracks:
            f.write('[' + track_name + ']\n{\n')
            f.writelines(tracks[track_name])
            f.write('}\n')


def note_to_button(note):
    if note == '38':
        # Snare
        return '0'
    elif note == '36':
        # Bass Drum
        return '7'
    elif note == '42':
        # Closed Hi-Hat
        return '1'
    elif note == '51':
        # Ride Cymbal
        return '2'
    else:
        return '4'


if __name__ == '__main__':
    main()
