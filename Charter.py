class Charter:
    def get_output(self, name, tempo_lines, note_lines):
        output = ''

        output += self.get_song_output(name) + '\n'
        output += self.get_sync_track_output(tempo_lines) + '\n'
        output += self.get_events_output() + '\n'
        output += self.get_tracks_output(note_lines) + '\n'

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
    def get_sync_track_output(tempo_lines):
        sync_track = ''

        sync_track += '[SyncTrack]\n'
        sync_track += '{\n'
        sync_track += '0 = TS 4\n' # We assume time signature is 4/4

        for tempo_line in tempo_lines:
            sync_track += tempo_line + '\n'

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
    def get_tracks_output(note_lines):
        tracks = ''

        tracks += '[ExpertSingle]\n'
        tracks += '{\n'

        for note_line in note_lines:
            tracks += note_line + '\n'

        tracks += '}'

        return tracks