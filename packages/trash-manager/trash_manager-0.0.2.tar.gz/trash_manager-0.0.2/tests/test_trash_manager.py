import pytest
import platform

import os

from trash_manager import TrashManager


@pytest.mark.skipif(platform.system() != "Linux", reason="Function specific to linux")
def test__LINUX__TrashManager_USER_TRASH():
    tm = TrashManager()

    if "XDG_DATA_HOME" in os.environ:
        del os.environ["XDG_DATA_HOME"]

    expected_path = os.path.expandvars("$HOME/.local/share/Trash")
    assert tm.USER_TRASH == expected_path

    os.environ["XDG_DATA_HOME"] = "/tmp/home"
    assert tm.USER_TRASH == "/tmp/home/Trash"
    del os.environ["XDG_DATA_HOME"]


def test_TrashManager_list():
    tm = TrashManager()
    assert type(tm.list()) == list
