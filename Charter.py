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
        header += 'Charter = "Midi to Clone Hero Script"\n'
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
        sync_track += '0 = TS 4\n' # We assume time signature is 4/4

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


    @staticmethod
    def get_tracks_output(track_names, note_events, time_scale):
        tracks = ''

        channels = {}

        for note_event in note_events:
            channel = note_event.channel

            if channel not in channels:
                channels[channel] = []

            channels[channel].append(note_event)

        for channel in channels:
            if channel < len(track_names): # We have to skip some channels if we've run out of tracks
                tracks += '[' + track_names[channel] + ']\n'
                tracks += '{\n'

                for note_event in channels[channel]:
                    tracks += note_event.get_chart_line(time_scale) + '\n'

                tracks += '}\n'

        return tracks