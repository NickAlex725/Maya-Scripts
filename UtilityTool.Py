import maya.OpenMayaUI as Omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance


import maya.cmds as cmds


def get_maya_main_win():
    main_window = Omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)


class ToolWin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__(parent=get_maya_main_win())
        self.util_tool = ToolClass()
        self.setWindowTitle("Final Touch Ups")
        self.resize(500, 200)
        self._make_main_layout()
        self._connect_signals()

    def _make_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self._add_form_layout()
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def _add_form_layout(self):
        self.form_layout = QtWidgets.QFormLayout()
        self._add_prefix_or_suffix_layout()
        self._add_custom_grp_layout()
        self._add_btn_layout()
        self._add_playblast_layout()
        self.main_layout.addLayout(self.form_layout)

    def _add_prefix_or_suffix_layout(self):
        self.name_ledit = QtWidgets.QLineEdit("Prefix/Suffix")
        self.prefix_chkbox = QtWidgets.QRadioButton("Prefix?")
        self.suffix_chkbox = QtWidgets.QRadioButton("Suffix?")
        self.apply_name_btn = QtWidgets.QPushButton("Apply")
        self.prefix_or_suffix_layout = QtWidgets.QHBoxLayout()
        self.prefix_or_suffix_layout.addWidget(self.name_ledit)
        self.prefix_or_suffix_layout.addWidget(self.prefix_chkbox)
        self.prefix_or_suffix_layout.addWidget(self.suffix_chkbox)
        self.prefix_or_suffix_layout.addWidget(self.apply_name_btn)
        self.form_layout.addRow("Prefix or Suffix name",
                                self.prefix_or_suffix_layout)

    def _add_custom_grp_layout(self):
        self.grp_name_ledit = QtWidgets.QLineEdit("Group Name")
        self.create_group_btn = QtWidgets.QPushButton("Create Group")
        self.custom_grp_layout = QtWidgets.QHBoxLayout()
        self.custom_grp_layout.addWidget(self.grp_name_ledit)
        self.custom_grp_layout.addWidget(self.create_group_btn)
        self.form_layout.addRow("Group Name", self.custom_grp_layout)

    def _add_playblast_layout(self):
        self.cmbx_name = QtWidgets.QLabel("Framerate")
        self.framerate_cmbx = QtWidgets.QComboBox()
        self.framerate_cmbx.addItem("Game: 15FPS")
        self.framerate_cmbx.addItem("Film: 24FPS")
        self.spbx_name = QtWidgets.QLabel("Playblast Length")
        self.playblast_length_spbx = QtWidgets.QSpinBox()
        self.wireframe_on_chbx = QtWidgets.QCheckBox("Show Wireframe?")
        self.playblast_btn = QtWidgets.QPushButton("Playblast")
        self.playblast_layout = QtWidgets.QHBoxLayout()
        self._add_playblast_widgets()
        self.form_layout.addRow("Playblast", self.playblast_layout)

    def _add_playblast_widgets(self):
        self.playblast_layout.addWidget(self.cmbx_name)
        self.playblast_layout.addWidget(self.framerate_cmbx)
        self.playblast_layout.addWidget(self.spbx_name)
        self.playblast_layout.addWidget(self.playblast_length_spbx)
        self.playblast_layout.addWidget(self.wireframe_on_chbx)
        self.playblast_layout.addWidget(self.playblast_btn)

    def _add_btn_layout(self):
        self.freeze_btn = QtWidgets.QPushButton("Freeze Transformations")
        self.delete_history_btn = QtWidgets.QPushButton("Delete History")
        self.auto_uv_btn = QtWidgets.QPushButton("Auto UV")
        self.btn_layout = QtWidgets.QHBoxLayout()
        self.btn_layout.addWidget(self.freeze_btn)
        self.btn_layout.addWidget(self.delete_history_btn)
        self.btn_layout.addWidget(self.auto_uv_btn)
        self.form_layout.addRow(self.btn_layout)

    def _connect_signals(self):
        self.apply_name_btn.clicked.connect(self._apply)
        self.create_group_btn.clicked.connect(self._create_grp)
        self.delete_history_btn.clicked.connect(self._delete_history)
        self.freeze_btn.clicked.connect(self._freeze_transformations)
        self.auto_uv_btn.clicked.connect(self._auto_uv)
        self.playblast_btn.clicked.connect(self._prep_playblast)

    @QtCore.Slot()
    def _cancel(self):
        self.close()

    @QtCore.Slot()
    def _apply(self):
        self._set_tool_properties()
        self.util_tool.rename_objs()

    @QtCore.Slot()
    def _create_grp(self):
        self._set_tool_properties()
        self.util_tool.create_grp()

    @QtCore.Slot()
    def _prep_playblast(self):
        self._set_tool_properties()
        self.util_tool.prep_playblast()

    @QtCore.Slot()
    def _auto_uv(self):
        self._set_tool_properties()
        self.util_tool.auto_uv()

    @QtCore.Slot()
    def _delete_history(self):
        self._set_tool_properties()
        self.util_tool.delete_history()

    @QtCore.Slot()
    def _freeze_transformations(self):
        self._set_tool_properties()
        self.util_tool.freeze_transformations()

    def _set_tool_properties(self):
        self.util_tool.__init__()
        self.util_tool.suffix_enabled = self.suffix_chkbox.isChecked()
        self.util_tool.prefix_enabled = self.prefix_chkbox.isChecked()
        self.util_tool.chars_to_add = self.name_ledit.text()
        self.util_tool.grp_name = self.grp_name_ledit.text()
        self.util_tool.wireframe = self.wireframe_on_chbx.isChecked()
        self.util_tool.playblast_length = self.playblast_length_spbx.value()
        if (self.framerate_cmbx == "Game: 15FPS"):
            self.util_tool.timeline_fps = "game"
        elif (self.framerate_cmbx == "Film: 24FPS"):
            self.util_tool.timeline_fps = "film"


class ToolClass():
    def __init__(self):
        self.prefix_enabled = False
        self.suffix_enabled = False
        self.chars_to_add = ""
        self.grp_name = ""
        self.wireframe = True
        self.playblast_length = 6
        self.timeline_fps = "film"

    def rename_objs(self):
        self.selected_objs = cmds.ls(sl=True)
        self.counter = 0
        for objs in self.selected_objs:
            if (self.suffix_enabled):
                self.new_name = (self.selected_objs[self.counter]
                                 + self.chars_to_add)
                cmds.rename(objs, self.new_name)
            if (self.prefix_enabled):
                self.new_name = (self.chars_to_add
                                 + self.selected_objs[self.counter])
                cmds.rename(objs, self.new_name)
            self.counter += 1

    def create_grp(self):
        self.selected_objs = cmds.ls(sl=True)
        self.grp = cmds.group(name=self.grp_name)
        for objs in self.selected_objs:
            cmds.parent(objs, self.grp, add=True)

    def prep_playblast(self):
        self.currState = cmds.grid(toggle=True, q=True)
        cmds.grid(toggle=(self.currState == 0))
        cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", True)
        self.viewport = cmds.getPanel(wf=True)
        if (self.wireframe):
            cmds.modelEditor(self.viewport, edit=True, wireframeOnShaded=True)
        else:
            cmds.modelEditor(self.viewport, edit=True, wireframeOnShaded=False)
        self.set_keyframes()
        cmds.currentUnit(self.timeline_fps)
        cmds.playblast(o=True)

    def set_keyframes(self):
        if (self.timeline_fps == "film"):
            self.max_time = 24 * self.playblast_length
        elif (self.timeline_fps == "game"):
            self.max_time = 15 * self.playblast_length
        cmds.playbackOptions(min=0, max=self.max_time)
        cmds.setKeyframe(t=0)
        cmds.setKeyframe(t=self.max_time, v=359, at="rotateY")

    def auto_uv(self):
        self.selected_objs = cmds.ls(sl=True)
        for objs in self.selected_objs:
            cmds.polyAutoProjection(objs)

    def freeze_transformations(self):
        self.selected_objs = cmds.ls(sl=True)
        for objs in self.selected_objs:
            cmds.makeIdentity(objs, apply=True)

    def delete_history(self):
        self.selected_objs = cmds.ls(sl=True)
        for objs in self.selected_objs:
            cmds.delete(objs, ch=True)


def main():
    pass


if __name__ == "__main__":
    main()
