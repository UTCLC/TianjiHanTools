from PySide6.QtWidgets import (QDockWidget, QTreeWidget, QTreeWidgetItem,
                               QLineEdit, QCheckBox, QHBoxLayout, QVBoxLayout, 
                               QWidget, QPushButton, QFileDialog, QTabWidget,
                               QDialog, QLabel, QComboBox, QDialogButtonBox,
                               QMessageBox, QGroupBox)
from PySide6.QtCore import Qt, Signal
import json
import os
import re
from collections import defaultdict
import loc

jap = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7A3]')

class RuleDialog(QDialog):
    def __init__(self, rule=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(loc.translate("locRuleEditor") if rule else loc.translate("locAddRule"))
        layout = QVBoxLayout(self)
        
        self.name_label = QLabel(loc.translate("locNameInfo")+":")
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        
        self.type_label = QLabel(loc.translate("locTypeInfo")+":")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["start_with", "regex", "contains_space", "default"])
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)
        
        self.param_label = QLabel(loc.translate("locParam")+":")
        self.param_edit = QLineEdit()
        layout.addWidget(self.param_label)
        layout.addWidget(self.param_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.type_combo.currentTextChanged.connect(self.update_ui)
        if rule:
            self.name_edit.setText(rule['name'])
            self.type_combo.setCurrentText(rule['type'])
            self.param_edit.setText(rule.get('param', ''))
        self.update_ui()
    
    def update_ui(self):
        type_ = self.type_combo.currentText()
        if type_ in ["default", "contains_space"]:
            self.param_edit.setEnabled(False)
        else:
            self.param_edit.setEnabled(True)

class ToolTxTFormatLate(QDockWidget):
    file_double_clicked = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(loc.translate("locLocalizedStrStandardization"), parent)
        self.classification_rules = [
            {'name': 'starred', 'type': 'start_with', 'param': '*'},
            {'name': 'spaced', 'type': 'regex', 'param': r'[\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7A3 ]'},
            {'name': 'others', 'type': 'default'}
        ]
        
        self.tabs = QTabWidget()
        self.classification_tab = QWidget()
        self.create_classification_tab()
        self.tabs.addTab(self.create_convert_tab(), loc.translate("locConvert"))
        self.tabs.addTab(self.create_merge_tab(), loc.translate("locMerge"))
        self.tabs.addTab(self.create_upgrade_tab(), loc.translate("locUpgrade"))
        self.tabs.addTab(self.classification_tab, loc.translate("locClassification"))
        
        self.setWidget(self.tabs)
        self.update_rules_tree()

    def create_convert_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        group = QGroupBox(loc.translate("locConvertTxt2Json"))
        group_layout = QVBoxLayout()
        
        self.convert_input_edit = QLineEdit()
        self.convert_input_btn = QPushButton(loc.translate("locSelectInputFile"))
        self.convert_output_edit = QLineEdit()
        self.convert_output_btn = QPushButton(loc.translate("locSelectOutputDir"))
        self.convert_btn = QPushButton(loc.translate("locConvert"))
        
        group_layout.addWidget(QLabel(loc.translate("locInputFile")))
        group_layout.addWidget(self.convert_input_edit)
        group_layout.addWidget(self.convert_input_btn)
        group_layout.addWidget(QLabel(loc.translate("locOutputDir")))
        group_layout.addWidget(self.convert_output_edit)
        group_layout.addWidget(self.convert_output_btn)
        group_layout.addWidget(self.convert_btn)
        group.setLayout(group_layout)
        
        layout.addWidget(group)
        layout.addStretch()
        
        # 连接信号
        self.convert_input_btn.clicked.connect(lambda: self.select_file(self.convert_input_edit))
        self.convert_output_btn.clicked.connect(lambda: self.select_directory(self.convert_output_edit))
        self.convert_btn.clicked.connect(self.do_convert)
        
        return tab

    def create_merge_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        group = QGroupBox(loc.translate("locMergeJson2Txt"))
        group_layout = QVBoxLayout()
        
        self.merge_input_edit = QLineEdit()
        self.merge_input_btn = QPushButton(loc.translate("locSelectInputDir"))
        self.merge_output_edit = QLineEdit()
        self.merge_output_btn = QPushButton(loc.translate("locSelectOutputFile"))
        self.merge_btn = QPushButton(loc.translate("locMerge"))
        
        group_layout.addWidget(QLabel(loc.translate("locInputDir")))
        group_layout.addWidget(self.merge_input_edit)
        group_layout.addWidget(self.merge_input_btn)
        group_layout.addWidget(QLabel(loc.translate("locOutputFile")))
        group_layout.addWidget(self.merge_output_edit)
        group_layout.addWidget(self.merge_output_btn)
        group_layout.addWidget(self.merge_btn)
        group.setLayout(group_layout)
        
        layout.addWidget(group)
        layout.addStretch()
        
        # 连接信号
        self.merge_input_btn.clicked.connect(lambda: self.select_directory(self.merge_input_edit))
        self.merge_output_btn.clicked.connect(lambda: self.save_file(self.merge_output_edit))
        self.merge_btn.clicked.connect(self.do_merge)
        
        return tab

    def create_upgrade_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        group = QGroupBox(loc.translate("locUpgradeTxt"))
        group_layout = QVBoxLayout()
        
        self.upgrade_old_txt_edit = QLineEdit()
        self.upgrade_old_txt_btn = QPushButton(loc.translate("locSelectOldTxt"))
        self.upgrade_old_json_edit = QLineEdit()
        self.upgrade_old_json_btn = QPushButton(loc.translate("locSelectOldJson"))
        self.upgrade_new_txt_edit = QLineEdit()
        self.upgrade_new_txt_btn = QPushButton(loc.translate("locSelectNewTxt"))
        self.upgrade_output_edit = QLineEdit()
        self.upgrade_output_btn = QPushButton(loc.translate("locSelectOutputDir"))
        self.upgrade_btn = QPushButton(loc.translate("locUpgrade"))
        
        group_layout.addWidget(QLabel(loc.translate("locOldTxt")))
        group_layout.addWidget(self.upgrade_old_txt_edit)
        group_layout.addWidget(self.upgrade_old_txt_btn)
        group_layout.addWidget(QLabel(loc.translate("locNewTxt")))
        group_layout.addWidget(self.upgrade_old_json_edit)
        group_layout.addWidget(self.upgrade_old_json_btn)
        group_layout.addWidget(QLabel(loc.translate("locOutputDir")))
        group_layout.addWidget(self.upgrade_new_txt_edit)
        group_layout.addWidget(self.upgrade_new_txt_btn)
        group_layout.addWidget(QLabel(loc.translate("locOutputDir")))
        group_layout.addWidget(self.upgrade_output_edit)
        group_layout.addWidget(self.upgrade_output_btn)
        group_layout.addWidget(self.upgrade_btn)
        group.setLayout(group_layout)
        
        layout.addWidget(group)
        layout.addStretch()
        
        # 连接信号
        self.upgrade_old_txt_btn.clicked.connect(lambda: self.select_file(self.upgrade_old_txt_edit))
        self.upgrade_old_json_btn.clicked.connect(lambda: self.select_directory(self.upgrade_old_json_edit))
        self.upgrade_new_txt_btn.clicked.connect(lambda: self.select_file(self.upgrade_new_txt_edit))
        self.upgrade_output_btn.clicked.connect(lambda: self.select_directory(self.upgrade_output_edit))
        self.upgrade_btn.clicked.connect(self.do_upgrade)
        
        return tab

    def create_classification_tab(self):
        layout = QVBoxLayout(self.classification_tab)
        self.rules_tree = QTreeWidget()
        self.rules_tree.setHeaderLabels([loc.translate("locName"), loc.translate("locType"), loc.translate("locParam")])
        layout.addWidget(self.rules_tree)
        
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton(loc.translate("locAdd"))
        self.edit_btn = QPushButton(loc.translate("locEdit"))
        self.delete_btn = QPushButton(loc.translate("locDelete"))
        self.up_btn = QPushButton(loc.translate("locMoveUp"))
        self.down_btn = QPushButton(loc.translate("locMoveDn"))
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.up_btn)
        btn_layout.addWidget(self.down_btn)
        layout.addLayout(btn_layout)
        
        self.add_btn.clicked.connect(self.add_rule)
        self.edit_btn.clicked.connect(self.edit_rule)
        self.delete_btn.clicked.connect(self.delete_rule)
        self.up_btn.clicked.connect(self.move_rule_up)
        self.down_btn.clicked.connect(self.move_rule_down)

    def update_rules_tree(self):
        self.rules_tree.clear()
        for rule in self.classification_rules:
            item = QTreeWidgetItem([rule['name'], rule['type'], rule.get('param', '')])
            self.rules_tree.addTopLevelItem(item)

    def add_rule(self):
        dlg = RuleDialog()
        if dlg.exec():
            new_rule = {
                'name': dlg.name_edit.text(),
                'type': dlg.type_combo.currentText(),
                'param': dlg.param_edit.text() if dlg.type_combo.currentText() not in ['default', 'contains_space'] else ''
            }
            self.classification_rules.append(new_rule)
            self.update_rules_tree()

    def edit_rule(self):
        item = self.rules_tree.currentItem()
        if not item: return
        
        index = self.rules_tree.indexOfTopLevelItem(item)
        rule = self.classification_rules[index]
        dlg = RuleDialog(rule)
        if dlg.exec():
            self.classification_rules[index] = {
                'name': dlg.name_edit.text(),
                'type': dlg.type_combo.currentText(),
                'param': dlg.param_edit.text() if dlg.type_combo.currentText() not in ['default', 'contains_space'] else ''
            }
            self.update_rules_tree()

    def delete_rule(self):
        item = self.rules_tree.currentItem()
        if not item: return
        
        index = self.rules_tree.indexOfTopLevelItem(item)
        del self.classification_rules[index]
        self.update_rules_tree()

    def move_rule_up(self):
        index = self.rules_tree.indexOfTopLevelItem(self.rules_tree.currentItem())
        if index > 0:
            self.classification_rules.insert(index-1, self.classification_rules.pop(index))
            self.update_rules_tree()

    def move_rule_down(self):
        index = self.rules_tree.indexOfTopLevelItem(self.rules_tree.currentItem())
        if index < len(self.classification_rules)-1:
            self.classification_rules.insert(index+1, self.classification_rules.pop(index))
            self.update_rules_tree()
    def select_file(self, edit_widget):
        path, _ = QFileDialog.getOpenFileName(self, loc.translate("locSelectFile"))
        if path:
            edit_widget.setText(path)

    def select_directory(self, edit_widget):
        path = QFileDialog.getExistingDirectory(self, loc.translate("locSelectDir"))
        if path:
            edit_widget.setText(path)

    def save_file(self, edit_widget):
        path, _ = QFileDialog.getSaveFileName(self, loc.translate("locSaveFile"))
        if path:
            edit_widget.setText(path)

    def categorize_line(self, line):
        line = line.rstrip('\n')
        for rule in self.classification_rules:
            t = rule['type']
            p = rule.get('param', '')
            if t == 'start_with' and line.startswith(p):
                return rule['name']
            elif t == 'regex' and re.search(p, line):
                return rule['name']
            elif t == 'contains_space' and ' ' in line:
                return rule['name']
            elif t == 'default':
                return rule['name']
        return None

    def do_convert(self):
        try:
            input_txt = self.convert_input_edit.text()
            output_dir = self.convert_output_edit.text()
            
            if not os.path.exists(input_txt):
                raise ValueError("Input file not exists: "+input_txt)
            
            os.makedirs(output_dir, exist_ok=True)
            
            with open(input_txt, 'r', encoding='utf-8') as f:
                lines = [line.rstrip('\n') for line in f]
            
            categories = {rule['name']: {} for rule in self.classification_rules}
            
            for line_num, line in enumerate(lines):
                category = self.categorize_line(line)
                if not category:
                    raise ValueError(f"Can't categorize line {line_num}: {line}")
                categories[category][str(line_num)] = line
            
            for name, data in categories.items():
                output_path = os.path.join(output_dir, f"{name}.json")
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            QMessageBox.information(self, loc.translate("locFinished"), loc.translate("locConvertFinished"))
        except Exception as e:
            QMessageBox.critical(self, loc.translate("locError"), str(e))

    def do_merge(self):
        try:
            input_dir = self.merge_input_edit.text()
            output_txt = self.merge_output_edit.text()
            
            category_data = []
            for rule in self.classification_rules:
                path = os.path.join(input_dir, f"{rule['name']}.json")
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        category_data.append(json.load(f))
            
            all_keys = []
            for data in category_data:
                all_keys.extend(data.keys())
            max_line = max(map(int, all_keys)) if all_keys else -1
            
            merged = []
            for i in range(max_line + 1):
                key = str(i)
                for data in category_data:
                    if key in data:
                        merged.append(data[key])
                        break
                else:
                    merged.append('')
            
            with open(output_txt, 'w', encoding='utf-8') as f:
                f.write('\n'.join(merged))
            
            QMessageBox.information(self, loc.translate("locFinished"), loc.translate("locMergeFinished"))
        except Exception as e:
            QMessageBox.critical(self, loc.translate("locError"), str(e))

    def do_upgrade(self):
        try:
            old_txt = self.upgrade_old_txt_edit.text()
            old_json_dir = self.upgrade_old_json_edit.text()
            new_txt = self.upgrade_new_txt_edit.text()
            output_dir = self.upgrade_output_edit.text()
            
            # 读取旧数据
            with open(old_txt, 'r', encoding='utf-8') as f:
                old_lines = [line.rstrip('\n') for line in f]
            
            old_data = {}
            for rule in self.classification_rules:
                path = os.path.join(old_json_dir, f"{rule['name']}.json")
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        old_data[rule['name']] = json.load(f)
                else:
                    old_data[rule['name']] = {}
            
            # 构建翻译映射
            content_translations = defaultdict(list)
            for idx, content in enumerate(old_lines):
                category = self.categorize_line(content)
                translation = old_data[category].get(str(idx), content)
                content_translations[content].append(translation)
            
            # 处理新文件
            with open(new_txt, 'r', encoding='utf-8') as f:
                new_lines = [line.rstrip('\n') for line in f]
            
            new_data = {rule['name']: {} for rule in self.classification_rules}
            content_count = defaultdict(int)
            
            for idx, content in enumerate(new_lines):
                category = self.categorize_line(content)
                count = content_count[content]
                content_count[content] += 1
                
                if content in content_translations and count < len(content_translations[content]):
                    translation = content_translations[content][count]
                else:
                    translation = content
                
                new_data[category][str(idx)] = translation
            
            # 保存结果
            os.makedirs(output_dir, exist_ok=True)
            for name, data in new_data.items():
                path = os.path.join(output_dir, f"{name}.json")
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            QMessageBox.information(self, loc.translate("locFinished"), loc.translate("locUpgradeFinished"))
        except Exception as e:
            QMessageBox.critical(self, loc.translate("locError"), str(e))