# import pyaudio
import speech_recognition as sr

# mic_list = sr.Microphone.list_microphone_names()

def recogStart(mic_index):
    mic = sr.Microphone(mic_index)
    recog = sr.Recognizer()

    with mic as source:
        audio = recog.listen(source)
        try:
            voicetext = recog.recognize_google(audio, language='en')
            print(voicetext)
            return voicetext
        except:
            return ""

def get_mic_list():
    mic_list = sr.Microphone.list_microphone_names()
    return mic_list