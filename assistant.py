print("////////////////////I am your voice Assistant//////////////////////")
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
from datetime import datetime

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Function to listen to the user's voice and return the recognized command
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Increased timeout and phrase_time_limit
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")  # Print what the user said
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return ""
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return ""

# Function to make the assistant speak
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to open a website or application
def open_item(command):
    if "open" in command:
        item = command.replace("open", "").strip()
        print(f"Attempting to open: {item}")  # Debugging line

        # Check for specific commands to open common websites
        if "google" in item:
            speak("Opening Google")
            webbrowser.open("http://www.google.com")
        elif "youtube" in item:
            speak("Opening YouTube")
            webbrowser.open("http://www.youtube.com")
        elif "facebook" in item:
            speak("Opening Facebook")
            webbrowser.open("http://www.facebook.com")
        else:
            # For other websites or applications
            if "." in item:
                url = f"http://{item}"
                speak(f"Opening {item}")
                webbrowser.open(url)
            else:
                # Assuming it's an application
                speak(f"Opening {item}")
                os.system(f"start {item}")  # For Windows; use 'open' for Mac, or adjust for Linux
    else:
        speak("Sorry, I can't do that.")

# Main function that processes voice commands
def main():
    speak("Hello! I am your assistant. How can I assist you today?")
    
    while True:
        command = listen()

        if command:
            if "hello" in command:
                speak("Hello! How can I help you?")
            
            elif "time" in command:
                now = datetime.now()
                speak(f"The current time is {now.strftime('%H:%M')}")
    
            elif "date" in command:
                today = datetime.today()
                speak(f"Today's date is {today.strftime('%B %d, %Y')}")
    
            elif "open" in command:
                open_item(command)
    
            elif "exit" in command or "stop" in command:
                speak("Goodbye!")
                break
    
            else:
                speak("I'm sorry, I didn't catch that. Please try again.")

if __name__ == "__main__":
    main()
