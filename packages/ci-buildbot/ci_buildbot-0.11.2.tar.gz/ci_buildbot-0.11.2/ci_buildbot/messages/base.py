from __future__ import annotations

import datetime
import json
from typing import TYPE_CHECKING, Any, ClassVar

from pytz import timezone

from ci_buildbot import __version__

from ..exc import ImproperlyConfiguredError
from ..settings import jinja_env

if TYPE_CHECKING:
    from ci_buildbot.context_processors import AbstractContextProcessor

    from ..typedefs import MessageContext


class Message:
    """
    The base class for all slack messages.
    """

    #: The name of the Jinja template to use to render this message.
    template: str | None = None
    #: The list of context processors to use to annotate the message context.
    context_processors: ClassVar[list[type[AbstractContextProcessor]]] = []

    def get_template(self) -> str:
        """
        Return the filename of the Jinja template to use to render our slack message.

        Raises:
            ImproperlyConfigured: if the subclass does not define a template.

        Returns:
            The name of the Jinja template.

        """
        if not self.template:
            msg = "Message subclasses must define a template"
            raise ImproperlyConfiguredError(msg)
        return self.template

    def format(self, **kwargs) -> dict[str, Any]:
        """
        Generate the full JSON blob to send to slack.

        Adds the following keys to the context:

        * ``completed_date``: the date and time the build step finished
        * ``buildbot``: our the name and version

        Returns:
            The data structure to send to slack as our message.

        """
        context: MessageContext = {}
        for processor in self.context_processors:
            processor(**kwargs).annotate(context)
        now = datetime.datetime.now(timezone("UTC"))
        now_pacific = now.astimezone(timezone("US/Pacific"))
        context["completed_date"] = now_pacific.strftime("%Y-%m-%d %H:%M %Z")
        context["buildbot"] = f"ci-buildbot-{__version__}"
        template = jinja_env.get_template(self.get_template())
        rendered = template.render(**context)
        return json.loads(rendered)
