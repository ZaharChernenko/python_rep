from enum import Enum, StrEnum

from PyQt5 import QtCore, QtGui, QtWidgets


class ValidExtensions(Enum):
    WORD: list[str] = [".docx", ".doc"]
    EXCEL: list[str] = [".xls", ".xlsx"]
    JSON: list[str] = [".json"]


class ExtensionValidator:
    def __init__(self, valid_extensions: ValidExtensions):
        self.valid_extensions: ValidExtensions = valid_extensions

    def __call__(self, file_path: str) -> bool:
        return any(file_path.endswith(ext) for ext in self.valid_extensions.value)


class DragAndDropFrameStyles(StrEnum):
    WORD = "#word_field {background-color: rgba(17, 146, 244, 0.7); border-radius: 10px;}"
    EXCEL = "#excel_field {background-color: rgba(115, 189, 137, 0.7); border-radius: 10px;}"
    JSON = "#json_field {background-color: rgba(228, 121, 11, 0.7); border-radius: 10px;}"


class DragAndDropFrameTitles(StrEnum):
    WORD = "word_field"
    EXCEL = "excel_field"
    JSON = "json_field"


class DragAndDropFrameLabelsText(StrEnum):
    WORD = "Word шаблон сертификата"
    EXCEL = "Excel файл"
    JSON = "Json паттерн"


class DragAndDropFrame(QtWidgets.QFrame):
    def __init__(
        self,
        *,
        widget: QtWidgets.QWidget,
        title: DragAndDropFrameTitles,
        style: DragAndDropFrameStyles,
        label_text: DragAndDropFrameLabelsText,
        extension_validator: ExtensionValidator,
        onFileDropped: "function",
    ):
        super().__init__(widget)
        self.setAcceptDrops(True)
        self.setObjectName(title)

        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setStyleSheet(style)

        self._vlayout = QtWidgets.QVBoxLayout(self)
        self._vlayout.setObjectName("vlayout")

        # создаем подпись
        self._label = QtWidgets.QLabel(self)
        self._label.setObjectName("label")
        self._label.setAlignment(QtCore.Qt.AlignCenter)
        self._label.setText(label_text)
        # добавляем на layout
        self._vlayout.addWidget(self._label)

        self._extenstion_validator = extension_validator
        self._is_file_set: bool = False
        self._onFileDropped = onFileDropped

    def __bool__(self):
        return self._is_file_set

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if self._extenstion_validator(file_path):
                    self._label.setText(file_path)
                    self._is_file_set = True
                    self._onFileDropped()
                else:
                    QtWidgets.QMessageBox.critical(self, "Ошибка", f"Неподдерживаемый формат файла: {file_path}")
            event.accept()
        else:
            event.ignore()

    def getFilePath(self) -> str:
        return self._label.text()
