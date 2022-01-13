import speech_recognition as sr
'''
def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something")
        audio = r.listen(source)
        voice_data = r.recognize_google(audio)
        return voice_data

'''
import speech_recognition as sr

def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something")
        r.adjust_for_ambient_noise(source, duration = 1)
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio)
            print('You said:{}'.format(voice_data))
            return voice_data
        except:
            print('sorry, could not recognize your voice')
            return None
