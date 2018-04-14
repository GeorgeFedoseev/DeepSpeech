import os

from telegram.ext import Updater


updater = Updater("592335153:AAEDnx7bFAfW87znwH6tAYsAfS-JZwdJEy8")   
def log_telegram(msg):
    try:
        updater.bot.send_message(chat_id="79735423", text=msg)
    except:
        pass

def telegram_send_text_as_attachement(name, text):
    try:
        fname = name+".txt"
        f = open(fname, "w")
        f.write(text)    
        f.close()

        f = open(fname, "r")
        updater.bot.send_document(chat_id="79735423", document=f)
        f.close()

        os.remove(fname)
    except:
        pass
