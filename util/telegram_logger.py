import os
import json

from telegram.ext import Updater

# "592335153:AAEDnx7bFAfW87znwH6tAYsAfS-JZwdJEy8"

class TelegramLogger:

    def __init__(self, accessToken, chat_id):
        self.updater = Updater(accessToken)
        self.chat_id = chat_id

    @classmethod
    def withJsonCredentials(cls, json_path):
        with open(json_path, 'r') as fp:            
            cred = json.load(fp)

            return cls(cred["accessToken"], cred["chatId"])




    def Log(self, msg):

        if len(msg) > 500:
            self.LogAsTxtAttachment(msg)
            return

        try:
            self.updater.bot.send_message(chat_id=self.chat_id, text=msg)
        except:
            pass

    def LogAsTxtAttachment(self, text, attachment_name="long_log"):
        try:
            fname = attachment_name+".txt"
            with open(fname, "w") as fp:             
                fp.write(text)            

            with open(fname, "r") as fp:            
                self.updater.bot.send_document(chat_id=self.chat_id, document=fp)
            os.remove(fname)
        except:
            pass
