import os
import shlex
import subprocess

import pytest

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MGN = "\033[35m"
CYAN = "\033[36m"
RST = "\033[0m"
root_path = os.path.abspath(os.getcwd())
main_file = root_path + "/src/zot2sioyek/zot2sioyek.py"
pdf_file = root_path + "/tests/E5M6X2IH/test.pdf"


def test_files():
    assert os.path.exists(pdf_file)
    assert os.path.exists(main_file)


def test_shlex():
    command = "-d -g Brian"
    as_list = ["-d", "-g", "Brian"]
    assert shlex.split(command) == as_list


test_cases = [
    ("", 1, "python zot2sioyek.py [FLAG] [ARGUMENTS]"),
    (
        "--help zotero",
        5,
        "If any necessary argument is not given, the user will be prompted to input it.",
    ),
]

@pytest.mark.parametrize(
    "command, line, expected_output",
    [
        ("", 1, "python zot2sioyek.py [FLAG] [ARGUMENTS]"),
        ( "--help zotero", 4, "Print all highlights from a given zotero file."),
    ],
)
def test_help(command, line, expected_output):
    full_command = ["python", main_file] + shlex.split(command)
    result = subprocess.run(full_command, capture_output=True, text=True)
    output = result.stdout.split("\n")[int(line)]
    assert output == expected_output

