# Bewerbung mit Buttons machen
# Deutsche Bewerbung/Englische Bewerbung
# Fragen: Siehe team-appli channel
# Nacheinander im Privatchat fragen
# In spezifischen Channel schicken
# Knopf: Annehmen/Ablehnen

import interactions as i
import configparser as cp


config = cp.ConfigParser()
config.read("config.ini")
bot = i.Client()
bot.load_extension("interactions.ext.jurigged")


@i.listen()
async def on_startup():
    print("Bot started.")

bot.load_extension("extensions.command")

bot.start(config["General"]["token"])
