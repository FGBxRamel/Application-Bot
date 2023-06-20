import configparser as cp
import sqlite3 as sql

import interactions as i


def setup_db():
    con = sql.connect("questions.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY,
        channel_id INTEGER,
        current_question INTEGER,
        language TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS answers (
        user_id INTEGER PRIMARY KEY,
        answer_1 TEXT,
        answer_2 TEXT,
        answer_3 TEXT,
        answer_4 TEXT,
        answer_5 TEXT,
        answer_6 TEXT,
        answer_7 TEXT,
        answer_8 TEXT,
        answer_9 TEXT,
        answer_10 TEXT,
        answer_11 TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS applications (
        message_id INTEGER PRIMARY KEY,
        language TEXT,
        user_id INTEGER
    )""")


setup_db()

config = cp.ConfigParser()
config.read("config.ini")
bot = i.Client(token=config["General"]["token"])
bot.load_extension("interactions.ext.jurigged")


@i.listen()
async def on_startup():
    print("Bot started.")

bot.load_extension("extensions.application")

bot.start()
