import sys
from PySide6.QtWidgets import (QMainWindow, QTabWidget, QWidget,
                             QVBoxLayout, QPushButton, QFileDialog, 
                             QMessageBox, QTreeWidgetItem,QMenu)
from PySide6.QtCore import Qt, QTimer
import os
import json
import datetime
from editors.text_editor import TextEditor

from core.file_save import FileSave as fs

class LocalizationIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_basic_ui()
        self._deferred_init()

    def _init_basic_ui(self):
        # 极简初始化
        self.setWindowTitle("天机汉化工具 | TianjiHanTools")
        self.resize(1200, 800)
        self.setCentralWidget(QWidget())
        self.setWindowState(Qt.WindowActive)

    def _deferred_init(self):
        # 分阶段加载
        QTimer.singleShot(100, self._stage1_init)
        QTimer.singleShot(500, self._stage2_init)

    def _stage1_init(self):
        """第一阶段：加载可见组件"""
        # 初始化菜单栏
        from widgets.menu_bar import ProjectMenuBar
        self.menu_bar = ProjectMenuBar()
        self.setMenuBar(self.menu_bar)
        # 立即显示进度
        self.statusBar().showMessage("正在加载核心组件...")

    def _stage2_init(self):
        from editors.json_editor import JSONEditor
        from editors.csv_editor import CSVEditor
        from editors.gm.gm_strings_editor import GMStringsEditor

        from core.project_manager import ProjectManager

        self.current_editors = {}
        self.editor_types = {
            'txt': TextEditor,
            'json': JSONEditor,
            'csv': CSVEditor,
            'GMStrings': GMStringsEditor
        }
        # 初始化核心模块
        self.project_manager = ProjectManager()
        self.project_manager.project_loaded.connect(self.on_project_loaded)
        self.project_manager.project_saved.connect(self.on_project_saved)
        self.project_manager.error_occurred.connect(self.show_error)
        self.init_ui()

    def init_ui(self):
        from widgets.menu_bar import ProjectMenuBar
        from widgets.file_explorer import FileExplorer
        from widgets.toolbar import MainToolBar

        # 初始化菜单栏
        self.menu_bar = ProjectMenuBar()
        self.menu_bar.new_project.connect(self.project_manager.new_project)
        self.menu_bar.open_project.connect(self.project_manager.open_project)
        self.menu_bar.save_project.connect(self.project_manager.save_project)
        self.menu_bar.exit_action.connect(self.exit)
        self.setMenuBar(self.menu_bar)

        # 文件浏览器
        self.file_explorer = FileExplorer()
        self.file_explorer.file_double_clicked.connect(self.open_file)
        self.menu_bar.file_explorer_action.connect(self.file_explorer.show_or_close)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.file_explorer)

        # 初始化工具栏
        self.tool_bar = MainToolBar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tool_bar)
        self.tool_bar.new_project.connect(self.project_manager.new_project)
        self.tool_bar.open_project.connect(self.project_manager.open_project)
        self.tool_bar.save_project.connect(self.project_manager.save_project)
        
        # 主编辑区域
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)  # 启用关闭按钮
        self.tabs.tabCloseRequested.connect(self.close_tab)  # 连接关闭信号
        self.tabs.setContextMenuPolicy(Qt.CustomContextMenu)  # 启用右键菜单
        self.tabs.customContextMenuRequested.connect(self.show_tab_context_menu)
        self.tabs.setMovable(True)
        self.setCentralWidget(self.tabs)

        self.statusBar().showMessage("准备就绪", 3000)

    def exit(self):
        reply = QMessageBox.question(
            self,
            '确认退出',
            '确定要退出程序吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def on_project_loaded(self, project_data):
        """处理工程加载完成"""
        self.file_explorer.load_project(project_data)
        QMessageBox.information(self, "成功", "工程加载成功！")

    def on_project_saved(self):
        """处理工程保存完成"""
        QMessageBox.information(self, "成功", "工程保存成功！")

    def show_error(self, message):
        """显示错误信息"""
        QMessageBox.critical(self, "错误", message)

    def open_project(self):
        project_folder = QFileDialog.getExistingDirectory(self, "选择工程文件夹")
        if not project_folder:
            return

        project_file = os.path.join(project_folder, 'project.json')
        if not os.path.exists(project_file):
            QMessageBox.critical(self, "错误", "无效的工程目录")
            return

        try:
            with open(project_file, 'r') as f:
                self.project_data = json.load(f)
            
            self.file_explorer.load_project(self.project_data)
            QMessageBox.information(self, "成功", "工程加载成功！")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载工程失败：{str(e)}")

    def save_project(self):
        if not self.project_data:
            return

        try:
            project_file = os.path.join(self.project_data['project_path'], 'project.json')
            self.project_data['last_modified'] = datetime.datetime.now().isoformat()
            
            with open(project_file, 'w') as f:
                json.dump(self.project_data, f, indent=4)
            
            QMessageBox.information(self, "成功", "工程保存成功！")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败：{str(e)}")

    def _populate_tree(self, parent, path):
        if os.path.isdir(path):
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                node = QTreeWidgetItem(parent)
                node.setText(0, item)
                
                if os.path.isdir(item_path):
                    self._populate_tree(node, item_path)
                else:
                    node.setData(0, Qt.ItemDataRole.UserRole, os.path.relpath(item_path, self.project_data['source']))
    
    def open_file(self, rel_path):
        type, rel_path = rel_path.split(":", 1)
        if type == "file":
            ext = rel_path.rsplit('.', 1)[1]
            editor_class = self.editor_types.get(ext, TextEditor)
            if rel_path in self.current_editors:
                self.tabs.setCurrentWidget(self.current_editors[rel_path])
                return
            source_path = os.path.join(self.project_manager.current_project['source'], rel_path)
            target_path = os.path.join(self.project_manager.current_project['target'], rel_path)
            editor = editor_class(source_path, target_path)
            tab = QWidget()
            tab.rel_path = rel_path  # 存储关联文件路径
            layout = QVBoxLayout(tab)
            layout.addWidget(editor)
            save_btn = QPushButton("保存")
            save_btn.clicked.connect(lambda: fs.save_file_raw(self, target_path, editor.get_content()))
            layout.addWidget(save_btn)
            self.tabs.addTab(tab, os.path.basename(rel_path))
            self.current_editors[rel_path] = tab
            self.tabs.setCurrentWidget(tab)

        if type == "gm":
            ext_using = ".win"
            if (rel_path.contains(".droid")):
                ext_using = ".droid"
            elif (rel_path.contains(".ios")):
                ext_using = ".ios"
            data_path, ext = rel_path.split(ext_using+'/',1)
            ext, id = ext.split('/',1)
            editor_class = self.editor_types.get(ext)
            if rel_path in self.current_editors:
                self.tabs.setCurrentWidget(self.current_editors[rel_path])
                return
            data_path = data_path + ext_using
            editor = editor_class(self.file_explorer.data[0][data_path], self.file_explorer.data[1][data_path], id)
            tab = QWidget()
            tab.rel_path = rel_path
            layout = QVBoxLayout(tab)
            layout.addWidget(editor)
            save_btn = QPushButton("写入 data")
            target_path = os.path.join(self.project_manager.current_project['target'], data_path)
            save_btn.clicked.connect(lambda: fs.save_file_gm(self, target_path, self.file_explorer.data[1][data_path]))
            layout.addWidget(save_btn)
            self.tabs.addTab(tab, f"{ext}:{id}")
            self.current_editors[rel_path] = tab
            self.tabs.setCurrentWidget(tab)

    def close_tab(self, index):
        """ 关闭指定索引的标签页 """
        widget = self.tabs.widget(index)
        if widget and hasattr(widget, 'rel_path'):
            # 从当前编辑器记录中移除
            if widget.rel_path in self.current_editors:
                del self.current_editors[widget.rel_path]
            widget.deleteLater()
            self.tabs.removeTab(index)

    def show_tab_context_menu(self, pos):
        """ 显示标签页右键菜单 """
        index = self.tabs.tabBar().tabAt(pos)
        if index >= 0:
            menu = QMenu()
            # 添加菜单项
            close_action = menu.addAction("关闭当前标签页")
            close_others_action = menu.addAction("关闭其他标签页")
            close_all_action = menu.addAction("关闭所有标签页")
            
            action = menu.exec_(self.tabs.mapToGlobal(pos))
            
            if action == close_action:
                self.close_tab(index)
            elif action == close_others_action:
                self._close_other_tabs(index)
            elif action == close_all_action:
                self._close_all_tabs()

    def _close_other_tabs(self, current_index):
        """ 关闭除当前标签外的其他标签 """
        for i in reversed(range(self.tabs.count())):
            if i != current_index:
                self.close_tab(i)

    def _close_all_tabs(self):
        """ 关闭所有标签页 """
        for i in reversed(range(self.tabs.count())):
            self.close_tab(i)