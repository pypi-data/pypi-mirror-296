"""
Copyright 2016 Inmanta

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: code@inmanta.com
"""

import re
import typing

import inmanta_plugins.mitogen.abc

import inmanta.agent.handler
import inmanta.export
import inmanta.resources


@inmanta.resources.resource("yum::Package", agent="host.name", id_attribute="name")
class Package(inmanta_plugins.mitogen.abc.ResourceABC):
    """
    A software package installed on an operating system.
    """

    fields = ("name",)


@inmanta.agent.handler.provider("yum::Package", name="yum")
class YumPackage(inmanta_plugins.mitogen.abc.HandlerABC[Package]):
    """
    A Package handler that uses yum
    """

    def _parse_fields(self, lines: list[str]) -> dict:
        props = {}
        key = ""
        old_key = None
        for line in lines:
            if line.strip() == "":
                continue

            if line.strip() == "Available Packages":
                break

            result = re.search(r"""^(.+) :\s+(.+)""", line)
            if result is None:
                continue

            key, value = result.groups()
            key = key.strip()

            if key == "":
                props[old_key] += " " + value
            else:
                props[key] = value
                old_key = key

        return props

    def _run_yum(self, args: list[str]) -> tuple[str, str, int]:
        """
        Execute dnf command with provided args if dnf installed otherwise it uses yum.

        :param args: The arguments of the command
        :return: A tuple with (stdout, stderr, returncode)
        """
        if self.proxy.file_exists("/usr/bin/dnf"):
            return self.proxy.run("/usr/bin/dnf", ["-d", "0", "-e", "1", "-y"] + args)
        else:
            return self.proxy.run("/usr/bin/yum", ["-d", "0", "-e", "1", "-y"] + args)

    def raise_for_errors(
        self,
        output: tuple[str, str, int],
        ignore_errors: typing.Optional[list[str]] = [],
    ):
        """
        Process the output of yum command and raises an error if the return code is not 0.
        """
        stdout = output[0].strip()
        error_msg = output[1].strip()
        if output[2] != 0:
            for error in ignore_errors:
                if error in error_msg:
                    return
            raise Exception("Yum failed: stdout:" + stdout + " errout: " + error_msg)

    def read_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: Package
    ) -> None:
        yum_output = self._run_yum(["info", resource.name])
        self.raise_for_errors(
            yum_output, ignore_errors=["Error: No matching Packages to list"]
        )
        lines = yum_output[0].split("\n")

        output = self._parse_fields(lines[1:])
        # to decide if the package is installed or not, the "Repo" field can be used
        # from the yum info output (for e.g., CentOS 7)
        # the dnf info output (for e.g., CentOS 8) doesn't have this field, "Repository" can be used instead
        repo_keyword = (
            "Repo"
            if "Repo" in output
            else "Repository" if "Repository" in output else None
        )

        if output.get(repo_keyword, None) not in ["installed", "@System"]:
            raise inmanta.agent.handler.ResourcePurged()

    def create_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: Package
    ) -> None:
        self.raise_for_errors(self._run_yum(["install", resource.name]))
        ctx.set_created()

    def update_resource(
        self,
        ctx: inmanta.agent.handler.HandlerContext,
        changes: dict,
        resource: Package,
    ) -> None:
        raise NotImplementedError("PackageHandler doesn't support update_resource !")

    def delete_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: Package
    ) -> None:
        self.raise_for_errors(self._run_yum(["remove", resource.name]))
        ctx.set_purged()
