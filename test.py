import asyncio
from telethon import TelegramClient, events, sync
from random import uniform
import json
from dotenv import load_dotenv
import os
import time

# enable logging
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

with open('./bot_config.json', 'r') as openfile:
    config_json = json.load(openfile)
items = config_json["items"]
send_notification_to = config_json["send_notification_to"]
group_tag = config_json["group_tag"]
blacklisted_words = ["looking for","dibs"]

load_dotenv()
API_ID = os.environ["TELETHON_ID"]
API_HASH = os.environ["TELETHON_HASH"]

min_wait_s = 2
max_wait_s = 15
mute_period_s = 90
client = TelegramClient('dibsomator', API_ID, API_HASH)

# turning blacklisted and keywords to lower-case
blacklisted_words = [x.lower() for x in blacklisted_words]
for value in items.values():
    value["keywords"] = [x.lower() for x in value["keywords"]]

# listening for new messages
@client.on(events.NewMessage(chats=group_tag))
async def new_message_handler(event):
    
    a = event.sender.username

    print("got message")

client.start()
print("Dibsbot is active..")
client.run_until_disconnected()
