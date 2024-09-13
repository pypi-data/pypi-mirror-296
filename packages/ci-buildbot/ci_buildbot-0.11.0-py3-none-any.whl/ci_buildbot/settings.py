"""
Settings for the ci_buildbot package.
"""

from __future__ import annotations
from pathlib import Path

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
    api_token: str | None = Field(None, validation_alias="slack_api_token")
    #: The name of the channel to post to
    channel: str = "jenkins"

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
    )
