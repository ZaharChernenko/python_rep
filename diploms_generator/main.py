from PyQt5 import QtCore, QtGui, QtWidgets

from model import DiplomsGeneratorModel, PatternBuilderException
from ui.image import ICON
from ui.ui_objects import (
    DragAndDropFrame,
    DragAndDropFrameLabelsText,
    DragAndDropFrameStyles,
    DragAndDropFrameTitles,
    ExtensionValidator,
    ValidExtensions,
)


class MainWindowUI(object):
    def setupUi(self, main_window: QtWidgets.QMainWindow):
        main_window.setObjectName("MainWindow")
        main_window.resize(640, 346)
        main_window.setStyleSheet(
            "#centralwidget {\n"
            "    background-color: #1f232a;\n"
            "}\n"
            "#generate_btn {\n"
            "    background-color: rgba(255, 255, 255, 0.7);\n"
            "    border-radius: 10px;\n"
            "}"
        )

        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.word_field = DragAndDropFrame(
            widget=self.centralwidget,
            title=DragAndDropFrameTitles.WORD,
            style=DragAndDropFrameStyles.WORD,
            label_text=DragAndDropFrameLabelsText.WORD,
            extension_validator=ExtensionValidator(ValidExtensions.WORD),
            onFileDropped=self.handleDropEvent,
        )
        self.verticalLayout.addWidget(self.word_field)

        self.excel_field = DragAndDropFrame(
            widget=self.centralwidget,
            title=DragAndDropFrameTitles.EXCEL,
            style=DragAndDropFrameStyles.EXCEL,
            label_text=DragAndDropFrameLabelsText.EXCEL,
            extension_validator=ExtensionValidator(ValidExtensions.EXCEL),
            onFileDropped=self.handleDropEvent,
        )
        self.verticalLayout.addWidget(self.excel_field)

        self.json_field = DragAndDropFrame(
            widget=self.centralwidget,
            title=DragAndDropFrameTitles.JSON,
            style=DragAndDropFrameStyles.JSON,
            label_text=DragAndDropFrameLabelsText.JSON,
            extension_validator=ExtensionValidator(ValidExtensions.JSON),
            onFileDropped=self.handleDropEvent,
        )
        self.verticalLayout.addWidget(self.json_field)

        self.generate_btn = QtWidgets.QPushButton(self.centralwidget)
        self.generate_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.generate_btn.setObjectName("generate_btn")
        self.generate_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.generate_btn.setText("Сгенерировать сертификаты")
        self.generate_btn.clicked.connect(self.handleClickEvent)
        self.verticalLayout.addWidget(self.generate_btn)

        main_window.setCentralWidget(self.centralwidget)
        main_window.setWindowTitle("Генератор сертификатов")
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def handleDropEvent(self):
        if self.checkAllFilesDropped():
            self.generate_btn.setEnabled(True)  # Активируем кнопку
            self.generate_btn.setStyleSheet("background-color: lightgreen;")
        else:
            self.generate_btn.setEnabled(False)  # Отключаем кнопку
            self.generate_btn.setStyleSheet("background-color: lightgray;")

    def checkAllFilesDropped(self) -> bool:
        return self.word_field and self.excel_field and self.json_field

    def handleClickEvent(self):
        try:
            diploms_generator_model: DiplomsGeneratorModel = DiplomsGeneratorModel(
                template_file_path=self.word_field.getFilePath(),
                excel_file_path=self.excel_field.getFilePath(),
                pattern_file_path=self.json_field.getFilePath(),
            )
        except PatternBuilderException as e:
            QtWidgets.QMessageBox.critical(self.centralwidget, "Ошибка", str(e))
            return
        try:
            diploms_generator_model()
        except PatternBuilderException as e:
            QtWidgets.QMessageBox.critical(self.centralwidget, "Ошибка", str(e))
            return
        QtWidgets.QMessageBox.information(self.centralwidget, "Операция завершена", "Шаблоны сгенерированы")


def setIcon(app: QtWidgets.QApplication):
    image = QtGui.QImage.fromData(QtCore.QByteArray(ICON))
    pixmap = QtGui.QPixmap.fromImage(image)
    app.setWindowIcon(QtGui.QIcon(pixmap))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    setIcon(app)

    main_window = QtWidgets.QMainWindow()
    MainWindowUI().setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())
