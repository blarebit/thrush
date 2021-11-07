"""File Manager views."""
import os
import shutil

from pathlib import Path

from django.conf import settings
from django.http import JsonResponse

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from file_manager.forms import UploadFileForm


class FileManager(APIView):
    """File manager class."""

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def __is_user_root(self, path):
        return path.endswith(
            "/aap/media/{0}".format(self.request.user.id)
        ) and path.endswith("/aap/media/{0}/".format(self.request.user.id))

    def __get_correct_path(self, path):
        """Retrieve correct path."""
        user_root_directory = os.path.join(
            settings.MEDIA_ROOT, str(self.request.user.id)
        )
        if not path or not path.startswith(user_root_directory):
            return os.path.join(user_root_directory, path)
        else:
            return path

    def __create_path(self, request, path="", new_folder=""):
        """Check if user root path dose not exist, create it."""
        correct_path = self.__get_correct_path(path)
        if not path and not new_folder:
            if not os.path.exists(correct_path):
                os.makedirs(correct_path)
                return [{"path": correct_path}, 201]
            elif request.META["CONTENT_TYPE"].startswith("multipart/form-data"):
                return [{"path": correct_path}, 201]
            else:
                return [
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "detail": "User root directory already existed!",
                    },
                    status.HTTP_400_BAD_REQUEST,
                ]
        elif new_folder:
            if not path:
                path = os.path.join(correct_path, new_folder)
            else:
                path = os.path.join(self.__get_correct_path(path), new_folder)
            if not os.path.exists(os.path.dirname(correct_path)):
                return [
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "detail": "Path is not existed!",
                    },
                    status.HTTP_400_BAD_REQUEST,
                ]
            else:
                try:
                    os.mkdir(path)
                except FileExistsError:
                    return [
                        {
                            "status_code": status.HTTP_400_BAD_REQUEST,
                            "code": status.HTTP_400_BAD_REQUEST,
                            "detail": "Directory already existed!",
                        },
                        status.HTTP_400_BAD_REQUEST,
                    ]
                return [{"path": path}, 201]
        elif path and not new_folder:
            return [
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "detail": "New directory name is not defined!",
                },
                status.HTTP_400_BAD_REQUEST,
            ]
        else:
            return [
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "detail": "Unknown Request!",
                },
                status.HTTP_400_BAD_REQUEST,
            ]

    def post(self, request, url_path="", format=None):
        """Upload file or create directory."""
        if request.META["CONTENT_TYPE"] == "application/json":
            request_keys = request.data.keys()
            if "new_folder" in request_keys:
                """Create new directory in url_path."""
                result = self.__create_path(
                    request, url_path, request.data["new_folder"]
                )
                if result[1] == 400:
                    return JsonResponse(result[0], status=result[1])
                else:
                    return JsonResponse(result[0], status=result[1])
            elif "rename_to" in request_keys:
                """Rename file or directory in url_path."""
                src = self.__get_correct_path(url_path)
                dst = self.__get_correct_path(url_path)
                if os.path.isdir(src):
                    return Response(
                        {
                            "path": shutil.move(
                                src,
                                os.path.join(
                                    os.path.dirname(dst), request.data["rename_to"]
                                ),
                            )
                        },
                        201,
                    )
                elif os.path.isfile(src):
                    try:
                        return Response(
                            os.rename(
                                src,
                                os.path.join(
                                    os.path.dirname(dst), request.data["rename_to"]
                                ),
                            )
                        )
                    except OSError:
                        return Response(
                            data={
                                "status_code": status.HTTP_400_BAD_REQUEST,
                                "code": status.HTTP_400_BAD_REQUEST,
                                "detail": "Destination is existed and not empty!",
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    except IsADirectoryError:
                        return Response(
                            data={
                                "status_code": status.HTTP_400_BAD_REQUEST,
                                "code": status.HTTP_400_BAD_REQUEST,
                                "detail": "Destination is a directory!",
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    except NotADirectoryError:
                        return Response(
                            data={
                                "status_code": status.HTTP_400_BAD_REQUEST,
                                "code": status.HTTP_400_BAD_REQUEST,
                                "detail": "Destination is a File!",
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response(
                        data={
                            "status_code": status.HTTP_400_BAD_REQUEST,
                            "code": status.HTTP_400_BAD_REQUEST,
                            "detail": "Unknown source path!",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            elif "copy_to" in request_keys:
                src = self.__get_correct_path(url_path)
                dst = self.__get_correct_path(request.data["copy_to"])
                if os.path.isdir(src) and os.path.isdir(dst):
                    return Response(
                        {"destination": shutil.copytree(src, dst, dirs_exist_ok=True)},
                        201,
                    )
                elif os.path.isfile(src):
                    return Response({"destination": shutil.copy2(src, dst)}, 201)
                else:
                    return Response(
                        data={
                            "status_code": status.HTTP_400_BAD_REQUEST,
                            "code": status.HTTP_400_BAD_REQUEST,
                            "detail": "Unknown move request!",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            elif request.data["move_to"]:
                src = self.__get_correct_path(url_path)
                dst = self.__get_correct_path(request.data["move_to"])
                if (os.path.isdir(src) or os.path.isfile(src)) and os.path.isdir(dst):
                    return Response({"path": shutil.move(src, dst)}, 201)
                else:
                    return Response(
                        data={
                            "status_code": status.HTTP_400_BAD_REQUEST,
                            "code": status.HTTP_400_BAD_REQUEST,
                            "detail": "Unknown move request!",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    data={
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "detail": "Unknown request!",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif request.META["CONTENT_TYPE"].startswith("multipart/form-data"):
            """Upload file to url_path."""
            try:
                f = request.FILES["file"]
            except FileNotFoundError:
                return Response(
                    data={
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "detail": "No file attached for upload!",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            correct_path = [{"path": self.__get_correct_path(url_path)}, 201]
            if not os.path.exists(correct_path[0]["path"]):
                return Response(
                    data={
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "detail": "Directory does not exist!",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if correct_path[1] == 201:
                file_destination = os.path.join(correct_path[0]["path"], f.name)
                form = UploadFileForm(request.POST, request.FILES)
                if form.is_valid():
                    with open(file_destination, "wb+") as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                    return JsonResponse({"file_destination": file_destination}, status=201)
                else:
                    return Response(
                        data={
                            "status_code": status.HTTP_403_FORBIDDEN,
                            "code": status.HTTP_403_FORBIDDEN,
                            "detail": "Forbidden file type.",
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )
            else:
                return JsonResponse(correct_path[0], status=correct_path[1])
        else:
            return Response(
                data={
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "detail": "Unknown endpoint.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, url_path, format=None):
        """Delete file or directory."""
        path = self.__get_correct_path(url_path)
        if os.path.isdir(path):
            """Delete directory."""
            if not self.__is_user_root(path):
                try:
                    return Response(os.rmdir(path))
                except FileNotFoundError:
                    return Response(
                        data={
                            "status_code": status.HTTP_400_BAD_REQUEST,
                            "code": status.HTTP_400_BAD_REQUEST,
                            "detail": "Directory dose not exist!",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except OSError:
                    return Response(
                        data={
                            "status_code": status.HTTP_400_BAD_REQUEST,
                            "code": status.HTTP_400_BAD_REQUEST,
                            "detail": "Directory is not empty!",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    data={
                        "status_code": status.HTTP_403_FORBIDDEN,
                        "code": status.HTTP_403_FORBIDDEN,
                        "detail": "This task is forbidden!",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        elif os.path.isfile(path):
            """Delete file."""
            try:
                return Response(os.remove(path))
            except FileNotFoundError:
                return Response(
                    data={
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "detail": "File dose not exist!",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                data={
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "detail": "Path is not correct or Directory does not exist!",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def __get_directory_list(self, path, dir_tree):
        for a in Path(path).iterdir():
            if a.is_dir():
                dir_tree.append({"path": a.as_posix(),
                                 "name": a.name,
                                 "size": 0,
                                 "type": "directory",
                                 })
                self.__get_directory_list(a.as_posix(), dir_tree)

            else:
                dir_tree.append({"path": a.as_posix(),
                                 "name": a.name,
                                 "size": os.stat(a.as_posix()).st_size,
                                 "type": "file",
                                 })
        return dir_tree

    def get(self, request, url_path="", format=None):
        """Retrieve a List of all files and directories from url_path."""
        dir_tree = []
        path = self.__get_correct_path(url_path)
        result = self.__get_directory_list(path, dir_tree)
        return Response({"result": result})
