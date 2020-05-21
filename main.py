import os
import subprocess
import time
from scripts.Events import Events
from scripts.Charter import Charter

CHARTER = Charter()


def main():
    print('|---------------------------------------------|')
    print('|                                             |')
    print('|             Midi to Clone Hero              |')
    print('|         Created by: Kyle Hutchinson         |')
    print('|                                             |')
    print('|---------------------------------------------|')

    input_folder = 'input/'
    print('\nFinding midi files inside:\n\t', input_folder)

    midi_files = [file_name for file_name in os.listdir(input_folder) if file_name.endswith('.mid')]
    convert_files(midi_files, input_folder)


def convert_files(midi_files, input_folder):
    start_time = time.time()
    print('Found:\n\t', midi_files)

    for midi_file in midi_files:
        convert_file(input_folder, midi_file)

    total_time = str(round(time.time() - start_time, 2))
    print('Conversions completed in: ' + total_time + ' seconds')


def convert_file(input_folder, file_name):
    start_time = time.time()
    print('\n-----------------------------------------------')
    song_name = file_name[:-4]
    events = Events(input_folder, file_name)
    output = CHARTER.get_output(song_name, events)
    create_output(input_folder + file_name, song_name, output)
    total_time = str(round(time.time() - start_time, 2))
    print('\nConverted in: ' + total_time + ' seconds')
    print('-----------------------------------------------\n')


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def create_output(mid_file_path, song_name, output):
    output_folder = 'output/'
    create_folder(output_folder)
    output_folder += song_name + '/'
    create_folder(output_folder)

    write_output_to_file(output_folder, output)
    create_audio_from_midi(mid_file_path, output_folder)


def write_output_to_file(output_folder, output):
    file_name = output_folder + 'notes.chart'
    print('Writing chart output to file:\n\t', file_name)

    with open(file_name, 'w') as f:
        f.write(output)


def create_audio_from_midi(mid_file_path, output_folder):
    song_file_name = output_folder + 'song.wav'
    print('Creating audio file from midi:\n\t', song_file_name)

    muse_score_path_windows = 'C:\\"Program Files (x86)"\\"MuseScore 3"\\bin\\MuseScore3'
    muse_score_path_mac = '/Applications/MuseScore 3.app/Contents/MacOS/mscore'

    if os.path.exists(muse_score_path_windows):
        muse_score_path = muse_score_path_windows
    elif os.path.exists(muse_score_path_mac):
        muse_score_path = muse_score_path_mac
    else:
        muse_score_path = ''

    if muse_score_path:
        muse_score_file_name = output_folder + 'song.mscz'

        # Converting temporary .mscz file
        subprocess.run(
            [muse_score_path, '-o', muse_score_file_name, mid_file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Converting the temporary .mscz file into a .wav file
        subprocess.run(
            [muse_score_path, '-o', song_file_name, muse_score_file_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Removing the temporary .mscz file
        os.remove(muse_score_file_name)
    else:
        print('\nERROR - Could not find MuseScore install')
        print('\tOn Windows:\n\t\t', muse_score_path_windows)
        print('\tOn Mac:\n\t\t', muse_score_path_mac)
        print('\tThis file will be skipped. Please create "song.wav" manually.')


if __name__ == '__main__':
    main()
