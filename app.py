from flask import Flask, render_template, request, redirect, url_for
import speech_recognition as sr
import pyttsx3
import webbrowser
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

def speak(text):
    print(text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_language(input_id):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak(f"Speak the {input_id.replace('_', ' ')}...")
        audio_data = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio_data).lower()
        speak("You said: " + text)
        return text
    except sr.UnknownValueError:
        speak("Sorry, could not understand audio.")
        return recognize_language(input_id)
    except sr.RequestError as e:
        speak("Could not request results; {0}".format(e))
        return recognize_language(input_id)

def detect_language(text):
    # Use Google Translate to detect the language
    detected_language = translator.detect(text).lang
    return detected_language

def translate_to_english(text):
    translated_text = translator.translate(text, dest='en').text
    return translated_text

def translate_to_target_language(text, target_language):
    translated_text = translator.translate(text, dest=target_language).text
    return translated_text

def process_text(text, language):
    if language.lower() == 'english':
        return process_english_text(text)
    else:
        return process_non_english_text(text, language)

def process_english_text(text):
    parts = text.split(' and ')
    mood, activity = parts[:2]
    return mood.strip(), activity.strip()

def process_non_english_text(text, language):
    # Translate to English for processing
    english_text = translate_to_english(text)
    mood, activity = process_english_text(english_text)
    # Translate back to the original language for display
    translated_mood = translate_to_target_language(mood, language)
    translated_activity = translate_to_target_language(activity, language)
    return translated_mood, translated_activity

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
            speak("You said: " + text)
            
            mood, activity = process_text(text, language)
            speak("Mood: " + mood)
            speak("Activity: " + activity)
            
            speak("Which platform do you want to open? (YouTube, Spotify)")
            platform_choice = platform.lower()
            
            if platform_choice == 'youtube':
                search_query = f'{mood} {activity} music {language}'
                youtube_url = f'https://www.youtube.com/results?search_query={search_query.replace(" ", "+")}'
                webbrowser.open(youtube_url)
            elif platform_choice == 'spotify':
                search_query = f'{mood} {activity} music {language}'
                spotify_url = f'https://open.spotify.com/search/{search_query.replace(" ", "%20")}'
                webbrowser.open(spotify_url)
            else:
                speak("Invalid platform choice.")
        except sr.UnknownValueError:
            speak("Sorry, could not understand audio.")
        except sr.RequestError as e:
            speak("Could not request results; {0}".format(e))
        
        speak("Do you want to search again? (yes/no):")
        choice = recognize_choice(recognizer)
        if choice.lower() != 'yes':
            return render_template("index.html")
        else:
            return redirect(url_for('index'))  # Redirect to the speech recognition page
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = False,host="0.0.0.0")
