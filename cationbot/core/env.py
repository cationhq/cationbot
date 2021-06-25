from typing import Dict, Optional

from pydantic import BaseSettings


class Environment(BaseSettings):
    """The environment variables from app."""

    # The prefix for bot commands.
    PREFIX: Optional[str]

    # The token provided by Discord dashboard.
    TOKEN: Optional[str]

    # Messages stuff
    ROLES_MESSAGE_ID: Optional[int]
    RULES_MESSAGE_ID: Optional[int]

    # Suggestions
    SUGGESTIONS_CHANNEL_ID: Optional[int]
    SUGGESTIONS_USELESS_EMOJI: Optional[str]
    SUGGESTIONS_USEFULL_EMOJI: Optional[str]

    # Roles stuff
    MEMBERS_ROLE_ID: Optional[int]
    EMOJI_ROLES: Optional[Dict[str, int]] = {}

    # The default message to responds to direct messages.
    DEFAULT_DM_RESPONSE: Optional[str]

    # Misc.
    CHANGE_PRESENCE_IN_MINUTES: Optional[int]

    class Config:
        case_sensitive = True
        env_file = ".env"


env = Environment()
