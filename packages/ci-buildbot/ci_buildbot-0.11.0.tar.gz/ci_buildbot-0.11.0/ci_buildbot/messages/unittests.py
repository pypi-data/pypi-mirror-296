from typing import ClassVar

from ..context_processors import (
    AbstractContextProcessor,
    CodebuildProcessor,
    GitProcessor,
    NameVersionProcessor,
    UnittestReportGroupProcessor,
)
from .base import Message


class UnittestsStartMessage(Message):
    template = "unittests_start.tpl"
    context_processors: ClassVar[list[type[AbstractContextProcessor]]] = [
        NameVersionProcessor,
        CodebuildProcessor,
        GitProcessor,
    ]


class UnittestsSuccessMessage(Message):
    template = "unittests_success.tpl"
    context_processors: ClassVar[list[type[AbstractContextProcessor]]] = [
        NameVersionProcessor,
        CodebuildProcessor,
        UnittestReportGroupProcessor,
        GitProcessor,
    ]


class UnittestsFailureMessage(Message):
    template = "unittests_failed.tpl"
    context_processors: ClassVar[list[type[AbstractContextProcessor]]] = [
        NameVersionProcessor,
        CodebuildProcessor,
        UnittestReportGroupProcessor,
        GitProcessor,
    ]
