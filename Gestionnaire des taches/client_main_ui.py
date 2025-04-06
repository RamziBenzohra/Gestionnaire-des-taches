from PyQt5 import QtCore, QtGui, QtWidgets


from client_second_ui import ClientSecondUi




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(QtCore.QSize(500, 200))
        MainWindow.setMaximumSize(QtCore.QSize(500, 200))
        MainWindow.setWindowIcon(QtGui.QIcon("icon"))
        MainWindow.setWindowTitle("Gestionnaire de tâches")
        MainWindow.setAutoFillBackground(True)
        palette = MainWindow.palette()
        palette.setColor(MainWindow.backgroundRole(), QtGui.QColor("#00aa7f"))
        MainWindow.setPalette(palette)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        app_font = QtGui.QFont("Arial", 10)
        self.centralwidget.setFont(app_font)

        layout = QtWidgets.QVBoxLayout(self.centralwidget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)


        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setText("Entrez votre nom d'utilisateur:")

        layout.addWidget(self.label)

        self.username_input = QtWidgets.QLineEdit(self.centralwidget)
        self.username_input.setObjectName("lineEdit")
        self.username_input.setMinimumHeight(40)
        layout.addWidget(self.username_input)

        self.next_btn = QtWidgets.QPushButton(self.centralwidget)
        self.next_btn.setObjectName("pushButton")
        self.next_btn.setText("Continuer")
        self.next_btn.setMinimumHeight(40)
        layout.addWidget(self.next_btn)

        MainWindow.setCentralWidget(self.centralwidget)

        # Connect button click to open_second_screen
        self.next_btn.clicked.connect(self.open_second_screen)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def open_second_screen(self):
        """
        Ouvre une deuxième fenêtre si un nom d'utilisateur est saisi.
        """
        username = self.username_input.text()  # Récupère le nom d'utilisateur saisi dans le champ de texte
        try:
            if username:  # Vérifie si un nom d'utilisateur a été saisi
                self.second_window = QtWidgets.QMainWindow()
                self.ui = ClientSecondUi()
                self.ui.setupUi(self.second_window)
                self.ui.username = username  # Transmet le nom d'utilisateur à la deuxième fenêtre
                self.ui.load_data()  # Charge les données spécifiques à l'utilisateur dans la deuxième fenêtre
                self.second_window.show()  # Affiche la deuxième fenêtre
                MainWindow.hide()  # Cache la fenêtre principale (MainWindow)
        except Exception as e:
            print(f"Error : {e.__context__}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())