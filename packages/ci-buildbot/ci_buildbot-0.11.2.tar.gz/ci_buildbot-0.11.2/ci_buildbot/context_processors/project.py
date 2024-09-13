import pathlib
import subprocess

import toml

from ..exc import ImproperlyConfiguredError
from ..typedefs import MessageContext
from .base import AbstractContextProcessor


class NameVersionProcessor(AbstractContextProcessor):
    """
    A context processor that adds the following keys to the context:

    * ``name``: the project name
    * ``version``: the current version of the project

    If this is a python project, we'll get the name and version from setup.py.

    If not, we'll try to get it from Makefile by doing ``make image_name``
    for the name and ``make version`` for the version.
    """

    def setup_py(self, path: pathlib.Path) -> dict[str, str]:
        """
        Process a setup.py file and return the name and version.

        Raises:
            ValueError: if the setup.py is a stub, and doesn't
                contain a version and name

        Args:
            path: the path to the setup.py file

        Returns:
            A dictionary with the keys ``name`` and ``version``

        """
        context: dict[str, str] = {}
        context["version"] = subprocess.run(
            ["/usr/bin/env", "python", str(path), "--version"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if context["version"] == "0.0.0":
            msg = "setup.py is a stub"
            raise ValueError(msg)
        context["name"] = subprocess.run(
            ["/usr/bin/env", "python", str(path), "--name"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        return context

    def makefile(self, path: pathlib.Path) -> dict[str, str]:
        """
        Process a Makefile and return the name and version.

        Raises:
            ValueError: if the Makefile doesn't contain the
                ``image_name`` or ``version`` targets

        Args:
            path: the path to the Makefile

        Returns:
            A dictionary with the keys ``name`` and ``version``

        """
        context: dict[str, str] = {}
        # This command line extracts the names of the targets from the Makefile,
        # ignoring the implicit ones, and sorts them.
        command = [
            "make",
            "-pRrq",
            "-f",
            str(path)
        ]
        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            raise
        if 'image_name:' not in result.stdout:
            msg = "Makefile does not contain an image_name target"
            raise ValueError(msg)
        if 'version:' not in result.stdout:
            msg = "Makefile does not contain a version target"
            raise ValueError(msg)
        context["name"] = (
            subprocess.check_output(["make", "image_name"]).decode("utf8").strip()
        )
        context["version"] = (
            subprocess.check_output(["make", "version"]).decode("utf8").strip()
        )
        return context

    def pyproject_toml(self, path: pathlib.Path) -> dict[str, str]:
        """
        Process a pyproject.toml file and return the name and version.

        Raises:
            ValueError: if the pyproject.toml is a stub, and doesn't
                contain a version and name

        Args:
            path: the path to the pyproject.toml file

        Returns:
            A dictionary with the keys ``name`` and ``version``

        """
        context: dict[str, str] = {}
        data = toml.load(path)
        if "project" not in data:
            msg = "pyproject.toml is a stub: no project section"
            raise ValueError(msg)
        context["name"] = data["project"]["name"]
        context["version"] = data["project"]["version"]
        return context

    def annotate(self, context: MessageContext) -> None:
        """
        Add the following keys to ``context``:

        * ``name``: the project name
        * ``version``: the current version of the project

        If this is a python project, we'll get the name and version from
        setup.py.

        If not, we'll try to get it from Makefile by doing ``make image_name``
        for the name and ``make version`` for the version.

        Args:
            context: the current message context

        """
        super().annotate(context)
        setup_py = pathlib.Path.cwd() / "setup.py"
        makefile = pathlib.Path.cwd() / "Makefile"
        pyproject_toml = pathlib.Path.cwd() / "pyproject.toml"
        if setup_py.exists():
            try:
                context.update(self.setup_py(setup_py))
            except ValueError:
                pass
            else:
                return
        if pyproject_toml.exists():
            try:
                context.update(self.pyproject_toml(pyproject_toml))
            except ValueError:
                pass
            else:
                return
        if makefile.exists():
            try:
                context.update(self.makefile(makefile))
            except ValueError:
                pass
            else:
                return
        msg = "Cannot determine project name and version"
        raise ImproperlyConfiguredError(msg)
