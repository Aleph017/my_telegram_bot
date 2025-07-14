from dotenv import load_dotenv
from telebot import types
import telebot
import os
import json
import logging

def load():
    logging.info("Loading story.json")
    with open("story.json", "r") as file:
        return json.load(file)

def init_bot():
    logging.info("Initiating the bot")
    if not os.path.exists("progress"):
        logging.info(f"Creating {os.getcwd()}/progress directory")
        os.mkdir("progress")
    else: logging.info(f"Directory {os.getcwd()}/progress detected")
    if not os.path.exists("images"):
        logging.info(f"Creating {os.getcwd()}/images directory")
        os.mkdir("images")
    else: logging.info(f"Directory {os.getcwd()}/images detected")
    load_dotenv()
    TOKEN=os.getenv("OLEG_ENV")
    if TOKEN is None:
        logging.critical("Token not found in environment. Edit '.env' file")
        exit(1)
    return telebot.TeleBot(token=str(TOKEN), parse_mode=None)

def update_progress(ID, progress):
    logging.info(f"Saving progress for chat {ID}")
    with open(f"progress/{ID}", "w") as savefile:
        savefile.write(progress)

def load_progress(ID):
    logging.info(f"Loading progress for chat {ID}")
    try:
        with open(f"progress/{ID}", "r") as savefile:
            return savefile.read()
    except FileNotFoundError:
        logging.error(f"No savefile found for chat {ID}, returning \"start\"")
        return "start"
    
def snd_msg(progress, story, bot, ID):
    logging.info(f"Sending a message in chat {ID}")

    keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True)


    if "image" in story[progress]:
        try:
            with open(story[progress]["image"], "rb") as img:
                bot.send_photo(ID, img)
                logging.info(f"Sent image {story[progress]['image']} to chat {ID}")
        except Exception as e:
            logging.error(f"Failed to send image {story[progress]['image']} to chat {ID}")

    try:
        for choice in story[progress]["choices"]:
            keyboard.add(types.KeyboardButton(text=choice["text"]))
        bot.send_message(ID, story[progress]["text"], reply_markup=keyboard)
    except Exception as e:
        bot.send_message(ID, f"ERROR: {e}")
        logging.error(f"Encountered exception in snd_msg function: {e}")


def main():
    logging.basicConfig(level=logging.INFO, 
                        format="%(asctime)s - %(levelname)s - %(message)s")
    bot = init_bot()
    story = load()

    @bot.message_handler(commands=["debug"])
    def debug(message):
        ID = message.chat.id
        user = message.from_user
        bot.reply_to(message, 
                     f"DEBUG INFO\n"
                     f"CHAT ID : {ID}\n"
                     f"USER ID : {user.id}\n"
                     f"PROGRESS : {load_progress(ID)}"
                    )
        logging.info(f"Debug command issued for chat {ID}")

    @bot.message_handler(commands=["start"])
    def start(message):
        current_progress = "start"
        logging.info(f"Starting the game for chat {message.chat.id}")
        snd_msg(current_progress, story, bot, message.chat.id)
        update_progress(message.chat.id, current_progress)
        
    @bot.message_handler(func=lambda message: True)
    def send_message(message):
        ID = message.chat.id
        logging.info(f"""Received message \"{message.text}\" from chat {message.chat.id}""")
        current_progress = load_progress(message.chat.id)
        
        if current_progress not in story:
            bot.send_message(ID, f"Story key not found: {current_progress}")
            bot.send_message(ID, f"Falling back to 'start'")
            update_progress(ID, "start")
            current_progress = "start"
            logging.warning(f"KeyError in {ID} chat; falling back to 'start'")

        for choice in story[current_progress]["choices"]:
            if message.text == choice["text"]:
                current_progress = choice["next"]
                snd_msg(current_progress, story, bot, ID)
                update_progress(ID, current_progress)
                break
        else:
            bot.send_message(ID, "sry m8 not seeing this option")
            logging.error(f"Invalid option \"{message.text}\" in chat {message.chat.id}")
            

    bot.polling()

if __name__ == "__main__":
    main()
