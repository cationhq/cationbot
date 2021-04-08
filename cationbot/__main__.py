import logging
from os import listdir, path
from pathlib import Path

from cationbot.core.bot import bot
from cationbot.core.env import env

logging.basicConfig(level=logging.INFO)

for filename in listdir(path.join(Path(__file__).parent, "cogs")):
    if filename.endswith(".py"):
        bot.load_extension(f"cationbot.cogs.{filename[:-3]}")


bot.run(env.TOKEN)
