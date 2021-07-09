from midiutil.MidiFile import MIDIFile
import py_midicsv
import csv


# read in midi files
# create list/array of midi song files(in same key(C?))
# for every song extract song information and put into bigger csv file
# run machine learning algorithm on notes (if current note is c what will the next note be?)

# Load the MIDI file and parse it into CSV format
csv_string_list = py_midicsv.midi_to_csv("happy_birthday_fl.mid")


# function to find first substring in list of strings
def index_containing_second_substring(the_list, substring):
    second_occurrence = False
    for k, s in enumerate(the_list):
        if substring in s:
            if not second_occurrence:
                second_occurrence = True
            else:
                return k
    return -1


def index_containing_substring(the_list, substring):
    for k, s in enumerate(the_list):
        if substring in s:
                return k
    return -1


print(csv_string_list)

# find first note in midi
# print(csv_string_list.index('2, 1920, Note_on_c, 1, 67, 66\n'))
print('index of first note')
print(index_containing_substring(csv_string_list, 'Note_on_c'))
first_note = index_containing_substring(csv_string_list, 'Note_on_c')
# find first offnote in midi
print('index of first note end')
print(index_containing_substring(csv_string_list, 'Note_on_c') +1)

# find last note index in midi
print('index last note')
last_note = index_containing_second_substring(csv_string_list, 'End_track')-2
print(last_note)

# find header to get division of time ( how many midi clock pulses are in a quarter note)
print('midi header division time')
split_midi_header = csv_string_list[index_containing_substring(csv_string_list, 'Header')].split(', ')
print(split_midi_header[5])


print('Individual Note length and frequencies: ')
print('----------------------------------------')
i = 0
for x in range(first_note, last_note, 2):
    start_note_event = csv_string_list[x].split(', ')
    end_note_event = csv_string_list[x+1].split(', ')
    print("Note Length: ")
    print((int(end_note_event[1]) - int(start_note_event[1])) / int(split_midi_header[5]))
    print("Note Frequency: ")
    print((int(start_note_event[4])))
    print()

# split row in csv midi event to get note frequency and time of start note
split_midi_start_event = csv_string_list[first_note].split(', ')

# frequency of first note
print(split_midi_start_event[4])

# time of first note
print(split_midi_start_event[1])

# split row in csv midi event to get time of end note
end_note = first_note + 1
split_midi_end_event = csv_string_list[end_note].split(', ')

# time of end first note
print(split_midi_end_event[1])

#duration of first note in midi clock pulses
print(int(split_midi_end_event[1]) - int(split_midi_start_event[1]))
# divide clock pulses by top bpm to find quarter note length
# master bpm
print(split_midi_header[5])



# iterate through every pair of midi events(note_start and note_end) to find every frequency and duration of note
# put information of each song in an array
# put array of songs into a csv file with each row being a new song
# put csv file into machine learning algorithms
# try to predict what the next note is based on the current note frequency/length
# no real way to test for accuracy but play around with rules to see what sounds the best

#


with open('happybday.csv', 'w', newline='') as csvfile:
    midiwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    midiwriter.writerow(csv_string_list)



# Parse the CSV output of the previous command back into a MIDI file
midi_object = py_midicsv.csv_to_midi(csv_string_list)

# Save the parsed MIDI file to disk
with open("example_converted.mid", "wb") as output_file:
    midi_writer = py_midicsv.FileWriter(output_file)
    midi_writer.write(midi_object)






# run through machine learning neural network


# output midi

# create your MIDI object
mf = MIDIFile(1)  # only 1 track
track = 0  # the only track

time = 0  # start at the beginning
mf.addTrackName(track, time, "Sample Track")
mf.addTempo(track, time, 120)

# add some notes
channel = 0
volume = 100

pitch = 60  # C4 (middle C)
time = 0  # start on beat 0
duration = 1  # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 60
time = 2.5  # start on beat 2
duration = 1  # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 60
time = 4  # start on beat 4
duration = 1  # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 60
time = 6.5  # start on beat 4
duration = 1  # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)

# write it to disk
with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)
