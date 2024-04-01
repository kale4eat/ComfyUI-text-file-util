import os
from typing import Optional

import folder_paths

from . import folder_util

NODE_CATEGORY = "text-file-util"

_RETURN_CODES = [
    "LF",
    "CRLF",
    "LFCR",
]

_RETURN_CODE_MAP = {
    "LF": "\n",
    "CRLF": "\r\n",
    "LFCR": "\n\r",
}


class ReadAllText:
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_util.get_text_input_directory()
        files = [
            f
            for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f))
        ]
        text_files = files
        return {
            "required": {"file_name": (sorted(text_files),)},
            "optional": {"encoding": ("STRING", {"default": "utf-8"})},
        }

    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "file_name")
    FUNCTION = "read"

    def read(self, file_name, encoding=None):
        file = os.path.join(folder_util.get_text_input_directory(), file_name)
        with open(file, mode="r", encoding=encoding) as f:
            return (f.read(), file_name)


class ReadAllLines:
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_util.get_text_input_directory()
        files = [
            f
            for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f))
        ]
        text_files = files
        return {
            "required": {"file_name": (sorted(text_files),)},
            "optional": {"encoding": ("STRING", {"default": "utf-8"})},
        }

    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "file_name")
    OUTPUT_IS_LIST = (True, False)
    FUNCTION = "read"

    def read(self, file_name, encoding=None):
        file = os.path.join(folder_util.get_text_input_directory(), file_name)
        with open(file, mode="r", encoding=encoding) as f:
            return (f.readlines(), file_name)


class WriteText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": ""}),
                "file_name": ("STRING", {"default": "text.txt"}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "mode": (["w", "a"],),
            },
            "optional": {
                "encoding": ("STRING", {"default": "utf-8"}),
                "newline": (_RETURN_CODES,),
            },
        }

    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "write"

    def write(
        self,
        text,
        file_name,
        filename_prefix,
        mode,
        encoding=None,
        newline=None,
    ):
        subfolder = os.path.dirname(os.path.normpath(filename_prefix))
        file_name = (
            os.path.basename(os.path.normpath(filename_prefix)) + "_" + file_name
        )
        full_output_folder = os.path.join(
            folder_util.get_text_output_directory(), subfolder
        )
        os.makedirs(full_output_folder, exist_ok=True)
        file = os.path.join(full_output_folder, file_name)
        newline = _RETURN_CODE_MAP[newline] if newline else None
        with open(file, mode=mode, encoding=encoding, newline=newline) as f:
            f.write(text)

        return {}


class WriteTextWithSequentialNumbering:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": ""}),
                "ext": ("STRING", {"default": ".txt"}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
            "optional": {
                "encoding": ("STRING", {"default": "utf-8"}),
                "newline": (_RETURN_CODES,),
            },
        }

    CATEGORY = NODE_CATEGORY
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "write"

    def write(
        self,
        text,
        ext,
        filename_prefix,
        encoding=None,
        newline=None,
    ):
        full_output_folder, filename, counter, _, _ = folder_paths.get_save_image_path(
            filename_prefix, folder_util.get_text_output_directory()
        )
        file = os.path.join(
            full_output_folder,
            f"{filename}_{counter:05}_{ext}",
        )
        newline = _RETURN_CODE_MAP[newline] if newline else None
        with open(file, mode="w", encoding=encoding, newline=newline) as f:
            f.write(text)
        return {}


class WriteTextLines:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "texts": ("STRING", {"forceInput": True}),
                "file_name": ("STRING", {"default": "text.txt"}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "mode": (["w", "a"],),
            },
            "optional": {
                "encoding": ("STRING", {"default": "utf-8"}),
                "newline": (_RETURN_CODES,),
            },
        }

    CATEGORY = NODE_CATEGORY
    INPUT_IS_LIST = True
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "write"

    def write(
        self,
        texts: list[str],
        file_name: list[str],
        filename_prefix: list[str],
        mode: list[str],
        encoding: Optional[list[str]] = None,
        newline: Optional[list[str]] = None,
    ):
        subfolder = os.path.dirname(os.path.normpath(filename_prefix[0]))
        file_name_ = (
            os.path.basename(os.path.normpath(filename_prefix[0])) + "_" + file_name[0]
        )
        full_output_folder = os.path.join(
            folder_util.get_text_output_directory(), subfolder
        )
        os.makedirs(full_output_folder, exist_ok=True)
        file = os.path.join(folder_util.get_text_output_directory(), file_name_)
        newline_ = _RETURN_CODE_MAP[newline[0]] if newline else None
        encoding_ = encoding[0] if encoding else None
        with open(file, mode=mode[0], encoding=encoding_, newline=newline_) as f:
            for text in texts:
                f.write(text)

        return {}


NODE_CLASS_MAPPINGS = {
    "text_file_util_ReadAllText": ReadAllText,
    "text_file_util_ReadAllLines": ReadAllLines,
    "text_file_util_WriteText": WriteText,
    "text_file_util_WriteTextWithSequentialNumbering": WriteTextWithSequentialNumbering,
    "text_file_util_WriteTextLines": WriteTextLines,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "text_file_util_ReadAllText": "Read All Text",
    "text_file_util_ReadAllLines": "Read All Lines",
    "text_file_util_WriteText": "Write Text",
    "text_file_util_WriteTextWithSequentialNumbering": "Write Text With Sequential Numbering",
    "text_file_util_WriteTextLines": "Write Text Lines (For List)",
}
