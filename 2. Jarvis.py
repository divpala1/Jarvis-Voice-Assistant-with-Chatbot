import pyttsx3  # Module for text-to-speech
import datetime  # Module to get dates
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib  # Module for sending email.
import chatbot  # chatbot.py imported

engine = pyttsx3.init('sapi5')
# init function to get an engine instance for the speech synthesis
# The Speech Application Programming Interface or SAPI is an API developed by Microsoft to allow the use of speech recognition and speech synthesis within Windows applications.

voices = engine.getProperty('voices')

engine.setProperty('voice', voices[
    0].id)  # Sets the voice of engine to a male voice. voices[0] is male voice, and voice[1] is female voice.

# engine.setProperty('rate', 180)  # Changes the rate of speech. Default is 200.

contacts = {"name of the person": "their email id",
            "sam": "sam123@gmail.com"}  # A dictionary for the email functionality.


def speak(audio):
    engine.say(audio)
    engine.runAndWait()  # Runs the speech. All the say() texts won’t be said unless the interpreter encounters runAndWait().


def wishMe():
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        print("Good Morning!")
        speak("Good Morning!")

    elif 12 <= hour < 17:
        print("Good Afternoon!")
        speak("Good Afternoon!")

    elif 17 <= hour < 20:
        print("Good Afternoon!")
        speak("Good Afternoon!")

    elif 20 <= hour <= 24:
        print("Good Night!")
        speak("Good Night!")

    speak("Hi I am Jarvis, your personal assistant. How may I help you?")


def takeCommand():
    """
    Takes microphone input from the user and converts it into a string.
    """

    # In-case of Pyaudio installation error, follow the link below.
    # https://thetechinfinite.com/2020/07/14/how-to-install-pyaudio-module-in-python-3-0-in-windows/

    r = sr.Recognizer()  # The primary purpose of a Recognizer instance is, of course, to recognize speech.

    with sr.Microphone() as source:
        print("\nListening...")  # String printed after which the recognizer starts listening.
        r.pause_threshold = 1  # Seconds of non-speaking audio before a phrase is considered complete
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"\nUser: {query.capitalize()}")

    except:
        print("Kindly repeat sir...")
        return "None"

    return query


def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()

    file = open(r"PATH to the mail.txt file which has the username-password of your email\mail.txt",
                "r")  # Opening the txt file in which username and password of the sender is stored. First line of the text file is email-id, and the second line is password.
    l1 = file.readlines()  # Making a list with each line of the file as an element.

    server.login(l1[0], l1[1])  # l1[0] is the sender's email. l1[1] is sender's password.
    server.sendmail(l1[0], to, content)

    file.close()
    server.close()


if __name__ == '__main__':
    print("Jai Shree Krishna")
    speak("Jai Shree Krishna")
    wishMe()
    print("---Say Bye to exit---")

    while True:
        query = takeCommand().lower()

        # Logic for tasks to be executed by Jarvis

        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")  # The word 'wikipedia' is replaced with blank.
            results = wikipedia.summary(query, sentences=2)  # Returns two sentences from wikipedia.
            speak("According to Wikipedia")
            print("Jarvis:", results)
            speak(results)

        # Browser related queries

        elif "open youtube" in query:
            webbrowser.open("youtube.com")
            # If your default web-browser doesn't open while using this command then, open the source code of webbrowser module. Go to line 541 and replace the string present there with "Google\\Chrome\\Application\\chrome.exe" (Assuming your default browser is chrome).

        elif "open google" in query:
            webbrowser.open("google.com")

        elif "open instagram" in query:
            webbrowser.open("instagram.com")

        elif "open facebook" in query:
            webbrowser.open("facebook.com")

        elif "open twitter" in query:
            webbrowser.open("twitter.com")

        # Music related queries

        elif "play music" in query:
            music_dir = "PATH TO MUSIC FOLDER"  # Whenever specifying a path, remember using '\\' instead of '\' to specify sub-directories.
            songs = os.listdir(
                music_dir)  # This function returns all the files, and directories in the specified directory.
            print(songs)

            # List of extensions to be allowed to be executed.
            ext = ('.flac', '.mp3')

            while True:
                x = random.randint(0, len(songs) - 1)
                if songs[x].endswith(ext):
                    print("Playing", songs[x])
                    os.startfile(
                        os.path.join(music_dir, songs[x]))  # os.path.join combines path names into one complete path.
                    break  # Deleting this line will result in opening of multiple music player windows hence DO NOT delete it.
                else:
                    continue

        # Time related queries

        elif "time now" in query:
            strTime = datetime.datetime.now().strftime("%H:%M")  # Converts the time to string format.
            print("The time is", strTime)
            speak("Sir the time is {}".format(strTime))

        # Opening programs residing in the pc

        elif "open pycharm" in query:
            pycharmPath = "PATH TO PYCHARM"  # Example: "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2020.3.5\\bin\\pycharm64.exe"
            os.startfile(pycharmPath)

        elif "send email" in query:
            try:
                speak("To whom shall the email be addressed to?")
                receiver = takeCommand().lower()  # Names from the dictionary in line 21 are acceptable responses.
                to = contacts[receiver]

                print("Would you like to type the email or dictate it?")
                speak("Would you like to type the email or dictate it?")

                ans = takeCommand()
                if "dictate" in ans:
                    speak("What should I say?")
                    content = takeCommand()

                elif "type" in ans:
                    speak("Enter the message sir")
                    content = input("Enter message:")

                print("Sending...")
                sendEmail(to, content)
                print("Email sent.")
                speak("The email has been sent sir.")

            except:
                speak("Sorry sir. Due to an error I was unable to send the email.")

        elif "bye" in query:
            print("Have a good day sir!")
            speak("Have a good day sir!")
            exit()

        else:
            x = chatbot.answer(query)
            print("Jarvis:", x)
            speak(x)
