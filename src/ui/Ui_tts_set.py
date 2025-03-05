# Form implementation generated from reading ui file 'e:\tzy\github\easytts\src\ui\tts_set.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_TTSSet(object):
    def setupUi(self, TTSSet):
        TTSSet.setObjectName("TTSSet")
        TTSSet.resize(784, 290)
        self.verticalLayout = QtWidgets.QVBoxLayout(TTSSet)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ttsProviderComboBox = QtWidgets.QComboBox(parent=TTSSet)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ttsProviderComboBox.sizePolicy().hasHeightForWidth())
        self.ttsProviderComboBox.setSizePolicy(sizePolicy)
        self.ttsProviderComboBox.setMinimumSize(QtCore.QSize(250, 0))
        self.ttsProviderComboBox.setMaximumSize(QtCore.QSize(250, 16777215))
        self.ttsProviderComboBox.setObjectName("ttsProviderComboBox")
        self.horizontalLayout.addWidget(self.ttsProviderComboBox, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.saveSetButton = QtWidgets.QPushButton(parent=TTSSet)
        self.saveSetButton.setMinimumSize(QtCore.QSize(100, 0))
        self.saveSetButton.setObjectName("saveSetButton")
        self.horizontalLayout.addWidget(self.saveSetButton)
        self.generateButton = QtWidgets.QPushButton(parent=TTSSet)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generateButton.sizePolicy().hasHeightForWidth())
        self.generateButton.setSizePolicy(sizePolicy)
        self.generateButton.setMinimumSize(QtCore.QSize(100, 0))
        self.generateButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.generateButton.setObjectName("generateButton")
        self.horizontalLayout.addWidget(self.generateButton, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.ttsProviderStackedWidget = QtWidgets.QStackedWidget(parent=TTSSet)
        self.ttsProviderStackedWidget.setObjectName("ttsProviderStackedWidget")
        self.edgeTTSPage = QtWidgets.QWidget()
        self.edgeTTSPage.setObjectName("edgeTTSPage")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.edgeTTSPage)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.edgeTTSPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(25, 0))
        self.label.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.edgeTTSLanguageSet = QtWidgets.QComboBox(parent=self.edgeTTSPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edgeTTSLanguageSet.sizePolicy().hasHeightForWidth())
        self.edgeTTSLanguageSet.setSizePolicy(sizePolicy)
        self.edgeTTSLanguageSet.setMinimumSize(QtCore.QSize(150, 0))
        self.edgeTTSLanguageSet.setMaximumSize(QtCore.QSize(200, 16777215))
        self.edgeTTSLanguageSet.setObjectName("edgeTTSLanguageSet")
        self.horizontalLayout_2.addWidget(self.edgeTTSLanguageSet, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(parent=self.edgeTTSPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(25, 0))
        self.label_2.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.edgeTTSVoiceSet = QtWidgets.QComboBox(parent=self.edgeTTSPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edgeTTSVoiceSet.sizePolicy().hasHeightForWidth())
        self.edgeTTSVoiceSet.setSizePolicy(sizePolicy)
        self.edgeTTSVoiceSet.setMinimumSize(QtCore.QSize(150, 0))
        self.edgeTTSVoiceSet.setMaximumSize(QtCore.QSize(200, 16777215))
        self.edgeTTSVoiceSet.setObjectName("edgeTTSVoiceSet")
        self.horizontalLayout_3.addWidget(self.edgeTTSVoiceSet, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.ttsProviderStackedWidget.addWidget(self.edgeTTSPage)
        self.ttsProviderPage2 = QtWidgets.QWidget()
        self.ttsProviderPage2.setObjectName("ttsProviderPage2")
        self.ttsProviderStackedWidget.addWidget(self.ttsProviderPage2)
        self.verticalLayout.addWidget(self.ttsProviderStackedWidget)

        self.retranslateUi(TTSSet)
        QtCore.QMetaObject.connectSlotsByName(TTSSet)

    def retranslateUi(self, TTSSet):
        _translate = QtCore.QCoreApplication.translate
        TTSSet.setWindowTitle(_translate("TTSSet", "Form"))
        self.saveSetButton.setText(_translate("TTSSet", "保存"))
        self.generateButton.setText(_translate("TTSSet", "生成"))
        self.label.setText(_translate("TTSSet", "语言："))
        self.label_2.setText(_translate("TTSSet", "音色："))
