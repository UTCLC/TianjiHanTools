from PySide6.QtWidgets import QMenuBar
from PySide6.QtCore import Signal
from PySide6.QtGui import QKeySequence, QAction

class ProjectMenuBar(QMenuBar):
    new_project = Signal(object)
    open_project = Signal(object)
    save_project = Signal()
    file_explorer_action = Signal()
    exit_action = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        file_menu = self.addMenu('文件')
        
        # 新建工程
        new_action = QAction('新建工程', self)
        new_action.triggered.connect(lambda: self.new_project.emit(self.parent()))
        new_action.setShortcut(QKeySequence.StandardKey.New)
        file_menu.addAction(new_action)
        
        # 打开工程
        open_action = QAction('打开工程', self)
        open_action.triggered.connect(lambda: self.open_project.emit(self.parent()))
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        # 保存工程
        save_action = QAction('保存工程', self)
        save_action.triggered.connect(self.save_project.emit)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        file_menu.addAction(save_action)

        export_menu = file_menu.addMenu("导出")
        save_zip_action = QAction('通用压缩格式 (.zip)', self)
        export_menu.addAction(save_zip_action)

        preferences_action = QAction('首选项', self)
        preferences_action.setShortcut(QKeySequence.StandardKey.Preferences)
        file_menu.addAction(preferences_action)

        file_menu.addSeparator()

        exit_action = QAction('退出', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.exit_action.emit)
        file_menu.addAction(exit_action)

        edit_menu = self.addMenu('编辑')
        build_menu = self.addMenu('构建')

        view_menu = self.addMenu('视图')

        file_explorer_action = QAction('文件浏览器', self)
        file_explorer_action.triggered.connect(self.file_explorer_action.emit)
        view_menu.addAction(file_explorer_action)


        tools_menu = self.addMenu('工具')
        scripts_menu = self.addMenu('脚本')
        help_menu = self.addMenu('帮助')