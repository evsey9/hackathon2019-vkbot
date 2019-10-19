import speech_recognition as sr


class S2T:
    def main():
        with sr.Microphone() as source:
             r = sr.Recognizer()
             #r.adjust_for_ambient_noise(source, duration=1)
             audio = r.listen(source)

        try:
            out = r.recognize_google(audio, language="ru-RU")
            return out
        except sr.UnknownValueError:
            re = 'invalid'
            return re
