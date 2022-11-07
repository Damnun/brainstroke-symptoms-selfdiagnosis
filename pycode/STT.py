# TODO : https://cslife.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-Flask%EB%A1%9C-%EB%A7%88%EC%9D%B4%ED%81%AC%EC%97%90%EC%84%9C-%EC%9E%85%EB%A0%A5%EB%B0%9B%EC%9D%80-%EC%9D%8C%EC%84%B1%EC%9D%84-%ED%85%8D%EC%8A%A4%ED%8A%B8%EB%A1%9C-%EB%9D%84%EC%9A%B0%EB%8A%94-%EC%9B%B9%ED%8E%98%EC%9D%B4%EC%A7%80-%EB%A7%8C%EB%93%A4%EA%B8%B0
# TODO : 주변 소음 때문에 몇 초 이후 자르기 or 버튼으로 자르기
import pyaudio
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
    try:
        transcript = r.recognize_google(audio, language="ko-KR")
        print("Google Speech Recognition thinks you said " + transcript)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))