from PySide6.QtWidgets import (QDockWidget, QTreeWidget, QTreeWidgetItem,
                               QLineEdit, QCheckBox, QHBoxLayout, QVBoxLayout, QWidget)
from PySide6.QtCore import Qt, Signal
import os
import re

class FileExplorer(QDockWidget):
    file_double_clicked = Signal(str)  # 发送相对路径
    
    def __init__(self, parent=None):
        super().__init__("文件浏览器", parent)
        self.data = [{},{}]
        
        # 创建搜索组件
        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("搜索...")
        self.regex_checkbox = QCheckBox("正则表达式")
        
        # 创建布局
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_line)
        search_layout.addWidget(self.regex_checkbox)
        
        # 创建树部件
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("项目文件")
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)

        # 主容器布局
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.tree)
        self.setWidget(container)
        
        # 连接信号
        self.search_line.textChanged.connect(self.update_filter)
        self.regex_checkbox.stateChanged.connect(self.update_filter)

    def update_filter(self):
        """更新树形结构的过滤状态"""
        search_text = self.search_line.text()
        use_regex = self.regex_checkbox.isChecked()
        self.filter_items(search_text, use_regex)

    def filter_items(self, text, use_regex):
        """过滤树形结构项"""
        try:
            pattern = re.compile(text, re.IGNORECASE) if use_regex and text else None
        except re.error:
            return  # 忽略无效的正则表达式

        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            item = root.child(i)
            self._filter_item(item, text, pattern, use_regex)

    def _filter_item(self, item, text, pattern, use_regex):
        """递归过滤树节点"""
        child_visible = False
        # 先处理子节点
        for i in range(item.childCount()):
            child = item.child(i)
            if self._filter_item(child, text, pattern, use_regex):
                child_visible = True

        # 检查当前节点是否匹配
        match = False
        if not text:  # 空搜索字符串显示所有
            match = True
        else:
            item_text = item.text(0)
            if use_regex and pattern:
                match = bool(pattern.search(item_text))
            else:
                match = text.lower() in item_text.lower()

        # 显示逻辑：自身匹配或子节点可见
        is_visible = match or child_visible
        item.setHidden(not is_visible)
        
        # 展开匹配的父节点
        if is_visible and item.parent():
            item.parent().setExpanded(True)
            
        return is_visible

    def on_item_double_clicked(self, item):
        if not item.childCount():
            rel_path = item.data(0, Qt.ItemDataRole.UserRole)
            if rel_path:
                self.file_double_clicked.emit(rel_path)

    def load_project(self, project_data):
        self.tree.clear()
        if not project_data:
            return

        source_dir = project_data['source']
        self._populate_tree(self.tree, source_dir, project_data)
        self.tree.expandToDepth(1)  # 默认展开一级目录

    def _populate_tree(self, parent, path, base_data):
        for item_name in sorted(os.listdir(path)):
            item_path = os.path.join(path, item_name)
            node = QTreeWidgetItem(parent)
            node.setText(0, item_name)
            if os.path.isdir(item_path):
                self._populate_tree(node, item_path, base_data)
            elif item_name.endswith('.win'):
                self._populate_tree_gm(node, item_path, base_data)
            else:
                rel_path = os.path.relpath(item_path, base_data['source'])
                node.setData(0, Qt.ItemDataRole.UserRole, f"file:{rel_path}")

    def _populate_tree_gm(self, parent, path, base_data):
        from modules.UML import GameMakerLib as gml
        rel_path = os.path.relpath(path, base_data['source'])
        self.data[0][rel_path] = gml.Read(base_data['source'] + "/" + rel_path)
        self.data[1][rel_path] = gml.Read(base_data['target'] + "/" + rel_path)

        pnode = QTreeWidgetItem(parent)
        pnode.setText(0, "Strings")
        for i in range(len(self.data[0][rel_path].Strings)):
            node = QTreeWidgetItem(pnode)
            node.setText(0, self.data[0][rel_path].Strings[i].Content)
            node.setToolTip(0, str(i))
            node.setData(0, Qt.ItemDataRole.UserRole, f"gm:{rel_path}/GMStrings/{i}")

        pnode = QTreeWidgetItem(parent)
        pnode.setText(0, "Fonts")
        for i in range(len(self.data[0][rel_path].Fonts)):
            node = QTreeWidgetItem(pnode)
            node.setText(0, self.data[0][rel_path].Fonts[i].Name.Content)
            node.setToolTip(0, str(i))
            node.setData(0, Qt.ItemDataRole.UserRole, f"gm:{rel_path}/GMFonts/{i}")

    def show_or_close(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()