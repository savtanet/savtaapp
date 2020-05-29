import pyttsx3
from SpeechRecognition import recognizeSpeech


def talkToUser(textToSpeak):
    engine = pyttsx3.init()
    engine.say(textToSpeak)
    engine.runAndWait()


# just a default structure
def welcomeUser():
    talkToUser("Welcome savta, how i can help you today?")
    recognizeSpeech()
    talkToUser("Thank you for using our services, goodbye")
