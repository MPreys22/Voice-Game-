import pyaudio 
import wave
import torch
import torchaudio
import torchaudio.functional as functional
import torchaudio.transforms as transforms

audio = pyaudio.PyAudio()


def voice_recording():
   
    # I really liked the documentation from the pyaudio example and decided to put it in my project. Link: https://people.csail.mit.edu/hubert/pyaudio/docs/
    print("----------------------Choose a Device---------------------")
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
            if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
    print("-------------------------------------------------------------")

voice_recording()

# Rather in pyaudio, I want to end the recording on the users notice, or if they beat the game