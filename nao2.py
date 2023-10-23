import numpy
import naoqi
import openai

from naoqi import ALProxy

#Robot Connection
robot_ip = "127.0.0.1"  # Replace with your robot's IP address
port = 9559  # Default port; change if necessary
tts = ALProxy("ALTextToSpeech", robot_ip, port)
asr = ALProxy("ALSpeechRecognition", robot_ip, port)

#Made by Billy J 2023
#Digital Technologies
#2.7.11 NAO Communication
#2.7.12 NAO Movement
#2.7.13 NAO Vision
#2.7.14 NAO Speech
#2.7.15 NAO Speech Recognition
def onWordRecognized(value):
    # The value will be a list where the first element is the recognized word, and the second element is the confidence score
    recognized_word = value[0]
    print("Recognized: {}".format(recognized_word))

# Subscribe to the WordRecognized event
asr.setLanguage("English")
asr.setWordListAsVocabulary(["yes", "no"])  # Replace with your desired vocabulary
asr.subscribe("WordRecognition")
memory = ALProxy("ALMemory", robot_ip, port)
memory.subscribeToEvent("WordRecognized", "onWordRecognized", onWordRecognized.__name__)

#2.7.16 NAO Speech Synthesis

print("Script Started")
tts.say("Hello, I am NAO")
print("Said Hello, I am NAO")

