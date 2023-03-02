import speech_recognition as sr # our speech recognition module
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time
from selenium import webdriver # most important module, make sure to visit any online tutorials for installation guide
from selenium.webdriver.chrome.options import Options # another important module
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def addressbook(): # if you have a preloaded contacts file, you are able to link a name and their contact. This allows you to send a message to the person just by telling the voice assistant the name.
    file = open('contacts.csv', 'r')
    import csv
    reader = csv.reader(file)
    address_book = []
    for item in reader:
        del(item[1:30])
        address_book.append(item)

    address_book_dic = {}
    for item in address_book:
        address_book_dic.update({item[0]:item[1]})
    return(address_book_dic)


def whatsapp(text, name): # function for whatsapp web, not the app
    options = Options()
    options.add_argument("CHANGME") # change this to your own directory
    options.add_argument('--profile-directory=Profile 2')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://web.whatsapp.com/%22")
    time.sleep(20) # it takes a while to load
    user = driver.find_element_by_xpath('//span[@title="{}"][@dir="auto"]'.format(name))
    user.click()
    #find out the whatsapp message box using the inspect element and paste it in the ' '
    msg_box = driver.find_element_by_class_name('CHANGEME')
    msg_box.send_keys(text)
    #find out the whatsapp enter button using inspect element and paste it in the ' '
    driver.find_element_by_class_name('CHANGEME').click()


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command


def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'whatsapp' in command:
        message = "Hi, I am Jarvis, an online assistant. This is an automated message." # initiation message
        victim = ""
        raw_message = command.replace('whatsapp', '')
        count_loop = 0
        for n in raw_message.split():
            count_loop += 1
            if count_loop == 1:
                victim = n
        print(victim.capitalize())
        message += raw_message.replace(victim, '')
        talk("Sir, do you want me to message {}".format(victim))
        answer = take_command()
        print(answer)
        if answer == "yes":
            whatsapp(message, victim.capitalize())
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'date' in command:
        talk('sorry, I have a headache')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'exit' in command:
        quit()
    else:
        talk('Please say the command again.')


today = datetime.date.today()
now = datetime.datetime.now()
current_time = datetime.datetime.now().strftime('%I:%M %p')
hour = now.hour
if hour < 12:
    greeting = "Good morning"
elif hour < 18:
    greeting = "Good afternoon"
else:
    greeting = "Good night"
talk("{},sir. Today is {} and the time now is {}. What would you like me to do today?".format(greeting, today, current_time))
while True:
    run_alexa()
