<img src="https://raw.githubusercontent.com/albiDmtr/dibsomator/main/logo.ico"  width="84" height="84">
###  Dibsbot
##### A Telegram bot for automating dibbing on items in the Otaniemi Buy and Sell group

## Setup:
**1.**  Setup a virtual cloud instance if you wish the bot to run over the clock

**2.** Clone this repository to your local or virtual machine

**3.**  Get API keys from [my.telegram.org/apps](https://my.telegram.org/apps)
> It is recommended to use an account different from your main account to avoid losing access to it in case the bot malfunctions

**4.** In the folder containing the code of the bot, create a file named `.env` and give the following environment variables the values of your Telegram credentials
```
    TELETHON_ID = "<your app ID goes here>"
    TELETHON_HASH = "<your hash goes here>"
```
**5.** From the account you run dibsbot from, join the @aaltomarketplace group
> If you wish to recive notifications to a different account than what the bot is run on, <strong>make sure to send a message to the account the bot uses</strong>, otherwise Telegram will not let it send messages to you

**6.** Specify the bot what to look for in the `bot_config.json` file
> You can find an example bot_config.json file, but here is a description of what each key means:
- `"keywords"`: These are the words the bot is looking for in messages
- `"max_price"`: The maximum price in euros the bot will dib to
- `"dibs_to_unknown_price"`: If set to `true`, the bot will dib to items matching the keywords even if it can not figure out what the price is
- `"notify_only"`: If set to `false`, the bot will write dibs to the item in the group, if set to a Telegram tag, the bot will not write dibs and will only send a notification to the given user
- `"active"`: If `false`, the bot will not dib or notify users about the given item. Automatically set to `false` after dibbing
- `"notify_about_free"`: If set to `true`, the user will get notification of every free to take item
- `"send_notification_to"`:  The bot will send all notifications to this user
- `"group_tag"`: The tag of the group the bot checks for messages in. You likely need `"@aaltomarketplace"`.

**7.** If you run the bot from a Linux virtual machine, you can run the Bash scripts `start.sh` to start the bot and `stop.sh` to stop it. If you run it locally, just run the Python script `main.py`

## Possible future features:
- Filter by pickup location
- Use GPT3 to check if what is being sold is what we think it is
- Beer as currency
- Not all fields are mandatory in bot_config.json
- Telegram UI (bot can be configurated in telegram)
- Multi-user