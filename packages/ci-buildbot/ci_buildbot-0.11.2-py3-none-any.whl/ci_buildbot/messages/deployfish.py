from typing import ClassVar

from ..context_processors import (
    AbstractContextProcessor,
    CodebuildProcessor,
    DeployfishDeployProcessor,
    GitProcessor,
    NameVersionProcessor,
)
from .base import Message


class DeployfishDeployStartMessage(Message):
    """
    Send a slack message about starting a deployfish service deploy.
    """

    template: str = "deploy_start.tpl"
    context_processors: ClassVar[list[type[AbstractContextProcessor]]] = [
        NameVersionProcessor,
        DeployfishDeployProcessor,
        GitProcessor,
        CodebuildProcessor,
    ]


class DeployfishDeploySuccessMessage(Message):
    """
    Send a slack message about a successful deployfish service deploy.
    """

    template: str = "deploy_success.tpl"
    context_processors: ClassVar[list[type[AbstractContextProcessor]]] = [
        NameVersionProcessor,
        DeployfishDeployProcessor,
        GitProcessor,
        CodebuildProcessor,
    ]


class DeployfishDeployFailureMessage(Message):
    """
    Send a slack message about a unsuccessful deployfish service deploy.
    """

    template: str = "deploy_failed.tpl"
    context_processors: ClassVar[list[type[AbstractContextProcessor]]] = [
        NameVersionProcessor,
        DeployfishDeployProcessor,
        GitProcessor,
        CodebuildProcessor,
    ]
