from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """The environment variables."""

    COMMAND_PREFIX: Optional[str]
    TOKEN: Optional[str]

    RULES_MESSAGE_ID: Optional[int]
    CHOOSE_TECH_MESSAGE_ID: Optional[int]
    MEMBER_ROLE_NAME: Optional[str]

    DEFAULT_DIRECT_MESSAGE_RESPONSE: Optional[str]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
