"""
Settings for the ci_buildbot package.
"""

from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

templates_path = Path(__file__).parent / "templates"
jinja_env = Environment(  # nosemgrep: python.flask.security.audit.jinja2-template-injection.jinja2-template-injection
    loader=FileSystemLoader(str(templates_path)),
)


class Settings(BaseSettings):
    """
    See https://docs.pydantic.dev/latest/usage/pydantic_settings/ for details on
    using and overriding this.

    """

    #: Run this in debug mode if True
    debug: bool = False
    #: The slack API token to use
    api_token: Optional[str] = Field(None, validation_alias="slack_api_token")  # noqa: FA100
    #: The name of the channel to post to
    channel: str = "jenkins"

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env.buildbot",
        env_file_encoding="utf-8",
    )
