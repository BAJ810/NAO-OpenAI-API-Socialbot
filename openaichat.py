import paho.mqtt.client as mqtt
import openai
import speech_recognition as sr
import os
import time

# Initialize speech recognizer
r = sr.Recognizer()

#MQTT settings
MQTT_ip = "localhost"
MQTT_port = 1949
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_ip, MQTT_port)

average_time_per_word = 0.3
message_received = False

# OpenAI setup
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")
chat_history = ""
conversation_history = []
session_id = None
assistant_id = os.environ.get("OPENAI_ASSISTANT_KEY")
if not assistant_id:
    print("The OPENAI_ASSISTANT_KEY environment variable is not set.")

def estimate_speaking_time(text):
    words = text.split()
    # Estimate the time to speak the text
    estimated_time = len(words) * average_time_per_word
    return estimated_time

# Define a callback for when the robot is done speaking
def on_done_speaking(client, userdata, msg):
    global message_received
    if msg.payload.decode() == "done":
        print("Robot done speaking. Ready for next action.")
        message_received = True

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global message_received
    print(f"Message received: {msg.payload.decode()}")
    if msg.topic == "nao/done_speaking":
        message_received = True

# Create an MQTT client instance
mqtt_client = mqtt.Client()

# Assign event callbacks
mqtt_client.on_message = on_message

# Connect to the broker
mqtt_client.connect(MQTT_ip, MQTT_port, 60)

# Subscribe to the topic
mqtt_client.subscribe("nao/done_speaking")
mqtt_client.message_callback_add("nao/done_speaking", on_done_speaking)

mqtt_client.loop_start()

# Subscribe to the topic where we'll receive the done speaking notification

# Setup the MQTT client and callbacks
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_ip, MQTT_port)

# Subscribe to the topic where we'll receive the done speaking notification
mqtt_client.subscribe("nao/done_speaking")
mqtt_client.message_callback_add("nao/done_speaking", on_done_speaking)

system_message = {
    'role': 'system',
    'content': "You are Rosey the Robot, the friendly NAO v5 robot at Bialik College, not only assists with classroom activities but also makes an effort to get to know the students. When interacting, Rosey should ask for the student's name and year level. This allows for more personalized assistance and helps build a connection with the students. Rosey should use this information to tailor the conversation and educational support to the student's specific needs and level. Along with providing academic help, Rosey's approachable and relatable communication style should make the students feel comfortable and valued. Rosey maintains a positive, encouraging tone throughout, ensuring the students feel supported in their learning journey. Here is the chat history: "
}

# Use the default microphone as the audio source
mqtt_client.loop_start()

# List all microphone names to find the index of Wave Link Stream
mics = sr.Microphone.list_microphone_names()
wave_link_index = None
for index, name in enumerate(mics):
    if "Wave Link Stream" in name:
        wave_link_index = index
        break

# Check if the Wave Link Stream microphone was found
if wave_link_index is not None:
    print("Wave Link Stream microphone found.")
else:
    print("Wave Link Stream microphone not found. Using default microphone.")

print("You can start speaking to the chatbot now. Say 'stop' to end the conversation.")
while True:
    try:
        if wave_link_index is not None:
            with sr.Microphone(device_index=wave_link_index) as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Calibrated for ambient noise, ready to listen...")
                r.pause_threshold = 1.5  # Wait for a pause in speech
                print("Listening...")
                mqtt_client.publish("nao/listening", "start")
                audio = r.listen(source)
        else:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Calibrated for ambient noise, ready to listen...")
                r.pause_threshold = 1.5 # Wait for a pause in speech
                print("Listening...")
                mqtt_client.publish("nao/listening", "start")
                audio = r.listen(source)

        mqtt_client.publish("nao/thinking", "start")
        print("Recognizing...")  # This line should be printed after 'r.listen' has collected the audio data
        speech_to_text = r.recognize_google(audio)
        mqtt_client.publish("nao/speaking", "start")
        print("You said: " + speech_to_text)

        # Check if the user said 'stop'
        if speech_to_text.lower() == 'stop':
            break

        conversation_history.append({'role': 'user', 'content': speech_to_text})

        # Prepare the message for the Assstant
        #user_message = {
          #  'role': 'user',
         #   'content': speech_to_text
        #}

        # Concatenate system_message and conversation_history
        all_messages = [system_message] + conversation_history

        # Get the response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can specify the model if required
            temperature=0.4,
            top_p=.25,
            max_tokens=150,
            messages = all_messages
            )
    
        # Extract the text of the response
        ai_text = response.choices[0].message['content'].strip()

        # Print out the ChatGPT response
        print(ai_text)
        mqtt_client.publish("nao/tts", ai_text)
        estimated_time = estimate_speaking_time(ai_text)
        print(f"Estimated speaking time: {estimated_time} seconds")
        while not message_received:
            time.sleep(0.1)  # You can implement a better waiting logic here
        #time.sleep(estimated_time)
        #is_speaking = True
        #while is_speaking:
        #    time.sleep(0.1)
        message_received = False
        #memory
        conversation_history.append({'role': 'assistant', 'content': ai_text})


    except sr.UnknownValueError:
        # Speech was unintelligible
        print("Sorry, I did not understand that. Please try again.")
    except sr.RequestError as e:
        # Could not request results from Google Speech Recognition service
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except openai.error.OpenAIError as e:
        # OpenAI API error
        print(f"Error with OpenAI API: {e}")

# End the MQTT client loop
mqtt_client.loop_stop()
mqtt_client.disconnect()
print("Script terminated by user.")
print("Conversation ended.")
