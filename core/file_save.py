import os
from PySide6.QtWidgets import (QMessageBox)
from modules.UML import GameMakerLib as gml
class FileSave():
    def __init__(self):
        super().__init__()
        self.current_project = None

    def save_file_raw(self, path, content):
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            QMessageBox.information(self, "成功", "文件保存成功！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败：{str(e)}")

    def save_file_gm(self, path, content):
        try:
            gml.Write(path, content)
            QMessageBox.information(self, "成功", "文件保存成功！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败：{str(e)}")