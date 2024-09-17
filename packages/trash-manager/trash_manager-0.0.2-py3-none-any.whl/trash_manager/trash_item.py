from __future__ import annotations
import datetime
import platform
from pathlib import Path
from . import config

if platform.system() == "Windows":
    import winshell


class ITrashItem:
    def __init__(self, original_path: str, deletion_date: datetime.datetime):
        self.original_path = original_path
        self.deletion_date = deletion_date
    
    def recover(self, recover_to: str = ""):
        raise NotImplementedError("This function is not implemented for this OS")


if platform.system() == "Linux":
    class TrashItem(ITrashItem):
        def __init__(self, original_path: str, deletion_date: datetime.datetime, trashed_path: str, trashinfo_path: str):
            ITrashItem.__init__(self, original_path, deletion_date)
            self.trashed_path = trashed_path
            self.trashinfo_path = trashinfo_path

        @staticmethod
        def for_trashed_file(path: str) -> TrashItem:
            def find_tag(start: int, tag: str):
                pos = content.find(tag, start)
                if pos == -1: return -1, -1
                end_pos = content.find(b'\n', pos)
                return (pos + len(tag), end_pos) if end_pos != -1 else (-1, -1)

            trash_info_tag = b"[Trash Info]"
            path_tag = b"Path="
            deletion_date_tag = b"DeletionDate="

            path = Path(path)
            trashinfo_path = path.parent.parent / "info" / (path.name + ".trashinfo")
            with open(str(trashinfo_path), 'rb') as f:
                content = f.read()

            trash_info_pos = content.find(trash_info_tag)
            if trash_info_pos == -1:
                return None

            path_pos, path_end_pos = find_tag(trash_info_pos, path_tag)
            deletion_date_pos, deletion_date_end_pos = find_tag(trash_info_pos, deletion_date_tag)
            if path_pos == -1 or deletion_date_pos == -1:
                return None

            path_value = content[path_pos:path_end_pos].decode()
            deletion_date_value = datetime.datetime.fromisoformat(content[deletion_date_pos:deletion_date_end_pos].decode())
            return TrashItem(path_value, deletion_date_value, str(path), str(trashinfo_path))

        def recover(self, recover_to: str = ""):
            if recover_to == "":
                recover_to = self.original_path
            recover_to = Path(recover_to)
            trashed_file = Path(self.trashed_path)
            trashinfo_file = Path(self.trashinfo_path)

            if recover_to.exists():
                raise FileExistsError("A file exists in the trashed file's place")

            trashed_file.rename(str(recover_to))
            trashinfo_file.unlink(True)

elif platform.system() == "Windows":
    class TrashItem(ITrashItem):
        def __init__(self, original_path: str, deletion_date: datetime.datetime, item: winshell.ShellRecycledItem):
            ITrashItem.__init__(self, original_path, deletion_date)
            self.item = item
        
        @staticmethod
        def for_item(item: winshell.ShellRecycledItem) -> TrashItem:
            return TrashItem(item.original_filename(), item.recycle_date(), item)
        
        def recover(self, recover_to: str = ""):
            if recover_to == "":
                recover_to = self.original_path
            
            winshell.move_file(
                self.item.real_filename(),
                recover_to,
                allow_undo=config.WINDOWS_TrashItem_recover__ALLOW_UNDO,
                no_confirm=config.WINDOWS_TrashItem_recover__NO_CONFIRM,
                rename_on_collision=config.WINDOWS_TrashItem_recover__RENAME_ON_COLLISION,
                silent=config.WINDOWS_TrashItem_recover__SILENT
            )