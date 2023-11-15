import paho.mqtt.client as mqtt
from naoqi import ALProxy, ALModule, ALBroker
import time
import os

nao_ip = "192.168.192.208"
#os.environ.get("NAO_IP")
if not nao_ip:
    raise ValueError("The NAO IP is not set.")
nao_port = 9559

#MQTT settings
mqtt_ip = "localhost"
mqtt_port = 1949 #mosquitto port - to change: mosquito -p 1949
last_message_time = 0
message_interval = 1  # Only allow messages every 1 seconds

# Set up the NAOqi proxy's
tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)
motion_proxy = ALProxy("ALMotion", nao_ip, nao_port)
awareness = ALProxy("ALBasicAwareness", nao_ip, nao_port)
motion = ALProxy("ALMotion", nao_ip, nao_port)
autonomous_life = ALProxy("ALAutonomousLife", nao_ip, nao_port)
posture = ALProxy("ALRobotPosture", nao_ip, nao_port)
speech_proxy = ALProxy("ALAnimatedSpeech", nao_ip, nao_port)
system_proxy = ALProxy("ALSystem", nao_ip, nao_port)
laser = ALProxy("ALLaser", nao_ip, nao_port)
people_perception = ALProxy("ALPeoplePerception", nao_ip, nao_port)
memory = ALProxy("ALMemory", nao_ip, nao_port)
leds = ALProxy("ALLeds", nao_ip, nao_port)
audio_device = ALProxy("ALAudioDevice", nao_ip, nao_port)

# Listening behavior
def start_listening():
    leds.fadeRGB("FaceLeds", "blue", 0.5)  # Set eyes to blue
    # Optionally play a listening sound
    audio_device.playFile("g:\My Drive\School\Year 9 2023\Digital Technologies\listeningsound.wav")

# Thinking behavior
def start_thinking():
    leds.fadeRGB("FaceLeds", "yellow", 0.5)  # Set eyes to yellow
    # Optionally play a thinking sound
    #audio_device.playFile("/path/to/thinking/sound.wav")

# Speaking behavior
def start_speaking():
    leds.fadeRGB("FaceLeds", "green", 0.5)  # Set eyes to green
    # Optionally play a speaking sound before actual speech
    #audio_device.playFile("/path/to/speaking/sound.wav")

# Reset LEDs to default behavior
def reset_leds():
    leds.reset("FaceLeds")

#class SpeechHandler(ALModule):
#    def __init__(self, name):
#        ALModule.__init__(self, name)
#        global memory
#        memory.subscribeToEvent("ALTextToSpeech/TextDone", self.getName(), "onTextDone")
#
#    def onTextDone(self, eventName, value, subscriberIdentifier):
#        if value:  # Check if the speaking task is done
#            print("Speech has finished")
#            global mqtt_client
#            mqtt_client.publish("nao/done_speaking", "done")
#            memory.unsubscribeToEvent("ALTextToSpeech/TextDone", self.getName())


#    def say_with_gesture(self, text):
#        self.speech_proxy.say(text)  # This will use animated speech


naoqiversion = system_proxy.systemVersion()
print("NAOqi version: ", naoqiversion)

tts.say("NAO q i online. Version:  Sleep then starting Motors - ChatGPT NAO Robot")
print("said NAO q i online. Version:  Sleep then starting Motors - ChatGPT NAO Robot")
leds.rasta(3.0)

#myBroker = ALBroker("myBroker", "0.0.0.0", 0, nao_ip, nao_port)
#speech_handler = SpeechHandler("SpeechHandler")

autonomous_life.setState("disabled")

time.sleep(1) #motors enable time


motion_proxy.stiffnessInterpolation("Head", 1.0, 1.0)
print("Motor Successful - Head")
motion_proxy.stiffnessInterpolation("Legs", 1.0, 1.0)
print("Motor Successful - Legs")
motion_proxy.stiffnessInterpolation("RArm", 1.0, 1.0)
print("Motor Successful - RArm")

motion_proxy.stiffnessInterpolation("LShoulderRoll", 1.0, 1.0)
print("Motor Successful - LShoulderRoll")
motion_proxy.stiffnessInterpolation("LShoulderPitch", 1.0, 1.0)
print("Motor Successful - LShoulderPitch")
motion_proxy.stiffnessInterpolation("LElbowYaw", 1.0, 1.0)
print("Motor Successful - LElbowYaw")
motion_proxy.stiffnessInterpolation("LElbowRoll", 1.0, 1.0)
print("Motor Successful - LElbowRoll")
motion_proxy.stiffnessInterpolation("LWristYaw", 1.0, 1.0)
print("Motor Successful - LWristYaw")

print("Motors on")

# Set the robot to an idle posture
posture.goToPosture("Stand", 0.5)

# Enable breathing animations on body parts
motion.setBreathEnabled("Body", True)

# Enable basic awareness
awareness.setEngagementMode("FullyEngaged")
awareness.startAwareness()

# Animated speech configuration
configuration = {"bodyLanguageMode":"random"}

try:
    tts.say("Ready to chat.")
except Exception as e:
    print("An error occurred while trying to speak:", e)

# MQTT callback function
def on_message(client, userdata, msg):
    global last_message_time
    current_time = time.time()

    # Immediate actions for state changes
    if msg.topic == "nao/listening":
        start_listening()
    elif msg.topic == "nao/thinking":
        start_thinking()
    else:
        start_speaking()
        speech_proxy.say(msg.payload, configuration) #add ",configuration" to add gestures
        mqtt_client.publish("nao/done_speaking", "done")


# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_ip, mqtt_port)

# Subscribe to the topic
mqtt_client.subscribe("nao/tts")

# Start the MQTT client loop
mqtt_client.loop_forever()