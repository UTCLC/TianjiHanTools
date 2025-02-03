import os
from PySide6.QtWidgets import (QMessageBox)
from modules.UML import GameMakerLib as gml
import core.loc as loc
class FileSave():
    def __init__(self):
        super().__init__()
        self.current_project = None

    def save_file_raw(self, path, content):
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            QMessageBox.information(self, loc.translate("locSuccess"), loc.translate("locProjectSaved"))
        except Exception as e:
            QMessageBox.critical(self, loc.translate("locError"), loc.translate("locProjectLoadFailed")+str(e))

    def save_file_gm(self, path, content):
        try:
            gml.Write(path, content)
            QMessageBox.information(self, loc.translate("locSuccess"), loc.translate("locProjectSaved"))
        except Exception as e:
            QMessageBox.critical(self, loc.translate("locError"), loc.translate("locProjectLoadFailed")+str(e))