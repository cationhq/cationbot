import logging

from cationbot.core.bot import bot
from cationbot.core.settings import settings

logging.basicConfig(level=logging.INFO)

bot.run(settings.TOKEN)
