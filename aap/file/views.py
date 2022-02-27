"""File views."""
import logging
import os
import pathlib
import shutil
from urllib.parse import urljoin
from typing import List, Dict, Union, Optional

from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from humanfriendly import format_size
from rest_framework import status, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import NodeAlreadyExists, NodeNotFound, InvalidPath
from .forms import UploadForm
from .serializers import (
    FileActionSerializer,
    NewFolderActionSerializer,
    RenameActionSerializer,
    CopyActionSerializer,
    MoveActionSerializer,
)


def fix_path(node_path: str, full_path: bool = False) -> str:
    """Remove based path from a user media path."""
    media_root = settings.MEDIA_ROOT.as_posix()
    # +1 is for removing the first slash.
    node_path = node_path[node_path.find(media_root) + len(media_root) + 1:]
    if full_path:
        return urljoin(settings.MEDIA_URL, node_path)
    return node_path


def setup_path(fn):
    """
    Setup path and update the URL path to a real path.

    Note:
        It will create an empty directory if user doesn't have any.
    """

    def wrap(self, request, path: str = ""):
        if ".." in path:
            raise NotFound
        real_path = settings.MEDIA_ROOT / str(request.user.id)
        if not real_path.exists():
            real_path.mkdir()
        if path:
            real_path /= path
        return fn(self, request, real_path)

    return wrap


def validate_path(fn):
    """Validate path to ensure it exists."""

    def wrap(self, request, path: pathlib.Path):
        # Validate the path.
        if not path.exists():
            return Response(
                data={
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "code": status.HTTP_404_NOT_FOUND,
                    "detail": "path not found",
                },
                status=status.HTTP_404_NOT_FOUND,
                exception=True,
            )
        return fn(self, request, path)

    return wrap


def validate_input(fn):
    """Input validation decorator."""

    def wrap(self, request, path: pathlib.Path):
        # Validate form data.
        if "multipart/form-data" in request.headers["Content-Type"]:
            form = UploadForm(request.POST, request.FILES)
            if not form.is_valid():
                return Response(
                    data={
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "detail": form.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    exception=True,
                )
            if not path.is_dir():
                raise InvalidPath
            if (path / form.files["file"].name).exists():
                raise NodeAlreadyExists

            return fn(self, request, path, form=form)

        # Validate JSON.
        else:
            file_action = FileActionSerializer(data=request.data)
            file_action.is_valid(raise_exception=True)

            # New folder.
            if file_action.data["action"] == "new_folder":
                new_folder_serializer = NewFolderActionSerializer(
                    data=file_action.data["params"]
                )
                new_folder_serializer.is_valid(raise_exception=True)
                if (path / new_folder_serializer.data["name"]).exists():
                    raise NodeAlreadyExists

            # Rename.
            if file_action.data["action"] == "rename":
                rename_serializer = RenameActionSerializer(
                    data=file_action.data["params"]
                )
                rename_serializer.is_valid(raise_exception=True)
                old_path = path / rename_serializer.data["old_name"]
                new_path = path / rename_serializer.data["new_name"]
                if not old_path.exists():
                    raise NodeNotFound
                if new_path.exists():
                    raise NodeAlreadyExists

            # Move and Copy.
            if file_action.data["action"] in ("move", "copy"):
                if file_action.data["action"] == "move":
                    action_serializer = MoveActionSerializer(
                        data=file_action.data["params"]
                    )
                else:
                    action_serializer = CopyActionSerializer(
                        data=file_action.data["params"]
                    )
                action_serializer.is_valid(raise_exception=True)
                source = path / action_serializer.data["source"]
                destination = (
                    path / action_serializer.data["destination"] / action_serializer.data["source"]
                )
                if not source.resolve().is_relative_to(
                    path
                ) or not destination.resolve().is_relative_to(path):
                    raise InvalidPath
                if not source.exists():
                    raise NodeNotFound
                if destination.exists():
                    raise NodeAlreadyExists

            return fn(self, request, path, serializer=file_action)

    return wrap


class FileAPIView(APIView):
    """File API view."""

    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def _represent_node_info(path: pathlib.Path):
        if path.is_dir():
            return {
                "link": fix_path(path.as_posix()),
                "url": fix_path(path.as_posix(), True),
                "name": path.name,
                "size": {
                    "bytes": 0,
                    "readable": "",
                },
                "type": "directory",
            }
        size = os.stat(path.as_posix()).st_size
        return {
            "link": fix_path(path.as_posix()),
            "url": fix_path(path.as_posix(), True),
            "name": path.name,
            "size": {
                "bytes": size,
                "readable": format_size(size, binary=True),
            },
            "type": "file",
        }

    def _get_node_info(
        self, path: pathlib.Path
    ) -> Union[Dict[str, Union[str, int]], List[Dict[str, Union[str, int]]]]:
        """Return node info which can be list of files and directories or a specific file info.

        Args:
            path (pathlib.Path): file or directory path.

        Returns:
            Union[Dict[str, Union[str, int]], List[Dict[str, Union[str, int]]]]: list of files and directories
                with details or a file info.
        """
        if path.is_file():
            return self._represent_node_info(path)

        tree = []
        for node in path.iterdir():
            tree.append(self._represent_node_info(node))
        return tree

    @swagger_auto_schema(request_body=FileActionSerializer)
    @setup_path
    @validate_path
    @validate_input
    def post(
        self,
        request,
        path: pathlib.Path,
        serializer: Optional[FileActionSerializer] = None,
        form: Optional[UploadForm] = None,
    ):
        """Upload a file or perform an action on a file or directory."""
        # Upload.
        if form:
            file_path = path / form.files["file"].name
            try:
                with open(file_path.as_posix(), "wb+") as file:
                    for chunk in form.files["file"].chunks():
                        file.write(chunk)
                return Response(
                    data=self._represent_node_info(file_path),
                    status=status.HTTP_201_CREATED,
                )
            except IOError as e:
                logging.error(str(e))
                return Response(
                    data={
                        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "detail": "Unexpected error.",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        # Actions
        # New folder.
        if serializer.data["action"] == "new_folder":
            new_path = path / serializer.data["params"]["name"]
            new_path.mkdir()
            return Response(
                data=self._represent_node_info(new_path), status=status.HTTP_201_CREATED
            )

        # Rename.
        if serializer.data["action"] == "rename":
            old_path = path / serializer.data["params"]["old_name"]
            new_path = path / serializer.data["params"]["new_name"]
            old_path.rename(new_path)
            return Response(
                data=self._represent_node_info(new_path), status=status.HTTP_200_OK
            )

        # Copy.
        if serializer.data["action"] == "copy":
            source = path / serializer.data["params"]["source"]
            destination = (
                path / serializer.data["params"]["destination"] / serializer.data["params"]["source"]
            )
            if source.is_file():
                shutil.copy(source, destination)
            else:
                shutil.copytree(source, destination)
            return Response(
                data=self._represent_node_info(destination), status=status.HTTP_200_OK
            )

        # Move.
        if serializer.data["action"] == "move":
            source = path / serializer.data["params"]["source"]
            destination = (
                path
                / serializer.data["params"]["destination"]
                / serializer.data["params"]["source"]
            )
            shutil.move(source, destination)
            return Response(
                data=self._represent_node_info(destination), status=status.HTTP_200_OK
            )

    @setup_path
    @validate_path
    def delete(self, request, path: pathlib.Path):
        """Delete a file or directory."""
        # Prevent to remove the user directory.
        if fix_path(path.as_posix()).count("/") == 1:
            raise InvalidPath

        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @setup_path
    @validate_path
    def get(self, request, path: pathlib.Path):
        """Retrieve list of all files and directories in the path or a file info."""
        return Response({"result": self._get_node_info(path)})
