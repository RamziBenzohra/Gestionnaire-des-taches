
import requests
from PyQt5 import QtCore, QtGui, QtWidgets


"""
       ici c'est le même code que "gestionnaire des taches" qui est utilisé donc pas besoin de commenter.
       """


class Ui_SecondWindow(object):  
    username= ""
    def setupUi(self, SecondWindow):
        SecondWindow.setObjectName("SecondWindow")
        SecondWindow.resize(1024, 768)  # Same size as main window
        SecondWindow.setMinimumSize(QtCore.QSize(1024, 768))
        SecondWindow.setMaximumSize(QtCore.QSize(1024, 768))
        # ... (No need to set window icon here unless it's different)

        SecondWindow.setWindowIcon(QtGui.QIcon("icon"))
        SecondWindow.setWindowTitle("Taches d'un utilisateur")

        SecondWindow.setAutoFillBackground(True)
        palette = SecondWindow.palette()
        palette.setColor(SecondWindow.backgroundRole(), QtGui.QColor("#00aa7f"))
        SecondWindow.setPalette(palette)

        self.centralwidget = QtWidgets.QWidget(SecondWindow)
        self.centralwidget.setObjectName("centralwidget")

        app_font = QtGui.QFont("Arial", 10)
        self.centralwidget.setFont(app_font)

        layout = QtWidgets.QVBoxLayout(self.centralwidget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        input_layout = QtWidgets.QHBoxLayout()

        self.tasks_line_input_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.tasks_line_input_2.setObjectName("lineEdit")
        self.tasks_line_input_2.setMinimumHeight(40)
        input_layout.addWidget(self.tasks_line_input_2)

        self.add_tasks_btn_2 = QtWidgets.QPushButton(self.centralwidget)
        self.add_tasks_btn_2.setObjectName("pushButton_2")
        self.add_tasks_btn_2.setText("Ajouter une tâche")
        self.add_tasks_btn_2.setMinimumHeight(40)
        input_layout.addWidget(self.add_tasks_btn_2)

        layout.addLayout(input_layout)



        button_layout = QtWidgets.QHBoxLayout()

        self.delete_tasks_btn_2 = QtWidgets.QPushButton(self.centralwidget)
        self.delete_tasks_btn_2.setObjectName("pushButton_3")
        self.delete_tasks_btn_2.setText("Supprimer une tâche")
        self.delete_tasks_btn_2.setMinimumHeight(40)
        button_layout.addWidget(self.delete_tasks_btn_2)

        layout.addLayout(button_layout)
        # --- End of button removal ---

        self.tasks_list_2 = QtWidgets.QListWidget(self.centralwidget)
        self.tasks_list_2.setObjectName("listWidget")
        self.tasks_list_2.setFont(app_font)
        layout.addWidget(self.tasks_list_2)

        self.errors_txt_2 = QtWidgets.QLabel(self.centralwidget)
        self.errors_txt_2.setObjectName("label")
        self.errors_txt_2.setText("An error has accuered, please come back tomorow")
        self.errors_txt_2.setStyleSheet("color: red; font-weight: bold; font-size: 16px;")
        layout.addWidget(self.errors_txt_2)

        # --- Refresh Button Layout ---
        refresh_layout = QtWidgets.QHBoxLayout()
        self.refresh_button = QtWidgets.QPushButton(self.centralwidget)
        self.refresh_button.setObjectName("refresh_button")
        self.refresh_button.setText("Refresh")
        self.refresh_button.setMinimumHeight(40)
        refresh_layout.addStretch(1)  # Stretch first to push to the right
        refresh_layout.addWidget(self.refresh_button)
        layout.addLayout(refresh_layout)
        # --- End of Refresh Button ---

        SecondWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SecondWindow)
        self.statusbar.setObjectName("statusbar")
        SecondWindow.setStatusBar(self.statusbar)

        for button in self.centralwidget.findChildren(QtWidgets.QPushButton):
            button_font = button.font()
            button_font.setPointSize(9)
            button.setFont(button_font)

        self.add_tasks_btn_2.clicked.connect(self.add_task_2)
        self.delete_tasks_btn_2.clicked.connect(self.delete_task_2)
        self.refresh_button.clicked.connect(self.load_data)


        QtCore.QMetaObject.connectSlotsByName(SecondWindow)



    def add_task_2(self):
        #même chose, j'ai réutilisé cette fonction donc pas besoin de la commenter ici aussi
        task_text = self.tasks_line_input_2.text()
        if task_text.strip():
            try:
                self.errors_txt_2.setText("")
                self.errors_txt_2.setText("Adding new task ........")
                new_task = {'description': task_text,
                            'username': self.username}
                response = requests.post('http://localhost:5000/v1/new_task', json=new_task)
                response.raise_for_status()

                if response.status_code == 201:
                    self.tasks_line_input_2.setText("")
                    self.errors_txt_2.setText("New task added ........")
                    self.load_data()


            except requests.exceptions.RequestException as e:
                self.errors_txt_2.setText("error adding task ........")
                print(f"Error adding task: {e}")
        else:
            self.errors_txt_2.setText("Can't add empty task ........")
            print("empty task")

    def delete_task_2(self):
        try:
            ##même chose, j'ai réutilisé cette fonction donc pas besoin de la commenter ici aussi
            self.errors_txt_2.setText("Deleting ........")
            current_list_item = self.tasks_list_2.currentItem().text()
            user, description = current_list_item.split(" | ", 1)
            task_id = self.user_tasks.get(description)

            delete_task = {'ID': task_id}
            response = requests.delete('http://localhost:5000/v1/delete_task', json=delete_task)
            response.raise_for_status()
            # Update the UI (optional):
            if response.status_code == 200:  # Task deleted successfully
                self.errors_txt_2.setText("Task deleted ........")
                self.load_data()  # Or remove the specific item from the list

        except requests.exceptions.RequestException as e:
            self.errors_txt_2.setText("Error deleting task ........")
            print(f"Error deleting task: {e}")


    def load_data(self):
        try:
            ##même chose, j'ai réutilisé cette fonction donc pas besoin de la commenter ici aussi
            response = requests.get(f'http://localhost:5000/v1/user?username={self.username}')
            response.raise_for_status()
            if response.status_code == 200:
                user_tasks = response.json()
                self.tasks_list_2.clear()
                self.user_tasks = {}
                for task in user_tasks:
                    task_id = task['id']
                    description = task['description']
                    user = task['username']
                    self.tasks_list_2.addItem(f"{user} | {description}")
                    self.user_tasks[description] = task_id
        except requests.exceptions.RequestException as e:
            self.label.setText("Error loading tasks ........")
            print(f"Error fetching tasks, comme back tomorrow || {e}")


