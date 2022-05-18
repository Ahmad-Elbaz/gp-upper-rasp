#! /usr/bin/python

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import pyttsx3 as vocal
import speech_recognition as ear
import pyjokes
import datetime
import os 
import wikipedia

import pafy
import vlc
import time
import random
import re, requests, subprocess, urllib.parse, urllib.request




#thres = 0.45 # Threshold to detect object

classNames = []
classFile = "/home/mr-x/Desktop/tst2/facial-recognition-main/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/home/mr-x/Desktop/tst2/facial-recognition-main/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "//home/mr-x/Desktop/tst2/facial-recognition-main/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def play(name):
        query_string = urllib.parse.urlencode({"search_query": name})
        formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
        search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
        clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
        video = pafy.new(clip2)
        # if n==1:
        #    videolink = video.getbest()
        videolink =video.getbestaudio()
        print("audio is playing")
        media = vlc.MediaPlayer(videolink.url)
        media.play()
        time.sleep(120)
        media.stop()


def getObjects(image, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(image,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(image,box,color=(0,255,0),thickness=2)
                    cv2.putText(image,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(image,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)


    return className




def Speak(content_to_speak):#it use to speak
    mouth = vocal.init()
    mouth.setProperty('rate',130)
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



def facedetect():
		#Initialize 'currentname' to trigger only when a new person is identified.
	currentname = "unknown"
	#Determine faces from encodings.pickle file model created from train_model.py
	encodingsP = "encodings.pickle"

	# load the known faces and embeddings along with OpenCV's Haar
	# cascade for face detection
	print("[INFO] loading encodings + face detector...")
	data = pickle.loads(open(encodingsP, "rb").read())

	# initialize the video stream and allow the camera sensor to warm up
	# Set the ser to the followng
	# src = 0 : for the build in single web cam, could be your laptop webcam
	# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
	#vs = VideoStream(src=2,framerate=10).start()
	vs = VideoStream(0).start()
	time.sleep(2.0)

	# start the FPS counter
	fps = FPS().start()

	# loop over frames from the video file stream
	while True:
		# grab the frame from the threaded video stream and resize it
		# to 500px (to speedup processing)
		frame = vs.read()
		frame = imutils.resize(frame, width=500)
		# Detect the fce boxes
		boxes = face_recognition.face_locations(frame)
		# compute the facial embeddings for each face bounding box
		encodings = face_recognition.face_encodings(frame, boxes)
		names = []

		# loop over the facial embeddings
		for encoding in encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"],
				encoding)
			name = "Unknown" #if face is not recognized, then print Unknown

			# check to see if we have found a match
			if True in matches:
				# find the indexes of all matched faces then initialize a
				# dictionary to count the total number of times each face
				# was matched
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}

				# loop over the matched indexes and maintain a count for
				# each recognized face face
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1

				# determine the recognized face with the largest number
				# of votes (note: in the event of an unlikely tie Python
				# will select first entry in the dictionary)
				name = max(counts, key=counts.get)

				#If someone in your dataset is identified, print their name on the screen
				if currentname != name:
					currentname = name
					print(currentname)

			# update the list of names
			names.append(name)

		# loop over the recognized faces
		for ((top, right, bottom, left), name) in zip(boxes, names):
			# draw the predicted face name on the image - color is in BGR
			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 255, 225), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				.8, (0, 255, 255), 2)

		# display the image to our screen
		cv2.imshow("Facial Recognition is Running", frame)
		key = cv2.waitKey(1) & 0xFF

		# quit when 'q' key is pressed
		if currentname == "ahmed" or currentname == "7olom" or currentname == "ibram" or currentname == "hassan" or currentname == "eslam":
			break
		# if key == ord("q"):
		# 	break

		# update the FPS counter
		fps.update()

	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()
	fps=0	
	return currentname

# Speak("good Evening doctor mohamed")
# Speak("we just ended the face recognition and voice Recognition")
Speak("this is a small test")	
while True :
	word=Hear()
	if word=="who are you":
		about()
	elif word == "who is this":
		person= facedetect()
		Speak("this is " + person)	
	elif word=="tell me a joke":
		jokes()

	elif word=="what time is now":
		NowtTime()

	elif word=="what day is today":
		Day()
	
	elif word=="how are you":
		Fine()
	elif word=="what is this":

		cap = cv2.VideoCapture(0)
		cap.set(3,640)
		cap.set(4,480)
		success, img = cap.read()
		result = getObjects(img,0.45,0.2)
		Speak("this is a " +result)
	elif word =="can I search for something":
		Speak("sure what you want to search for ?")
		ask = Hear() 
		result = wikipedia.summary(ask, sentences = 1 ,auto_suggest=False)

		Speak(result)

	elif word == "I want to hear a song" or word == "song" or word == "hear a song":
		Speak("Sure tell me the name of the song")	
		song_name = Hear()
		play(song_name)
