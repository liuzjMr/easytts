# Form implementation generated from reading ui file 'e:\tzy\github\easytts\src\ui\speaker_tts_set.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_speakerTTSSet(object):
    def setupUi(self, speakerTTSSet):
        speakerTTSSet.setObjectName("speakerTTSSet")
        speakerTTSSet.resize(361, 42)
        self.horizontalLayout = QtWidgets.QHBoxLayout(speakerTTSSet)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.speakerLabel = QtWidgets.QLabel(parent=speakerTTSSet)
        self.speakerLabel.setObjectName("speakerLabel")
        self.horizontalLayout.addWidget(self.speakerLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.speakerSetButton = QtWidgets.QPushButton(parent=speakerTTSSet)
        self.speakerSetButton.setObjectName("speakerSetButton")
        self.horizontalLayout.addWidget(self.speakerSetButton)

        self.retranslateUi(speakerTTSSet)
        QtCore.QMetaObject.connectSlotsByName(speakerTTSSet)

    def retranslateUi(self, speakerTTSSet):
        _translate = QtCore.QCoreApplication.translate
        speakerTTSSet.setWindowTitle(_translate("speakerTTSSet", "Form"))
        self.speakerLabel.setText(_translate("speakerTTSSet", "TextLabel"))
        self.speakerSetButton.setText(_translate("speakerTTSSet", "角色TTS设置"))
