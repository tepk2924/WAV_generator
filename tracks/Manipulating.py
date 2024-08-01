import os

with open("WAV_generator.py", "r") as f:
    code = f.read()
code_splited = code.split("#----CODE_SEPARATION\n")
exec(code_splited[0])
notes = []
LLLdo, LLLdos, LLLreb, LLLre, LLLres, LLLmib, LLLmi, LLLfa, LLLfas, LLLsolb, LLLsol, LLLsols, LLLlab, LLLla, LLLlas, LLLsib, LLLsi = -45, -44, -44, -43, -42, -42, -41, -40, -39, -39, -38, -37, -37, -36, -35, -35, -34
LLdo , LLdos , LLreb , LLre , LLres , LLmib , LLmi , LLfa , LLfas , LLsolb , LLsol , LLsols , LLlab , LLla , LLlas , LLsib , LLsi  = -33, -32, -32, -31, -30, -30, -29, -28, -27, -27, -26, -25, -25, -24, -23, -23, -22
Ldo  , Ldos  , Lreb  , Lre  , Lres  , Lmib  , Lmi  , Lfa  , Lfas  , Lsolb  , Lsol  , Lsols  , Llab  , Lla  , Llas  , Lsib  , Lsi   = -21, -20, -20, -19, -18, -18, -17, -16, -15, -15, -14, -13, -13, -12, -11, -11, -10
do   , dos   , reb   , re   , res   , mib   , mi   , fa   , fas   , solb   , sol   , sols   , lab   , la   , las   , sib   , si    =  -9,  -8,  -8,  -7,  -6,  -6,  -5,  -4,  -3,  -3,  -2,  -1,  -1,   0,   1,   1,   2
Hdo  , Hdos  , Hreb  , Hre  , Hres  , Hmib  , Hmi  , Hfa  , Hfas  , Hsolb  , Hsol  , Hsols  , Hlab  , Hla  , Hlas  , Hsib  , Hsi   =   3,   4,   4,   5,   6,   6,   7,   8,   9,   9,  10,  11,  11,  12,  13,  13,  14
HHdo , HHdos , HHreb , HHre , HHres , HHmib , HHmi , HHfa , HHfas , HHsolb , HHsol , HHsols , HHlab , HHla , HHlas , HHsib , HHsi  =  15,  16,  16,  17,  18,  18,  19,  20,  21,  21,  22,  23,  23,  24,  25,  25,  26

# Parameters that you don't want to change
TITLE = os.path.splitext(os.path.basename(__file__))[0]
SAMPLING_RATE = 44100

# Parameters that preset at initial state, but may changes when the notes list is parsed
CURRENT_TRACK_NUM = 0 #track that you are adding note to, must be lower than TOTAL_TRACK_NUM, can be changed with "c"
INTERPOLATE_POINTS_X = [0,1/16,15/16,1]
INTERPOLATE_POINTS_Y = [0,1,1,0] #those points are linearly interpolated, and the resulting function starting at 0 and ending at 1 is the filter applied each note. INT_X must be increasing sequence, 0 <= (each term in INT_Y) <= 1, can be changed with "i"

# Parameters that you have to set
WAVE_TYPE = 0 #wave type(sine, square, etc), can be changed with "t"
BASIC_FREQ = 440 #440Hz = A4, can be changed with "k", "f"
VOLUME = 1 #100% at 1, 0% at 0, can be changed with "v"
BPM = 140 #how many quarter notes in a single minute, can be changed with "b"
TOTAL_TRACK_NUM = 1 #how many tracks are they, CONSTANT
SIGMOID_NUMBER = 0 #min -0.8 @ input -1, 0 @ input 0, max 3 @ input 1; significantly slower if not 0, but able to change some tone of the sound, can be changed wit "S"

#Below, Code your awesome music tracks!

import numpy as np
wave_library: dict
wave_library[7] = (lambda x: np.interp(x, [0/16, 1/16, 2/16, 3/16, 4/16, 5/16, 6/16, 7/16, 8/16,
                                           8/16, 9/16, 10/16, 11/16, 12/16, 13/16, 14/16, 15/16, 16/16],
                                          [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2,
                                           -1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2]))

wave_library[8] = (lambda x: np.where(x < 1/3, -1 + 6*x, -0.5 + 1.5*(x - 1/3)))

wave_library[9] = (lambda x: 0.25*np.sin(6*np.pi*x) + 0.25*np.sin(10*np.pi*x) + 0.5*np.sin(14*np.pi*x))

notes += [["i", [0, 0], [1/16, 1], [15/16, 1/8], [1, 0]]]
notes += [["t", 7], [do, 1/4], [re, 1/4], [mi, 1/4], [fa, 1/4], [sol, 1]]
notes += [["t", 8], [do, 1/4], [re, 1/4], [mi, 1/4], [fa, 1/4], [sol, 1]]
notes += [["t", 9], [do, 1/4], [re, 1/4], [mi, 1/4], [fa, 1/4], [sol, 1]]

#Above, Code your awesome music tracks!

exec(code_splited[1])