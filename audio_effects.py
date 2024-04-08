from os.path import isfile
from pydub import AudioSegment
import soundfile as sf
from pedalboard import Pedalboard, Reverb
from os import remove as removeFile


# settings.py content
inputFile = r"Music/testsong1"  # Name of the file to import
outputFile = r"Music/music8d"      # Name of the file to export
timeLtoR = 1000  # Time taken for audio to move left -> right in ms
jumpPercentage = 5  # % of dist b/w L-R to jump at a time
panBoundary = 100  # % of dist from center that audio source can go
volumeMultiplier = 6  # Max volume DB increase at edges
speedMultiplier = 0.92  # Slowdown audio; 1.0=original, 0.5=half speed


# loadSound.py content
def loadSound(inputFile):
    if isfile(inputFile):
        return AudioSegment.from_mp3(inputFile)
    elif isfile(inputFile + ".wav"):
        return AudioSegment.from_wav(inputFile + ".wav")
    else:
        print("Source music file not found!")
        exit()


# effect8d.py content
def panArray():
    piecesCtoR = panBoundary / jumpPercentage
    piecesLtoR = piecesCtoR * 2
    pieceTime = int(timeLtoR / piecesLtoR)
    pan = []
    left = -panBoundary
    while left <= panBoundary:
        pan.append(left)
        left += jumpPercentage
    pan = [x / 100 for x in pan]
    return pan, pieceTime


def effect8d(sound):
    pan, pieceTime = panArray()
    sound8d = sound[0]
    panIndex = 0
    iteratePanArrayForward = True
    for time in range(0, len(sound) - pieceTime, pieceTime):
        piece = sound[time: time + pieceTime]
        if panIndex == 0:
            iteratePanArrayForward = True
        if panIndex == len(pan) - 1:
            iteratePanArrayForward = False
        volAdjust = volumeMultiplier - (abs(pan[panIndex]) / (panBoundary / 100) * volumeMultiplier)
        piece -= volAdjust
        pannedPiece = piece.pan(pan[panIndex])
        if iteratePanArrayForward:
            panIndex += 1
        else:
            panIndex -= 1
        sound8d = sound8d + pannedPiece
    return sound8d


# slow.py content
def effectSlowedDown(sound):
    soundSlowedDown = sound._spawn(
        sound.raw_data,
        overrides={"frame_rate": int(sound.frame_rate * speedMultiplier)},
    )
    soundSlowedDown.set_frame_rate(sound.frame_rate)
    return soundSlowedDown


# reverb.py content
def tempAudioFile(sound):
    with open("temp" + ".wav", "wb") as out_f:
        sound.export(out_f, format="wav")
    audio, sampleRate = sf.read("temp" + ".wav")
    return audio, sampleRate


def effectReverb(sound):
    sound, sampleRate = tempAudioFile(sound)
    addReverb = Pedalboard([Reverb(room_size=0.8, damping=1, width=0.5, wet_level=0.3, dry_level=0.8)])
    reverbedSound = addReverb(sound, sample_rate=sampleRate)
    return reverbedSound, sampleRate


# saveSound.py content
def saveSound(sound, sampleRate, outputFile):
    with sf.SoundFile("temp2" + ".wav", "w", samplerate=sampleRate, channels=sound.shape[1]) as f:
        f.write(sound)
    AudioSegment.from_wav("temp2" + ".wav").export(outputFile, format="mp3")
    removeFile("temp2" + ".wav")
    removeFile("temp.wav")

