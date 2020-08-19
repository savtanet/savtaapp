import pyttsx3

def talkToUser(textToSpeak):
    engine = pyttsx3.init()
    engine.say(textToSpeak)
    engine.runAndWait()

