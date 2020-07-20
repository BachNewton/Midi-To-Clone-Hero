class Charter:
    TRACK_NAMES = [
        'ExpertSingle',
        'ExpertDoubleBass',
        'ExpertDoubleRhythm',
        'ExpertDoubleGuitar',
        'ExpertKeyboard',
        'HardSingle',
        'HardDoubleBass',
        'HardDoubleRhythm',
        'HardDoubleGuitar',
        'HardKeyboard',
        'MediumSingle',
        'MediumDoubleBass',
        'MediumDoubleRhythm',
        'MediumDoubleGuitar',
        'MediumKeyboard',
        'EasySingle',
        'EasyDoubleBass',
        'EasyDoubleRhythm',
        'EasyDoubleGuitar',
        'EasyKeyboard'
    ]

    BUTTONS = 5

    def get_output(self, name, events):
        output = ''

        output += self.get_song_output(name) + '\n'
        output += self.get_sync_track_output(events.tempo_events, events.time_scale) + '\n'
        output += self.get_events_output() + '\n'
        output += self.get_tracks_output(self.TRACK_NAMES, events.note_events, events.time_scale) + '\n'

        return output

    @staticmethod
    def get_song_output(name):
        header = ''

        header += '[Song]\n'
        header += '{\n'
        header += 'Name = "' + name + '"\n'
        header += 'Charter = "Kyle Hutchinson"\n'
        header += 'Offset = 0\n'
        header += 'Resolution = 192\n'
        header += 'Player2 = bass\n'
        header += 'Difficulty = 0\n'
        header += 'PreviewStart = 0\n'
        header += 'PreviewEnd = 0\n'
        header += 'Genre = "Midi"\n'
        header += 'MediaType = "cd"\n'
        header += '}'

        return header

    @staticmethod
    def get_sync_track_output(tempo_events, time_scale):
        sync_track = ''

        sync_track += '[SyncTrack]\n'
        sync_track += '{\n'
        sync_track += '0 = TS 4\n'  # We assume time signature is 4/4

        for tempo_event in tempo_events:
            sync_track += tempo_event.get_chart_line(time_scale) + '\n'

        sync_track += '}'

        return sync_track

    @staticmethod
    def get_events_output():
        events = ''

        events += '[Events]\n'
        events += '{\n'
        events += '}'

        return events

    def get_tracks_output(self, track_names, note_events, time_scale):
        tracks = ''

        midi_tracks = {}
        drum_notes = []

        for note_event in note_events:
            if note_event.isOnEvent:
                if note_event.isDrumNote:
                    drum_notes.append(note_event)
                else:
                    midi_track = note_event.track

                    if midi_track not in midi_tracks:
                        midi_tracks[midi_track] = []

                    midi_tracks[midi_track].append(note_event)

        ordered_midi_tracks = []

        for midi_track in midi_tracks:
            ordered_midi_tracks.append(midi_tracks[midi_track])

        ordered_midi_tracks.sort(key=len, reverse=True)

        for i in range(min(len(track_names), len(ordered_midi_tracks))):
            track = self.get_track(track_names[i], ordered_midi_tracks[i], time_scale)
            tracks += track + '\n'

        # TODO: Add drum support when this is complete: https://strikeline.myjetbrains.com/youtrack/issue/CH-58
        # tracks += self.get_drum_track(drum_notes, time_scale) + '\n'

        return tracks

    def get_drum_track(self, note_events, time_scale):
        track = ''

        track += '[ExpertDrums]\n'
        track += '{\n'

        for note_event in note_events:
            button = self.get_drum_button(note_event.pitch)
            if button is not None:
                line = note_event.get_chart_line(time_scale, button, 0)  # Drum notes never have a duration
                track += line + '\n'

        track += '}'

        return track

    @staticmethod
    def get_drum_button(pitch):
        if pitch in [35, 36]:  # Acoustic Bass Drum, Electric Bass Drum
            button = 0  # Open / Kick
        elif pitch in [38, 40]:  # Acoustic Snare, Electric Snare
            button = 1  # Lane 1 / Red Tom
        elif pitch == 42:  # Closed Hi-hat
            button = 66  # Pro Drums Cymbal Lane 2 / Yellow Cymbal
        elif pitch == 51:  # Ride Cymbal 1
            button = 67  # Pro Drums Cymbal Lane 3 / Blue Cymbal
        else:
            print('Warning! - Unknown drum pitch:', pitch, '- Skipping this note')
            button = None

        return button

    def get_track(self, track_name, note_events, time_scale):
        track = ''

        track += '[' + track_name + ']\n'
        track += '{\n'

        last_pitch = 60  # Start on 'Middle C'
        last_button = 2  # Start on 'Yellow' button

        for note_event in note_events:
            button = self.get_button(note_event.pitch, last_pitch, last_button)
            line = note_event.get_chart_line(time_scale, button, 0)  # TODO: Add note duration
            track += line + '\n'

            last_pitch = note_event.pitch
            last_button = button

        track += '}'

        return track

    def get_button(self, pitch, last_pitch, last_button):
        diff = pitch - last_pitch
        direction = 1 if diff > 0 else -1
        diff = abs(diff)
        diff %= 13  # If we pass an octave, loop around

        # Minor Second / Major Second
        if diff in [1, 2]:
            last_button += direction * 1
            button = last_button % self.BUTTONS
        # Minor Third / Major Third / Perfect Forth
        elif diff in [3, 4, 5]:
            last_button += direction * 2
            button = last_button % self.BUTTONS
        # Tritone / Perfect Fifth / Minor Sixth / Major Sixth
        elif diff in [6, 7, 8, 9]:
            last_button += direction * 3
            button = last_button % self.BUTTONS
        # Minor Seventh / Major Seventh / Octave
        elif diff in [10, 11, 12]:
            last_button += direction * 4
            button = last_button % self.BUTTONS
        # Perfect Unison
        else:
            button = last_button

        return button
