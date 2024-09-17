import os
from pathlib import Path
import platform
from .trash_item import TrashItem

if platform.system() == "Windows":
    import winshell

class ITrashManager:
    USER_TRASH = ""

    def list(self, trash_path: str = "") -> list[TrashItem]:
        raise NotImplementedError("Trash Manager doesn't implement this method")


if platform.system() == "Linux":
    class TrashManager(ITrashManager):

        @property
        def USER_TRASH(self) -> str:
            prefix = os.environ.get("XDG_DATA_HOME", "")
            if prefix == "":
                prefix = os.path.expandvars("$HOME/.local/share")
            return os.path.join(prefix, "Trash")

        def list(self, trash_path: str = "") -> list[TrashItem]:
            if trash_path == "":
                trash_path = self.USER_TRASH
            trash_path = Path(trash_path)

            files_path = trash_path / "files"
            trash_data = []

            if files_path.exists():
                for filename in files_path.iterdir():
                    ti = TrashItem.for_trashed_file(str(filename))
                    if ti is not None:
                        trash_data.append(ti)
            return trash_data

elif platform.system() == "Windows":
    class TrashManager(ITrashManager):
        USER_TRASH = os.path.join(os.environ["SystemDrive"], "$Recycle.Bin")

        def list(self, trash_path: str = "") -> list[TrashItem]:
            # NOTE: We ignore trash_path
            items = []
            for winshell_item in winshell.recycle_bin():
                item = TrashItem.for_item(winshell_item)
                items.append(item)
            return items

else:
    class TrashManager(ITrashManager):
        def __init__(self):
            raise NotImplementedError("TrashManager for this OS is not implemented")
