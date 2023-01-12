import asyncio
from telethon import TelegramClient, events, sync
from random import uniform
import json
from dotenv import load_dotenv
import os
import time

# enable logging
import logging
import sys

file_handler = logging.FileHandler(filename='log.txt')
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.INFO, 
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    handlers=handlers
)

#logger = logging.getLogger('LOG')


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
    if event.photo:
        has_photo = True
    else:
        has_photo = False

    cleaned_text = event.raw_text.lower().replace('\n', ' ')

    # if has photo and doesn't contain blacklisted words
    if has_photo and all((elem not in cleaned_text) for elem in blacklisted_words):
        # look for matching keywords
        already_found_match = False
        for item in items.values():
            if item["active"]:
                for keyword in item["keywords"]:
                    if keyword in cleaned_text and not_part_of_word(keyword, cleaned_text):
                        # if price is right
                        price = determine_price(cleaned_text)
                        if (price and price <= item["max_price"]) or (not price and item["dibs_to_unknown_price"]):
                            if not item["notify_only"]:
                                await dib_item(item, keyword, event)
                            else:
                                await notify_user(item["notify_only"], keyword, event)

                            already_found_match = True
                            break
            if already_found_match:
                break
    logging.info("Got message.")

def not_part_of_word(keyword, text):
    pre_index = text.index(keyword)-1
    post_index = text.index(keyword)+len(keyword)
    pre_ok = not text[pre_index].isalpha() if pre_index >= 0 else True
    post_ok = not text[post_index].isalpha() if post_index < len(text) else True

    return pre_ok and post_ok

def deactivate(item_to_change):
    for item in items.values():
        if item == item_to_change:
            item["active"] = False

    config_json["items"] = items
    json_object = json.dumps(config_json, indent=4)

    with open("./bot_config.json", "w") as outfile:
        outfile.write(json_object)
        

def determine_price(cleaned_text):
    # the function looks for a number (integer or float) directly before any of these substrings:
    price_signs = [" euro"," euros"," e"," €","euro","euros","e","€"]

    # get indices after numbers
    sign_starting_indices = []
    for index, char in enumerate(cleaned_text[::-1]):
        if char.isdigit():
            sign_starting_indices.append( len(cleaned_text)-index )

    # get the index after which one of the price signs occur
    price_ending_index = None
    for index in sign_starting_indices:
        for sign in price_signs:
            if cleaned_text[index:index+len(sign)] == sign:
                price_ending_index = index-1
                break
        if price_ending_index:
            break

    # get the number before the price signs
    price = None
    if price_ending_index:
        for index in range(price_ending_index,-1,-1):
            if cleaned_text[index:price_ending_index+1].replace('.','',1).replace(',','',1).isdigit():
                price = float( cleaned_text[index:price_ending_index+1].replace(',','.',1) )
            else:
                break
    
    return price

last_dib = 0
async def dib_item(item, keyword, message):
    global last_dib

    seller = message.sender.first_name + ' ' + message.sender.last_name

    await asyncio.sleep(uniform(min_wait_s, max_wait_s))
    if time.time() - last_dib >= mute_period_s:
        # notify the user
        await client.send_message(send_notification_to, f"""🛒✅ You dibbed on a(n) {keyword}! ✅🛒
The seller is {seller}. Take a look at what you bought in the {group_tag} group.""")

        # dib the item in the group
        await message.reply(f'dibs {keyword}')
        last_dib = int(time.time())

        # write to the seller (currently not)
        #await asyncio.sleep(uniform(min_wait_s*4, max_wait_s*4))
        #await client.send_message(seller, f"Hi! I'm interested in the {keyword} you want to sell.")
        deactivate(item)
        logging.info(f"Dibbed {keyword}.")
    else:
        notify_user(send_notification_to, keyword, message)

async def notify_user(user, keyword, message):
    seller = message.sender.first_name + ' ' + message.sender.last_name

    await client.send_message(user, f"""🛒❗There's a(n) {keyword} on sale. ❗🛒
Take a look at the {group_tag} group to see what {seller} sells.""")

    logging.info(f"Notified user about {keyword}.")

client.start()
logging.info("Dibsbot is active..")
client.run_until_disconnected()