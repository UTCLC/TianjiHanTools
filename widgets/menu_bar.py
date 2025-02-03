from PySide6.QtWidgets import QMenuBar
from PySide6.QtCore import Signal
from PySide6.QtGui import QKeySequence, QAction
import core.loc as loc

class ProjectMenuBar(QMenuBar):
    new_project = Signal(object)
    open_project = Signal(object)
    save_project = Signal()
    file_explorer_action = Signal()
    exit_action = Signal()
    txt_split_action = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        file_menu = self.addMenu(loc.translate("locFile"))
        
        # 新建工程
        new_action = QAction(loc.translate("locNewInfo"), self)
        new_action.triggered.connect(lambda: self.new_project.emit(self.parent()))
        new_action.setShortcut(QKeySequence.StandardKey.New)
        file_menu.addAction(new_action)
        
        # 打开工程
        open_action = QAction(loc.translate("locOpenInfo"), self)
        open_action.triggered.connect(lambda: self.open_project.emit(self.parent()))
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        # 保存工程
        save_action = QAction(loc.translate("locSaveInfo"), self)
        save_action.triggered.connect(self.save_project.emit)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        file_menu.addAction(save_action)

        export_menu = file_menu.addMenu(loc.translate("locExport"))
        save_zip_action = QAction('.zip', self)
        export_menu.addAction(save_zip_action)

        preferences_action = QAction(loc.translate("locPreferences"), self)
        preferences_action.setShortcut(QKeySequence.StandardKey.Preferences)
        file_menu.addAction(preferences_action)

        file_menu.addSeparator()

        exit_action = QAction(loc.translate("locQuit"), self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.exit_action.emit)
        file_menu.addAction(exit_action)

        edit_menu = self.addMenu(loc.translate("locEdit"))
        build_menu = self.addMenu(loc.translate("locBuild"))

        view_menu = self.addMenu(loc.translate("locView"))

        file_explorer_action = QAction(loc.translate("locFileExplorer"), self)
        file_explorer_action.triggered.connect(self.file_explorer_action.emit)
        view_menu.addAction(file_explorer_action)


        tools_menu = self.addMenu(loc.translate("locTool"))
        txt_split_action = QAction(loc.translate("locLocalizedStrStandardization"), self)
        txt_split_action.triggered.connect(lambda: self.txt_split_action.emit(self.parent()))
        tools_menu.addAction(txt_split_action)


        scripts_menu = self.addMenu(loc.translate("locScript"))
        help_menu = self.addMenu(loc.translate("locHelp"))