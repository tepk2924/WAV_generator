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
BPM = 220 #how many quarter notes in a single minute, can be changed with "b"
TOTAL_TRACK_NUM = 6 #how many tracks are they, CONSTANT
SIGMOID_NUMBER = 0 #min -0.8 @ input -1, 0 @ input 0, max 3 @ input 1; significantly slower if not 0, but able to change some tone of the sound, can be changed wit "S"

#Below, Code your awesome music tracks!
def stc(height, length_note, length_entire):
    return [[height, length_note], ["r", length_entire - length_note]]

main_chorus_A = ([[re, 1/4], [re, 1/4], [re, 1/6], [do, 1/12], [Lsib, 1/6], [re, 1/12]]
        + [[Lsib, 1/4], [Lsib, 1/4], [Lsib, 1/6], [Lla, 1/12], [Lsol, 1/6], [Lsib, 1/12]]
        + [[Lla, 1/4], [Lla, 1/6], [Lfa, 1/12],[Lla, 1/4], [Lla, 1/6], [Lfa, 1/12]]
        + [[Lsol, 1/4], [Lsol, 1/6], [Lmi, 1/12], [Lsol, 1/6], [Lla, 1/12], [do, 1/6], [mi, 1/12]]) * 2
main_chorus_B = ([[re, 1/4], [re, 1/6], [mi, 1/12], [fa, 1/4], [re, 1/4]]
        + [[Lsib, 1/6], [Lsol, 1/12], [Lsib, 1/6], [Lsol, 1/12], [fa, 1/6], [sol, 1/12], [la, 1/6], [fa, 1/12]]
        + [[Lsib, 1/4], [Lsib, 1/6], [Lsib, 1/12], [fa, 1/6], [re, 1/12], [Lla, 1/6], [Lfa, 1/12]]
        + [[Lsol, 1/6], [Lmi, 1/12], [Lsol, 1/6], [Lmi, 1/12], [Lsol, 1/6], [Lsol, 1/12], [Lsol, 1/6], [Lla, 1/12]]) * 2
percusion_initial = [["v", 0.05], [0, 1/24], ["r", 5/24], ["v", 0.2], [0, 1/24], ["r", 1/8], ["v", 0.05], [0, 1/24], ["r", 1/24]] * 16
percusion_A = [["v", 0.05], [0, 1/4], ["r", 1/4], ["v", 0.2], [0, 1/4], ["v", 0.05], [0, 1/4]] * 8
percusion_B = [["v", 0.05], [0, 1/4], [0, 1/6], [0, 1/12], ["v", 0.2], [0, 1/4], ["v", 0.05], [0, 1/4]] * 8
base_A = [[LLre, 1/2], [Lre, 1/4], [LLre, 1/4], [LLLsib, 1/2], [LLsib, 1/4], [LLLsib, 1/4], [LLfa, 1/2], [Lfa, 1/4], [LLfa, 1/4], [LLdo, 1/2], [Ldo, 1/4], [LLdo, 1/4]] * 2
base_B = [[LLre, 1/4], [Lre, 1/4], [Lre, 1/4], [LLre, 1/4], [LLLsib, 1/4], [LLsib, 1/4], [LLsib, 1/4], [LLLsib, 1/4], [LLfa, 1/4], [Lfa, 1/4], [Lfa, 1/4], [LLfa, 1/4], [LLdo, 1/4], [Ldo, 1/4], [Ldo, 1/4], [LLdo, 1/4]] * 2
beep1 = [["r", 1/2], [Hfa, 15/32], ["r", 17/32], [Hre, 15/32], ["r", 17/32], [Hsib, 15/32], ["r", 17/32], [HHdos, 15/32], ["r", 1/32]] * 2
beep2 = [["r", 17/32], [fa, 15/32], ["r", 17/32], [re, 15/32], ["r", 17/32], [sib, 15/32], ["r", 17/32], [Hdos, 15/32]] * 2

notes += [["i", [0,0], [1/16, 0.4], [1, 0.4]], ["S", 1], ["t", 1], ["v", 0.15]] #track 0, main chorus, square wave, volume 0.15
notes += (stc(re, 1/12, 1/4) + stc(re, 1/12, 1/4) + stc(re, 1/12, 1/6) + stc(do, 1/12, 1/12) + stc(Lsib, 1/12, 1/6) + stc(re, 1/12, 1/12)
        + stc(Lsib, 1/12, 1/4) + stc(Lsib, 1/12, 1/4) + stc(Lsib, 1/12, 1/6) + stc(Lla, 1/12, 1/12) + stc(Lsol, 1/12, 1/6) + stc(Lsib, 1/12, 1/12)
        + stc(Lla, 1/12, 1/4) + stc(Lla, 1/12, 1/6) + stc(Lfa, 1/12, 1/12) + stc(Lla, 1/12, 1/4) + stc(Lla, 1/12, 1/6) + stc(Lfa, 1/12, 1/12)
        + stc(Lsol, 1/12, 1/4) + stc(Lsol, 1/12, 1/6) + stc(Lmi, 1/12, 1/12) + stc(Lsol, 1/12, 1/6) + stc(Lla, 1/12, 1/12) + stc(do, 1/12, 1/6) + stc(mi, 1/12, 1/12)) * 2
notes += [["s", 0],["S", .5], ["i", [0,0], [1/32, 1], [1,.3]]]
notes += main_chorus_A
notes += [["s", 1]]
notes += main_chorus_B
notes += [["s", 2]]
notes += main_chorus_A
notes += [["s", 3]]
notes += main_chorus_B

notes += [["c", 1], ["i", [0, 0], [1/16, 1], [1, 1]], ["S", 0], ["t", 4], ["v", 0.05]] #track 1, percusion, white noise, volume 0.05
notes += percusion_initial
notes += [["l", 0], ["i", [0, 0], [1/32, 1], [1, 0]]]
notes += percusion_A
notes += [["l", 1]]
notes += percusion_B
notes += [["l", 2]]
notes += percusion_A
notes += [["l", 3]]
notes += percusion_B

notes += [["c", 2], ["i", [0, 0], [1/16, 1], [1, 0]], ["S", -1], ["t", 6], ["v", 0.15]] #track 2, base, wave_type 6(S=-1), volume 0.15
notes += [["l", 0]]
notes += base_A
notes += [["l", 1]]
notes += base_B
notes += [["l", 2]]
notes += base_A
notes += [["l", 3]]
notes += base_B

notes += [["c", 3], ["i", [0, 1], [1/16, 1], [2/16, 0], [3/16, 0.8], [4/16, 0], [5/16, 0.8**2], [6/16, 0], [7/16, 0.8**3], [8/16, 0], [9/16, 0.8**4], [10/16, 0.8**5], [11/16, 0], [1, 0]], ["S", 0], ["t", 1], ["v", 0.15]] #track 3, beep1, square, volume 0.15
notes += [["l", 0]]
notes += beep1
notes += [["l", 1]]
notes += beep1
notes += [["l", 2]]
notes += beep1
notes += [["l", 3]]
notes += beep1

notes += [["c", 4], ["i", [0, 1], [1/16, 1], [2/16, 0], [3/16, 0.8], [4/16, 0], [5/16, 0.8**2], [6/16, 0], [7/16, 0.8**3], [8/16, 0], [9/16, 0.8**4], [10/16, 0.8**5], [11/16, 0], [1, 0]], ["S", 0], ["t", 1], ["v", 0.15]] #track 4, beep2, square, volume 0.15
notes += [["l", 0]]
notes += beep2
notes += [["l", 1]]
notes += beep2
notes += [["l", 2]]
notes += beep2
notes += [["l", 3]]
notes += beep2

#Above, Code your awesome music tracks!

exec(code_splited[1])