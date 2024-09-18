"""
Copyright 2024 Inmanta

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

import hashlib
import logging
import pathlib
import typing
from collections import defaultdict

import inmanta_plugins.mitogen.abc

import inmanta.agent
import inmanta.agent.handler
import inmanta.execute.proxy
import inmanta.export
import inmanta.resources
from inmanta.execute.util import Unknown
from inmanta.export import dependency_manager

if typing.TYPE_CHECKING:
    from inmanta.export import ModelDict, ResourceDict

LOGGER = logging.getLogger(__name__)


def hash_file(content: bytes) -> str:
    """
    Create a sha1 hash from the given content
    """
    sha1sum = hashlib.new("sha1")
    sha1sum.update(content)

    return sha1sum.hexdigest()


def generate_content(
    content_list: list[inmanta.execute.proxy.DynamicProxy],
    separator: str,
) -> str:
    """
    Generate a sorted list of content to prefix or suffix a file.

    :param content_list: The list of content object to sort and append together.
    :param separator: The string to use to join all the pieces together.
    """
    return separator.join(
        [
            c.value
            for c in sorted(
                content_list,
                key=lambda c: c.value if c.sorting_key is None else c.sorting_key,
            )
        ]
    )


def store_file(
    exporter: inmanta.export.Exporter, obj: inmanta.execute.proxy.DynamicProxy
) -> str:
    """
    Store the content of the fs::File entity on the server and return the hash of its
    content.

    :param exporter: The exporter that should be used to upload the file.
    :param obj: The file entity from the model, in which the content of the
        file is described.
    """
    content = obj.content
    if isinstance(content, Unknown):
        return content

    if "FileMarker" in content.__class__.__name__:
        with open(content.filename, "rb") as fd:
            content = fd.read()

    if len(obj.prefix_content) > 0:
        content = (
            generate_content(obj.prefix_content, obj.content_separator)
            + obj.content_separator
            + content
        )
    if len(obj.suffix_content) > 0:
        content += obj.content_seperator + generate_content(
            obj.suffix_content, obj.content_separator
        )

    return exporter.upload_file(content)


@inmanta.resources.resource("fs::File", agent="host.name", id_attribute="path")
class File(inmanta_plugins.mitogen.abc.ResourceABC):
    """
    A file on a filesystem
    """

    fields = (  # type:ignore[assignment]
        "path",
        "owner",
        "hash",
        "group",
        "permissions",
    )
    path: str
    owner: str
    hash: str
    group: str
    permissions: int

    @classmethod
    def get_hash(
        cls,
        exporter: inmanta.export.Exporter,
        entity: inmanta.execute.proxy.DynamicProxy,
    ) -> str:
        return store_file(exporter, entity)

    @classmethod
    def get_permissions(
        cls,
        _: inmanta.export.Exporter,
        entity: inmanta.execute.proxy.DynamicProxy,
    ) -> int:
        return int(entity.mode)


@inmanta.resources.resource("fs::Directory", agent="host.name", id_attribute="path")
class Directory(inmanta_plugins.mitogen.abc.ResourceABC):
    """
    A directory on a filesystem
    """

    fields = (  # type:ignore[assignment]
        "path",
        "owner",
        "group",
        "permissions",
    )
    path: str
    owner: str
    group: str
    permissions: str

    @classmethod
    def get_permissions(
        cls,
        _: inmanta.export.Exporter,
        entity: inmanta.execute.proxy.DynamicProxy,
    ) -> int:
        return int(entity.mode)


@inmanta.resources.resource("fs::Symlink", agent="host.name", id_attribute="dst")
class Symlink(inmanta_plugins.mitogen.abc.ResourceABC):
    """
    A symbolic link on the filesystem
    """

    fields = (  # type:ignore[assignment]
        "src",
        "dst",
    )
    src: str
    dst: str


@inmanta.agent.handler.provider("fs::File", name="posix_file")
class PosixFileProvider(inmanta_plugins.mitogen.abc.HandlerABC[File]):
    """
    This handler can deploy files on a unix system
    """

    def _get_file(self, ctx: inmanta.agent.handler.HandlerContext, hash: str) -> bytes:
        data = self.get_file(hash)
        if data is None:
            ctx.error(
                "File with hash %(hash)s is not available on the orchestrator",
                hash=hash,
            )
            raise RuntimeError("File missing from the orchestrator")
        return data

    def read_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: File
    ) -> None:
        if not self.proxy.file_exists(resource.path):
            raise inmanta.agent.handler.ResourcePurged()

        resource.hash = self.proxy.hash_file(resource.path)

        # upload the previous version for back up and for generating a diff!
        content = self.proxy.read_binary(resource.path)

        if not self.stat_file(resource.hash):
            self.upload_file(resource.hash, content)

        for key, value in self.proxy.file_stat(resource.path).items():
            setattr(resource, key, value)

    def create_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: File
    ) -> None:
        if self.proxy.file_exists(resource.path):
            raise Exception(
                f"Cannot create file {resource.path}, because it already exists."
            )

        data = self._get_file(ctx, resource.hash)
        if hash_file(data) != resource.hash:
            raise Exception(f"File hash was {resource.hash} expected {hash_file(data)}")

        self.proxy.put(resource.path, data)
        self.proxy.chmod(resource.path, str(resource.permissions))
        self.proxy.chown(resource.path, resource.owner, resource.group)
        ctx.set_created()

    def delete_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: File
    ) -> None:
        if self.proxy.file_exists(resource.path):
            self.proxy.remove(resource.path)
        ctx.set_purged()

    def update_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, changes: dict, resource: File
    ) -> None:
        if not self.proxy.file_exists(resource.path):
            raise Exception(
                f"Cannot update file {resource.path} because it doesn't exist"
            )

        if "hash" in changes:
            data = self._get_file(ctx, resource.hash)
            if hash_file(data) != resource.hash:
                raise Exception(
                    "File hash was {} expected {}".format(
                        resource.hash, hash_file(data)
                    )
                )
            self.proxy.put(resource.path, data)

        if "permissions" in changes:
            self.proxy.chmod(resource.path, str(resource.permissions))

        if "owner" in changes or "group" in changes:
            self.proxy.chown(resource.path, resource.owner, resource.group)
        ctx.set_updated()


@inmanta.agent.handler.provider("fs::Directory", name="posix_directory")
class DirectoryHandler(inmanta_plugins.mitogen.abc.HandlerABC[Directory]):
    """
    A handler for creating directories
    """

    def read_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: Directory
    ) -> None:
        if not self.proxy.file_exists(resource.path):
            raise inmanta.agent.handler.ResourcePurged()
        else:
            for key, value in self.proxy.file_stat(resource.path).items():
                setattr(resource, key, value)

    def create_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: Directory
    ) -> None:
        self.proxy.mkdir(resource.path)
        mode = str(resource.permissions)
        self.proxy.chmod(resource.path, mode)
        self.proxy.chown(resource.path, resource.owner, resource.group)
        ctx.set_created()

    def delete_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: Directory
    ) -> None:
        self.proxy.rmdir(resource.path)
        ctx.set_purged()

    def update_resource(
        self,
        ctx: inmanta.agent.handler.HandlerContext,
        changes: dict,
        resource: Directory,
    ) -> None:
        if "permissions" in changes:
            mode = str(resource.permissions)
            self.proxy.chmod(resource.path, mode)
        if "owner" in changes or "group" in changes:
            self.proxy.chown(resource.path, resource.owner, resource.group)
        ctx.set_updated()


@inmanta.agent.handler.provider("fs::Symlink", name="posix_symlink")
class SymlinkProvider(inmanta_plugins.mitogen.abc.HandlerABC[Symlink]):
    """
    This handler can deploy symlinks on unix systems
    """

    def read_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: Symlink
    ) -> None:
        if not self.proxy.file_exists(resource.dst):
            raise inmanta.agent.handler.ResourcePurged()
        elif not self.proxy.is_symlink(resource.dst):
            raise Exception(
                "The target of resource %s already exists but is not a symlink."
                % resource
            )
        else:
            resource.src = self.proxy.readlink(resource.dst)

    def create_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: Symlink
    ) -> None:
        self.proxy.symlink(resource.src, resource.dst)
        ctx.set_created()

    def delete_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: Symlink
    ) -> None:
        self.proxy.remove(resource.dst)
        ctx.set_purged()

    def update_resource(
        self,
        ctx: inmanta.agent.handler.HandlerContext,
        changes: dict,
        resource: Symlink,
    ) -> None:
        self.proxy.remove(resource.dst)
        self.proxy.symlink(resource.src, resource.dst)
        ctx.set_updated()


@dependency_manager
def dir_before_file(model: "ModelDict", resources: "ResourceDict"):
    """
    If a file/symlink/directory is defined on a host, then make it depend on its parent directory
    """
    # loop over all resources to find files and dirs
    per_host: dict[str, list[tuple[pathlib.Path, object]]] = defaultdict(list)
    per_host_dirs: dict[str, list[object]] = defaultdict(list)
    for resource in resources.values():
        if resource.id.get_entity_type() in [
            "fs::File",
            "fs::Directory",
        ]:
            per_host[resource.model.host].append(
                (pathlib.Path(resource.path), resource)
            )

        if resource.id.get_entity_type() == "fs::Symlink":
            per_host[resource.model.host].append((pathlib.Path(resource.src), resource))
            per_host[resource.model.host].append((pathlib.Path(resource.dst), resource))

        if resource.id.get_entity_type() == "fs::Directory":
            per_host_dirs[resource.model.host].append(resource)

    # now add deps per host
    for host, files in per_host.items():
        for path, hfile in files:
            for pdir in per_host_dirs[host]:
                if pathlib.Path(pdir.path) in path.parents:
                    if pdir.purged:
                        if hfile.purged:
                            # The folder is purged, and so is the file, the file should be
                            # cleaned up first, then the folder can be.
                            # This is not required as the folder would have cleaned the file,
                            # but it is also not wrong
                            pdir.requires.add(hfile)
                        else:
                            # Trying to create a file in a purged folder, this can not work
                            raise RuntimeError(
                                f"Directory {pdir.id} is purged but a resource is trying to "
                                f"deploy something in it: {hfile.id}"
                            )
                    else:
                        # Make the File resource require the directory
                        hfile.requires.add(pdir)
