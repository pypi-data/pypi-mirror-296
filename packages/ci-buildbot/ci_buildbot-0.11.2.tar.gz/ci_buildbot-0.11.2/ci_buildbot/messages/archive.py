from typing import ClassVar

from ..context_processors import (
    AbstractContextProcessor,
    CodebuildProcessor,
    GitChangelogProcessor,
    GitProcessor,
    NameVersionProcessor,
)
from .base import Message


class ArchiveCodeMessage(Message):
    """
    Used to send a slack message about archiving code tarballs to an artifactory.
    """

    template: str = "archive.tpl"
    context_processors: ClassVar[list[type[AbstractContextProcessor]]] = [
        NameVersionProcessor,
        GitProcessor,
        GitChangelogProcessor,
        CodebuildProcessor,
    ]
