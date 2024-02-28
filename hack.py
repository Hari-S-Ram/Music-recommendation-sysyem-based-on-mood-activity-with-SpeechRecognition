app.template_folder = 'hello'
from flask import Flask, render_template, request
import speech_recognition as sr
import pyttsx3
import webbrowser

app = Flask(__name__)

def speak(text):
    print(text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_language():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Speak the language you want to search in...")
        audio_data = recognizer.listen(source)

    try:
        language = recognizer.recognize_google(audio_data).lower()
        speak("You chose:" + language)
        return language
    except sr.UnknownValueError:
        speak("Sorry, could not understand audio.")
        return recognize_language()
    except sr.RequestError as e:
        speak("Could not request results; {0}".format(e))
        return recognize_language()

def process_text(text):
    parts = text.split(' and ')
    mood, activity = parts[:2]
    return mood.strip(), activity.strip()

def recognize_choice(recognizer):
    with sr.Microphone() as source:
        audio_data = recognizer.listen(source)
    try:
        choice = recognizer.recognize_google(audio_data).lower()
        return choice
    except sr.UnknownValueError:
        speak("Sorry, could not understand audio.")
        return recognize_choice(recognizer)
    except sr.RequestError as e:
        speak("Could not request results; {0}".format(e))
        return recognize_choice(recognizer)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        language = request.form["language"]
        mood_activity = request.form["mood_activity"]
        platform = request.form["platform"]
        
        speak(f"You chose {language}.")
        
        recognizer = sr.Recognizer()
        try:
            text = mood_activity
            speak("You said:" + text)
            
            mood, activity = process_text(text)
            speak("Mood: " + mood)
            speak("Activity: " + activity)
            
            speak("Which platform do you want to open? (YouTube, Spotify, Vimeo, Dailymotion, Twitch, BitChute, PeerTube, LBRY/Odysee, Metacafe, Veoh, Rumble, Internet Archive)")
            platform_choice = platform.lower()
            
            if platform_choice == 'youtube':
                search_query = f'{mood} {activity} music {language}'
                youtube_url = f'https://www.youtube.com/results?search_query={search_query.replace(" ", "+")}'
                webbrowser.open(youtube_url)
            elif platform_choice == 'spotify':
                search_query = f'{mood} {activity} music {language}'
                spotify_url = f'https://open.spotify.com/search/{search_query.replace(" ", "%20")}'
                webbrowser.open(spotify_url)
            elif platform_choice in ['vimeo', 'dailymotion', 'twitch', 'bitchute', 'peertube', 'lbry', 'odysee', 'metacafe', 'veoh', 'rumble', 'internet archive']:
                search_query = f'{mood} {activity} video {language}'
                platform_url = f'https://{platform_choice}.com/search?q={search_query.replace(" ", "+")}'
                webbrowser.open(platform_url)
            else:
                speak("Invalid platform choice.")
        except sr.UnknownValueError:
            speak("Sorry, could not understand audio.")
        except sr.RequestError as e:
            speak("Could not request results; {0}".format(e))
        
        speak("Do you want to search again? (yes/no):")
        choice = recognize_choice(recognizer)
        if choice.lower() != 'yes':
            return render_template("index.html", title="Speech Recognition App")
    
    return render_template("index.html", title="Speech Recognition App")

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        language = request.form["language"]
        mood_activity = request.form["mood_activity"]
        platform = request.form["platform"]
        
        speak(f"You chose {language}.")
        
        recognizer = sr.Recognizer()
        try:
            text = mood_activity
            speak("You said:" + text)
            
            mood, activity = process_text(text)
            speak("Mood: " + mood)
            speak("Activity: " + activity)
            
            speak("Which platform do you want to open? (YouTube, Spotify, Vimeo, Dailymotion, Twitch, BitChute, PeerTube, LBRY/Odysee, Metacafe, Veoh, Rumble, Internet Archive)")
            platform_choice = platform.lower()
            
            if platform_choice == 'youtube':
                search_query = f'{mood} {activity} music {language}'
                youtube_url = f'https://www.youtube.com/results?search_query={search_query.replace(" ", "+")}'
                webbrowser.open(youtube_url)
            elif platform_choice == 'spotify':
                search_query = f'{mood} {activity} music {language}'
                spotify_url = f'https://open.spotify.com/search/{search_query.replace(" ", "%20")}'
                webbrowser.open(spotify_url)
            elif platform_choice in ['vimeo', 'dailymotion', 'twitch', 'bitchute', 'peertube', 'lbry', 'odysee', 'metacafe', 'veoh', 'rumble', 'internet archive']:
                search_query = f'{mood} {activity} video {language}'
                platform_url = f'https://{platform_choice}.com/search?q={search_query.replace(" ", "+")}'
                webbrowser.open(platform_url)
            else:
                speak("Invalid platform choice.")
        except sr.UnknownValueError:
            speak("Sorry, could not understand audio.")
        except sr.RequestError as e:
            speak("Could not request results; {0}".format(e))
        
        speak("Do you want to search again? (yes/no):")
        choice = recognize_choice(recognizer)
        if choice.lower() != 'yes':
            return render_template("index.html", title="Speech Recognition App")
    
    return render_template("index.html", title="Speech Recognition App")
