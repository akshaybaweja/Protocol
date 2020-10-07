import os
import logging
from aiogram import Bot, Dispatcher, executor, types
import paralleldots
import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt

# ParallelDots for Emotion Analysis
api_key = os.environ['ParallelDots']
paralleldots.set_api_key( api_key )

# MQTT Initializations
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.connect("mqtt.eclipse.org", 1883, 60)

# Telegram Credentials
API_TOKEN = os.environ['telegram_bot_api_token']
telegramImageURL = 'https://api.telegram.org/file/bot'+API_TOKEN+'/'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def image_handler(message: types.Message):
    name = message["from"]["first_name"] + " " + message["from"]["last_name"]
    print("Skipping analysis of photo message sent by ", name)

@dp.message_handler()
async def echo(message: types.Message):
    name = message["from"]["first_name"] + " " + message["from"]["last_name"]
    text = message.text
    chatID = message.chat.id

    # Get Emotion
    apiResponse = paralleldots.emotion(text)
    apiResponse = apiResponse["emotion"]
    emotion = max(apiResponse, key=apiResponse.get)
    if(apiResponse[emotion] >= 0.9): # Publish emotion to MQTT only when emotion is extereme 90% or more
        print(name, "said", text, "; Emotion: " ,emotion)
        # Publish to MQTT Server
        (rc, mid) = mqttc.publish(emotion, "esprotocol", qos=2)

# MQTT Function Definitions
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    mqttc.loop_start()