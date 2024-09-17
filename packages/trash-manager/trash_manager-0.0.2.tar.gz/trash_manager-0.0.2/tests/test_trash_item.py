import pytest
import platform
import datetime

import os

from trash_manager import TrashItem


@pytest.mark.skipif(platform.system() != "Linux", reason="Function specific to linux")
def test__LINUX__TrashItem_for_trashed_file(tmp_path):
    # Prepare fake data
    original_filepath = "/tmp/my_file"
    deletion_date = "2024-08-07T01:53:48"
    data = f"""
[Trash Info]
Path={original_filepath}
DeletionDate={deletion_date}
""".encode()

    # Prepare fake trash
    os.mkdir(os.path.join(tmp_path, "Trash"))
    os.mkdir(os.path.join(tmp_path, "Trash", "files"))
    os.mkdir(os.path.join(tmp_path, "Trash", "info"))

    # Create a fake trashed file
    trashed_filepath = os.path.join(tmp_path, "Trash", "files", "from_fileinfo")
    open(trashed_filepath, 'w').close()

    # Create a fake trashinfo file
    trashinfo_filepath = os.path.join(tmp_path, "Trash", "info", "from_fileinfo.trashinfo")
    with open(trashinfo_filepath, 'wb') as f:
        f.write(data)

    # Test the alternative constructor
    ti = TrashItem.for_trashed_file(trashed_filepath)
    assert ti.trashinfo_path == trashinfo_filepath
    assert ti.trashed_path == trashed_filepath
    assert ti.original_path == original_filepath
    assert ti.deletion_date == datetime.datetime.fromisoformat(deletion_date)

@pytest.mark.skipif(platform.system() != "Windows", reason="Function specific to windows")
def test__WINDOWS__TrashItem_for_trashed_file(tmp_path):
    import winshell

    # Create a file
    my_file = os.path.realpath(os.path.join(tmp_path, "todelete"))
    open(my_file, 'w').close()

    # Delete the file
    winshell.delete_file(my_file, True, True, True)

    # Find the file
    items = sorted(filter(lambda x: x.original_filename() == my_file, winshell.recycle_bin()), key=lambda x: x.recycle_date(), reverse=True)
    assert len(items) > 0
    my_file_item = items[0]

    # Test the alternative constructor
    ti = TrashItem.for_item(my_file_item)
    assert ti.item == my_file_item
    assert ti.original_path == my_file
    assert ti.deletion_date == my_file_item.recycle_date()

@pytest.mark.skipif(platform.system() != "Linux", reason="Function specific to linux")
def test__LINUX__TrashItem_recover(tmp_path):
    # Prepare fake data
    original_filepath = f"{tmp_path}/my_file"
    deletion_date = "2024-08-07T01:53:48"
    data = f"""
    [Trash Info]
    Path={original_filepath}
    DeletionDate={deletion_date}
    """.encode()

    # Prepare fake trash
    os.mkdir(os.path.join(tmp_path, "Trash"))
    os.mkdir(os.path.join(tmp_path, "Trash", "files"))
    os.mkdir(os.path.join(tmp_path, "Trash", "info"))

    # Create a fake trashed file
    trashed_filepath = os.path.join(tmp_path, "Trash", "files", "my_file")
    open(trashed_filepath, 'w').close()

    # Create a fake trashinfo file
    trashinfo_filepath = os.path.join(tmp_path, "Trash", "info", "my_file.trashinfo")
    with open(trashinfo_filepath, 'wb') as f:
        f.write(data)

    ti = TrashItem.for_trashed_file(trashed_filepath)
    ti.recover()

    assert os.path.exists(original_filepath)
    assert not os.path.exists(trashed_filepath)
    assert not os.path.exists(trashinfo_filepath)


@pytest.mark.skipif(platform.system() != "Windows", reason="Function specific to windows")
def test__WINDOWS__TrashItem_recover(tmp_path):
    import winshell

    # Prepare paths
    original_filepath = os.path.join(tmp_path, "my_file")

    # Create and delete a file
    open(original_filepath, 'w').close()
    winshell.delete_file(original_filepath, True, True, True)

    # Find deleted file
    items = sorted(filter(lambda x: x.original_filename() == original_filepath, winshell.recycle_bin()), key=lambda x: x.recycle_date(), reverse=True)
    assert len(items) > 0
    my_file_item = items[0]

    ti = TrashItem.for_item(my_file_item)
    ti.recover()

    assert os.path.exists(original_filepath)