import logging

from cationbot.core.bot import bot
from cationbot.core.env import env

logging.basicConfig(level=logging.INFO)

bot.run(env.TOKEN)
