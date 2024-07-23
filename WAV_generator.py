import numpy as np
import time
from numpy import interp
from numpy import concatenate
from numpy import linspace
from numpy import where
from scipy.io.wavfile import write

start_time = time.time()

def wave_function(height, t):
    a = (BASIC_FREQ * 2**(height/12) * t) % 1
    x = where(SIGMOID_NUMBER == 0, a, where(a != 0, 1 / (1 + ((1 - a)/a)**(SIGMOID_NUMBER + 1)), 0))
    if WAVE_TYPE == 0: #sine_wave
        result_wave = np.sin(2 * np.pi * x)
    elif WAVE_TYPE == 1: #square_wave
        result_wave = where(x <= 1/4, -1, where(x <= 3/4, 1, -1))
    elif WAVE_TYPE == 2: #sawtooth wave
        result_wave = 2*x - 1
    elif WAVE_TYPE == 3: #triangular wave(similar to sine_wave)
        result_wave = 2 * np.abs(2*x - 1) - 1
    elif WAVE_TYPE == 4: #white noise, note[0] does nothing in frequency
        result_wave = np.random.normal(0, 1, len(t))
    elif WAVE_TYPE == 5: #white noise filtered with sine wave. percusion with some sound height
        result_wave = np.sin(2 * np.pi * x) * np.random.normal(0, 1, len(t))
    elif WAVE_TYPE == 6: #some husky sound, and with S = -1 generate electric-themed sound
        result_wave = where(x < 1/6, -0.5+6*x, where(x < 2/6, 0.5 - 9*(x-1/6), where(x < 3/6, 1 - 9*(x-2/6), where(x < 4/6, 0.75-9*(x-3/6), where(x < 5/6, 0.75-9*(x-4/6), -0.75+1.5*(x-5/6))))))
    return result_wave

class track:
    count = 0
    def __init__(self):
        self.id = track.count
        self.wave = np.array([])
        self.length = 0
        track.count += 1

    def concatenate(self, height, t, note_duration, note_length):
        self.wave = concatenate((self.wave, VOLUME * wave_function(height, t) * interp(t / note_duration, INTERPOLATE_POINTS_X, INTERPOLATE_POINTS_Y)))
        self.length += note_length

    def ornament_note(self, height_ornament, height_main, t, ornament_ratio, note_duration, note_length):
        self.wave = concatenate((self.wave, VOLUME * (wave_function(height_ornament, t) * where(t / note_duration < ornament_ratio, 1, 0)
                                                    + wave_function(height_main, t)     * where(t / note_duration < ornament_ratio, 0, 1))
                                    * interp(t / note_duration, INTERPOLATE_POINTS_X, INTERPOLATE_POINTS_Y)))
        self.length += note_length

    def padding(self, location):
        if location > self.length:
            self.wave = np.pad(self.wave, (0, location - self.length), mode = "constant")
            self.length = location

    def restnote(self, restnote_length):
        self.wave = concatenate((self.wave, np.zeros(restnote_length)))
        self.length += restnote_length

str_to_height = {"do" : -9, "do#" : -8, "dos" : -8, "reb" : -8,
                 "re" : -7, "re#" : -6, "res" : -6, "mib" : -6,
                 "mi" : -5, "fa" : -4, "fa#" : -3, "fas" : -3,
                 "solb" : -3, "sol" : -2, "sol#" : -1, "sols" : -1,
                 "lab" : -1, "la" : 0, "la#" : 1, "las" : 1, "sib" : 1, "si" : 2}
oct_change = {"H" : 12, "L" : -12}

notes = []
TOTAL_TRACK_NUM: int
TITLE: str
SAMPLING_RATE = 44100

#----CODE_SEPARATION

tracks = []
for i in range(TOTAL_TRACK_NUM):
    tracks.append(track())

locations = np.zeros(256, dtype = int)

iterations = 0
total_notes = len(notes)
DIV_NUM = 10
milestone = set([])
for i in range(DIV_NUM):
    milestone.add(int(np.around(total_notes * i / DIV_NUM)))

for note in notes:
    iterations += 1
    if str(type(note[0])) == "<class 'int'>" or str(type(note[0])) == "<class 'float'>": #note[0] is height; note[1] is length
        note_duration = 240 * note[1] / BPM
        note_length = int(note_duration * SAMPLING_RATE)
        t = linspace(0, note_duration, note_length ,endpoint=False)
        height = note[0]
        tracks[CURRENT_TRACK_NUM].concatenate(height, t, note_duration, note_length)
    elif len(note[0]) >= 2: #note[0] is height_str; note[1] is length; note[2] is octave (void is 0); height_str(note[0]) is "do", "re", "mi" and so on, prefixed with "H" to notate higher octave and "L" to lower octave, "la" notates BASIC_FREQ
        note_duration = 240 * note[1] / BPM
        note_length = int(note_duration * SAMPLING_RATE)
        t = linspace(0, note_duration, note_length ,endpoint=False)
        height_str = note[0]
        height = 0
        while (height_str[0] == "H" or height_str[0] == "L"):
            height += oct_change[height_str[0]]
            height_str = height_str[1:]
        height += str_to_height[height_str]
        tracks[CURRENT_TRACK_NUM].concatenate(height, t, note_duration, note_length)
    elif note[0] == "o": #note with ornament, ["o", "re", 1/16, "mi", 1/4] is note with length of the quarter note with ornament length is 1/16 of the length of the note (1/4 * 1/16 = 64th note)
        note_duration = 240 * note[4] / BPM
        note_length = int(note_duration * SAMPLING_RATE)
        t = linspace(0, note_duration, note_length,endpoint=False)

        if str(type(note[1])) == "<class 'int'>" or str(type(note[1])) == "<class 'float'>":
            height_ornament = note[1]
        else:
            height_str = note[1]
            height_ornament = 0
            while (height_str[0] == "H" or height_str[0] == "L"):
                height_ornament += oct_change[height_str[0]]
                height_str = height_str[1:]
            height_ornament += str_to_height[height_str] 

        if str(type(note[3])) == "<class 'int'>" or str(type(note[3])) == "<class 'float'>":
            height_main = note[3]
        else:
            height_str = note[3]
            height_main = 0
            while (height_str[0] == "H" or height_str[0] == "L"):
                height_main += oct_change[height_str[0]]
                height_str = height_str[1:]
            height_main += str_to_height[height_str]   
        tracks[CURRENT_TRACK_NUM].ornament_note(height_ornament, height_main, t, note[2], note_duration, note_length)
    elif note[0] == "b": #BPM change by const(note[1])
        BPM = note[1]
    elif note[0] == "k": #BASIC_FREQ change by KEY
        BASIC_FREQ *= 2**(note[1]/12)
    elif note[0] == "f": #BASIC_FREQ change by freqency constant in Hz
        BASIC_FREQ = note[1]
    elif note[0] == "r": #rest note, does not sound
        note_duration = 240 * note[1] / BPM
        tracks[CURRENT_TRACK_NUM].restnote(int(note_duration * SAMPLING_RATE))
    elif note[0] == "v": #change volume; note[1] is volume, 100% is 1, 0% is 0
        VOLUME = note[1]
    elif note[0] == "t": #change wave_type
        WAVE_TYPE = note[1]
    elif note[0] == "c": #change CURRENT_TRACK_NUM
        CURRENT_TRACK_NUM = note[1]
    elif note[0] == "s": #save current length of current track, note[1] is location
        locations[note[1]] = tracks[CURRENT_TRACK_NUM].length
    elif note[0] == "l": #load location from locations and pad to current location
        tracks[CURRENT_TRACK_NUM].padding(locations[note[1]])
    elif note[0] == "i": #["i", [0, 0], [1/16, 1], [15/16, 1], [1, 0]] is default setting
        point_num = len(note) - 1
        INTERPOLATE_POINTS_X = []
        INTERPOLATE_POINTS_Y = []
        for i in range(point_num):
            INTERPOLATE_POINTS_X.append(note[i+1][0])
            INTERPOLATE_POINTS_Y.append(note[i+1][1])
    elif note[0] == "S": #change SIGMOID_NUMBER by note[1]
        if note[1] < 0:
            SIGMOID_NUMBER = 0.8 * note[1]
        elif note[1] > 0:
            SIGMOID_NUMBER = 3 * note[1]
        else:
            SIGMOID_NUMBER = 0


    if iterations in milestone:
        print(str(iterations) + " out of " + str(total_notes) + " notes done (" + str(int(np.around(100 * iterations/total_notes))) + "%), " + str(time.time() - start_time) + " sec elapsed")

max_length = 0
for i in range(TOTAL_TRACK_NUM):
    if tracks[i].length > max_length:
        max_length = tracks[i].length

for i in range(TOTAL_TRACK_NUM):
    tracks[i].padding(max_length)

merged_wave = np.zeros(max_length)
for i in range(TOTAL_TRACK_NUM):
    merged_wave += tracks[i].wave

# Convert to 16-bit PCM format, result: lowest val = -32768 @ t = 0, 1/f, 2/f, ..., highest val = 32767 @ t = 0.5/f, 1.5/f, 2.5/f, ... 
scaled_wave = np.int16(merged_wave * 32767)

# Save the WAV file & close the file
write(TITLE + ".wav", SAMPLING_RATE, scaled_wave)
print("done! (100%), " + str(time.time() - start_time) + " sec elapsed")