import speech_recognition as sr
from googletrans import Translator

def recognizeSpeech():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        print("Google Speech Recognition thinks you said in English: - ")
        text = r.recognize_google(audio, language="en-US")
        print(text)

        #translator = Translator(service_urls=['translate.google.com', 'translate.google.co.il'])
        #translation = translator.translate(text, src='en',dest='he')
        #print(translation.origin, ' -> ', translation.text)

        return text

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
