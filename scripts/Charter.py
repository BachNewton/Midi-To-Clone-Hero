class Charter:
    TRACK_NAMES = [
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
        'MediumKeyboard',
        'EasySingle',
        'EasyDoubleGuitar',
        'EasyDoubleBass',
        'EasyDoubleRhythm',
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

        channels = {}

        for note_event in note_events:
            if note_event.isOnEvent:
                channel = note_event.channel

                if channel not in channels:
                    channels[channel] = []

                channels[channel].append(note_event)

        for channel in channels:
            if channel < len(track_names):  # We have to skip some channels if we've run out of tracks
                track = self.get_track(track_names[channel], channels[channel], time_scale)
                tracks += track + '\n'

        return tracks

    def get_track(self, track_name, note_events, time_scale):
        track = ''

        track += '[' + track_name + ']\n'
        track += '{\n'

        last_pitch = 60  # Start on 'Middle C'
        last_button = 3  # Start on 'Yellow' button

        for note_event in note_events:
            button = self.get_button(note_event.pitch, last_pitch, last_button)
            line = note_event.get_chart_line(time_scale, button, 0)  # Note duration will be added later
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
