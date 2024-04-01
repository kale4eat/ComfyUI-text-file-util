import os

import folder_paths

_text_input_directory = os.path.join(
    os.path.dirname(os.path.realpath(folder_paths.__file__)), "text_input"
)

_text_output_directory = os.path.join(
    os.path.dirname(os.path.realpath(folder_paths.__file__)), "text_output"
)


def get_text_input_directory():
    global _text_input_directory
    return _text_input_directory


def get_text_output_directory():
    global _text_output_directory
    return _text_output_directory


def initiarize():
    os.makedirs(get_text_input_directory(), exist_ok=True)
    os.makedirs(get_text_output_directory(), exist_ok=True)
