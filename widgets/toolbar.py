from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Signal, QSize

class MainToolBar(QToolBar):
    new_project = Signal(object)
    open_project = Signal(object)
    save_project = Signal()
    run_action = Signal()

    def __init__(self, parent=None):
        super().__init__("主工具栏", parent)
        self.init_ui()
        self.setMovable(False)
        self.setIconSize(QSize(24, 24))

    def init_ui(self):
        # 新建按钮
        new_action = QAction(QIcon("assets/icons/new.png"), "新建", self)
        new_action.triggered.connect(lambda: self.new_project.emit(self.parent()))
        new_action.setToolTip("新建工程 (Ctrl+N)")
        self.addAction(new_action)

        # 打开按钮
        open_action = QAction(QIcon("assets/icons/open.png"), "打开", self)
        open_action.triggered.connect(lambda: self.open_project.emit(self.parent()))
        open_action.setToolTip("打开工程 (Ctrl+O)")
        self.addAction(open_action)

        # 保存按钮
        save_action = QAction(QIcon("assets/icons/save.png"), "保存", self)
        save_action.triggered.connect(self.save_project.emit)
        save_action.setToolTip("保存工程 (Ctrl+S)")
        self.addAction(save_action)

        self.addSeparator()

        # 运行按钮
        run_action = QAction(QIcon("assets/icons/run.png"), "运行", self)
        run_action.triggered.connect(self.run_action.emit)
        run_action.setToolTip("运行工程 (F5)")
        self.addAction(run_action)