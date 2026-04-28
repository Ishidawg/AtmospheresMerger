from PySide6.QtWidgets import QMessageBox, QWidget
from script.merge import merge_atmospheres
import sys
import os


def get_default_game_path() -> str:
    if sys.platform.startswith("linux"):
        linux_path = "~/.local/share/Steam/steamapps/common/Dark Souls II Scholar of the First Sin/Game/ds2le_atmosphere_presets/atmospheres_extended.ini"
        return os.path.expanduser(linux_path)
    elif sys.platform == "win32":
        return r"C:\Program Files (x86)\Steam\steamapps\common\Dark Souls II Scholar of the First Sin\Game\ds2le_atmosphere_presets\atmospheres_extended.ini"
    return "Not Found"


def run_merge(parent: QWidget, game_path: str, community_path: str, selected_sections: list[str]) -> None:
    if not game_path or not community_path:
        QMessageBox.warning(
            parent,
            "Missing Files",
            "Please select both files before merging."
        )
        return

    try:
        merge_atmospheres(game_path, community_path, selected_sections)
        QMessageBox.information(parent, "Success", "Atmospheres merged!")
    except FileNotFoundError as e:
        QMessageBox.critical(parent, "File Not Found", str(e))
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"Error at:\n{str(e)}")
