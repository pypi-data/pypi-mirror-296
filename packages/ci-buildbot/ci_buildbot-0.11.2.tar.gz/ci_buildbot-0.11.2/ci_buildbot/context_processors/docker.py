from pathlib import Path

import docker

from ..typedefs import MessageContext
from .base import AbstractContextProcessor


class DockerImageNameProcessor(AbstractContextProcessor):
    """
    Adds the key ``short_image`` to the context, which is the basename of
    the Docker image without the repository name.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.image: str = kwargs["image"]

    def annotate(self, context: MessageContext) -> None:
        context["short_image"] = Path(self.image).name


class DockerProcessor(AbstractContextProcessor):
    """
    Adds the following keys to the context:

    * ``image_id``: the short id of the Docker image
    * ``image_size``: the size of the Docker image in MB
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.image: str = kwargs["image"]

    def annotate(self, context: MessageContext) -> None:
        client = docker.from_env()
        image = client.images.get(self.image)
        context["image_id"] = image.short_id.split(":")[1]
        context["image_size"] = image.attrs["Size"] / (1024 * 1024)
