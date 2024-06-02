from PyQt5 import QtCore, QtGui, QtWidgets

import setupUi


class ListFoodWindow:
    def __init__(self, list_food_window, database):
        self.products_list = database

        list_food_window.setStyleSheet("background-color: rgb(54, 54, 54);")
        self.central_widget = QtWidgets.QWidget(list_food_window)

        font = setupUi.setupRegularFont(28)
        medium_font = setupUi.setupMediumFont(30)

        self.header = setupUi.setupHeader(self.central_widget)
        self.header.setFont(medium_font)

        self.burger_btn_3 = setupUi.setupBurgerBtn(self.central_widget)

        self._input_product_name = QtWidgets.QLineEdit(self.central_widget)
        self._input_product_name.setGeometry(QtCore.QRect(20, 127, 560, 50))
        font.setPointSize(26)
        self._input_product_name.setFont(font)
        self._input_product_name.setStyleSheet("color: rgb(255, 255, 255);\n"
                                               "border: 1px solid white;\n"
                                               "border-radius: 2px")

        self.list_of_products = QtWidgets.QListWidget(self.central_widget)
        self.list_of_products.setGeometry(QtCore.QRect(20, 207, 560, 485))
        font.setPointSize(14)
        self.list_of_products.setFont(font)
        self.list_of_products.setStyleSheet("color: white;")
        self.list_of_products.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.btn_add_food = QtWidgets.QPushButton(self.central_widget)
        self.btn_add_food.setGeometry(QtCore.QRect(387, 746, 100, 100))
        self.btn_add_food.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_food.setStyleSheet("border: none;\n"
                                        "background-color: rgba(255, 255, 255, 0);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/plus-icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add_food.setIcon(icon1)
        self.btn_add_food.setIconSize(QtCore.QSize(100, 100))
        self.btn_add_food.setDisabled(True)

        self.btn_add_new_food = QtWidgets.QPushButton(self.central_widget)
        self.btn_add_new_food.setGeometry(QtCore.QRect(113, 746, 100, 100))
        self.btn_add_new_food.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_new_food.setStyleSheet("border: none;\n"
                                            "background-color: rgba(255, 255, 255, 0);")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/add_new_food_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btn_add_new_food.setIcon(icon2)
        self.btn_add_new_food.setIconSize(QtCore.QSize(100, 100))
        list_food_window.setCentralWidget(self.central_widget)

        self.retranslateUi(list_food_window)
        self.createListOfProducts()
        self.widgetsWork()
        QtCore.QMetaObject.connectSlotsByName(list_food_window)

    def retranslateUi(self, list_food_window):
        _translate = QtCore.QCoreApplication.translate
        list_food_window.setWindowTitle(_translate("MainWindow", "Добавить прием пищи"))
        self.header.setText(_translate("MainWindow", "ДОБАВИТЬ ПРОДУКТ"))
        self._input_product_name.setPlaceholderText("Введите название продукта: ")

    def createListOfProducts(self):
        for product in self.products_list:
            self.list_of_products.addItem(product["name"])

    def inputWork(self):
        is_find_from_start = False
        for i in range(len(self.products_list)):
            if len(self._input_product_name.text()) <= len(self.products_list[i]["name"]):
                if self._input_product_name.text().lower() == \
                        self.products_list[i]["name"][0:len(self._input_product_name.text())].lower():
                    self.list_of_products.scrollToItem(
                        self.list_of_products.item(i),
                        QtWidgets.QAbstractItemView.PositionAtTop)
                    is_find_from_start = True
                    break

        if not is_find_from_start:
            for j in range(len(self.products_list)):
                if self._input_product_name.text().lower() in self.products_list[j]["name"].lower():
                    self.list_of_products.scrollToItem(
                        self.list_of_products.item(j),
                        QtWidgets.QAbstractItemView.PositionAtTop)
                    break

    def defineCurrentProduct(self, item):
        for product in self.products_list:
            if item == product["name"]:
                self.current_product = product.values()
                break

    def widgetsWork(self):
        self._input_product_name.textEdited.connect(lambda: self.inputWork())

        self.list_of_products.itemClicked.connect(lambda: self.btn_add_food.setEnabled(True))
        self.list_of_products.itemClicked.connect(lambda item: self.defineCurrentProduct(item.text()))
