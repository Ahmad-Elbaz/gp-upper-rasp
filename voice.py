import pyttsx3 as vocal
import speech_recognition as ear
import pyjokes
import datetime




def Speak(content_to_speak):#it use to speak
    mouth = vocal.init()
    mouth.setProperty('rate',150)
    mouth.say(content_to_speak)
    mouth.runAndWait()#speak organ is formed..................
def Hear():#it regcognition voices 
    #intital the speech recognition organ
    r = ear.Recognizer()
    # open the robert ears ...
    with ear.Microphone() as source:     
        print("Listening...")
        r.pause_threshold = 1 #it decide to open audio inputs 
        audio = r.listen(source) #it is process hearing by the rober
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language ='en-in')# it convert the audio to text ...
        print(f"User said: {query}\n")
    except Exception as e: #exception case was handle by this
        print(e)
        value = "Unable to Recognize your voice"    
        print(value) 
        return value # hear organ is formed .....................
    return query #return in text format 
#it say the joke be is low 
def jokes():
    Speak("I want to say jokes really")
    Speak(pyjokes.get_joke())
#it will wish the user .....
def WishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        Speak("Good Morning Sir !")
        print("Good Morning Sir !")
    elif hour >= 12 and hour < 18:
        Speak("Good Afternoon Sir !")
        print("Good Afternoon Sir !")
    else:
        Speak("Good Evening Sir !") 
        print("Good Evening Sir !") 
#Robert say it self
def about():
    Speak("I am Ziko Version three Point three Point One") 
    Speak("I Can assist you ")             
# it will say time......
def NowtTime():
    Time = datetime.datetime.now().strftime("%X")
    print(f"Sir the time is {Time}") 
    Speak(f"Sir the time is {Time}")
# it will say day
def Day():
    Time = datetime.datetime.now().strftime("%a")
    Speak(f"Sir the Day is {Time}")
# it say if user say 
def Fine():
    Speak("I am Fine , Thank you")
    Speak("How are you ")

# x=0
# while True :
    
#     word = Hear()
#     if word== "tell me a joke":
#         jokes()

    #         x+=1
    #         jokes()
    # elif (word == "who are you"):
    #         x+=1
    #         about()
    # elif (word == "what time is now"):
    #         x+=1
    #         NowtTime()

