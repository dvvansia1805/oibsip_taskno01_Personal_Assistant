import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your voice assistant. How can I help you today?")

def takeCommand(timeout=5):
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, timeout=timeout)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.WaitTimeoutError:
        return "timeout"
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query

def listen_for_wake_word():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word 'Hey Jarvis'...")
        while True:
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio, language='en-in')
                if 'hey jarvis' in query.lower():
                    speak("Yes?")
                    return
            except Exception as e:
                print(e)
                continue

if __name__ == "__main__":
    while True:
        listen_for_wake_word()
        wishMe()
        while True:
            query = takeCommand().lower()

            if query == "timeout":
                speak("No command received. Turning off.")
                break

            # Logic for executing tasks based on query
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            elif 'open youtube' in query:
                webbrowser.open("youtube.com")
            elif 'open google' in query:
                webbrowser.open("google.com")
            elif 'play music' in query:
                music_dir = 'D:\\Songs'
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[0]))
            elif 'open spotify' in query:
                spotify_path = r"C:\Users\HP\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Spotify.lnk"
                try:
                    os.startfile(spotify_path)
                except Exception as e:
                    speak(f"Unable to open Spotify: {e}")
                    print(f"Unable to open Spotify: {e}")
            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")
            elif 'stop' in query:
                speak("Stopping. Have a good day!")
                break
