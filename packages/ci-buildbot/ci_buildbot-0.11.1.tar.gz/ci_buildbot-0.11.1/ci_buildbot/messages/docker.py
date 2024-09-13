from typing import ClassVar

from ..context_processors import (
    AbstractContextProcessor,
    CodebuildProcessor,
    DockerImageNameProcessor,
    DockerProcessor,
    GitProcessor,
    NameVersionProcessor,
)
from .base import Message


class DockerStartMessage(Message):
    """
    Send a slack message about starting a Docker image build.
    """

    template = "docker_start.tpl"
    context_processors: ClassVar[list[type[AbstractContextProcessor]]] = [
        NameVersionProcessor,
        DockerImageNameProcessor,
        CodebuildProcessor,
        GitProcessor,
    ]


class DockerSuccessMessage(Message):
    """
    Send a slack message about a successful Docker image build.
    """

    template = "docker_success.tpl"
    context_processors: ClassVar[list[type[AbstractContextProcessor]]] = [
        NameVersionProcessor,
        DockerImageNameProcessor,
        DockerProcessor,
        CodebuildProcessor,
        GitProcessor,
    ]


class DockerFailureMessage(Message):
    """
    Send a slack message about an unsuccessful Docker image build.
    """

    template = "docker_failed.tpl"
    context_processors: ClassVar[list[type[AbstractContextProcessor]]] = [
        NameVersionProcessor,
        DockerImageNameProcessor,
        CodebuildProcessor,
        GitProcessor,
    ]
