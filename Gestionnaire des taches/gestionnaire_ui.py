import random
import threading
import time

from gestionnaire_second_ui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import requests


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 768))
        MainWindow.setMaximumSize(QtCore.QSize(1024, 768))
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

        input_layout = QtWidgets.QHBoxLayout()

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setMinimumHeight(40)
        input_layout.addWidget(self.lineEdit)

        self.add_task_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_task_btn.setObjectName("pushButton_2")
        self.add_task_btn.setText("Ajouter une tâche")
        self.add_task_btn.setMinimumHeight(40)
        input_layout.addWidget(self.add_task_btn)

        layout.addLayout(input_layout)

        button_layout = QtWidgets.QHBoxLayout()

        self.generate_tasks_btn = QtWidgets.QPushButton(self.centralwidget)
        self.generate_tasks_btn.setObjectName("pushButton_4")
        self.generate_tasks_btn.setText("Générer des tâches aléatoires")
        self.generate_tasks_btn.setMinimumHeight(40)
        button_layout.addWidget(self.generate_tasks_btn)

        self.show_tasks_btn = QtWidgets.QPushButton(self.centralwidget)
        self.show_tasks_btn.setObjectName("pushButton_5")
        self.show_tasks_btn.setText("Afficher les tâches de l'utilisateur")
        self.show_tasks_btn.setMinimumHeight(40)
        button_layout.addWidget(self.show_tasks_btn)

        self.delete_task_btn = QtWidgets.QPushButton(self.centralwidget)
        self.delete_task_btn.setObjectName("pushButton_3")
        self.delete_task_btn.setText("Supprimer une tâche")
        self.delete_task_btn.setMinimumHeight(40)
        button_layout.addWidget(self.delete_task_btn)

        layout.addLayout(button_layout)

        self.tasks_list = QtWidgets.QListWidget(self.centralwidget)
        self.tasks_list.setObjectName("listWidget")
        self.tasks_list.setFont(app_font)
        layout.addWidget(self.tasks_list)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setText("An error has accuered, please come back tomorow")
        self.label.setStyleSheet("color: red; font-weight: bold; font-size: 16px;")
        layout.addWidget(self.label)

       
        refresh_layout = QtWidgets.QHBoxLayout()
        self.refresh_button = QtWidgets.QPushButton(self.centralwidget)
        self.refresh_button.setObjectName("refresh_button")
        self.refresh_button.setText("Refresh")
        self.refresh_button.setMinimumHeight(40)
        refresh_layout.addStretch(1)  # Stretch first to push to the right
        refresh_layout.addWidget(self.refresh_button)
        layout.addLayout(refresh_layout)
        

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        for button in self.centralwidget.findChildren(QtWidgets.QPushButton):
            button_font = button.font()
            button_font.setPointSize(9)
            button.setFont(button_font)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.add_task_btn.clicked.connect(self.add_task)
        self.delete_task_btn.clicked.connect(self.delete_task)
        self.generate_tasks_btn.clicked.connect(self.generate_random_tasks)
        self.show_tasks_btn.clicked.connect(self.open_second_screen)
        self.refresh_button.clicked.connect(self.refresh)
        self.load_tasks()

    def generate_random_tasks(self):
        try:
            ##ici, nous envoyons une requête  pour effacer toutes les fortunes que nous avons ajoutées précédemment
            response = requests.delete('http://localhost:5000/v1/delete_fortune')
            response.raise_for_status()
            if response.status_code == 200:
                ##nous sommes maintenant prêts à démarrer un nouveau thread pour ajouter des fortunes séparément du thread principal
                print("Fortunes are deleted....ready to add new ones")
                print("starting new seprate thread to add fortune")
                self.running = True ##nous utilisons cette variable pour arrêter d'ajouter des fortunes
                self.fortune_thread = threading.Thread(target=self.addFortureToDatabase)
                self.fortune_thread.daemon = True
                self.fortune_thread.start()##ici nous commençons le thread
        except requests.exceptions.RequestException as e:
            print(f"Error deleting fortunes: {e}")
            return False
    def addFortureToDatabase(self):
        try:
            while self.running:##tandis que "self.is running" est vrai, nous ajoutons donc des fortunes
                new_fortune = {'description': self.get_fortune(),
                        'username': "Gestionnaire"}
                ##   "self.get_fortune()"donne une nouvelle fortune au hasard à partir de la base de données de fortune,
                # donc à chaque fois, nous en obtenons une nouvelle

                ##ici nous envoyons la requête http pour ajouter de nouvelles fortunes au serveur,
                # lorsque la réponse est réussie nous chargeons à nouveau la liste depuis le serveur
                response = requests.post('http://localhost:5000/v1/new_fortune', json=new_fortune)
                response.raise_for_status()
                if response.status_code == 201:
                    self.label.setText("New Fortune added, please refresh ........")
                    print("fortune added click refresh")
                    self.load_tasks()
                time.sleep(5)##nous arrêtons le fil maintenant pendant 5 secondes, donc toutes
                # les 5 secondes il ajoute une nouvelle fortune
        except requests.exceptions.RequestException as e:
            self.label.setText("error adding fortune ........")
            print(f"Error adding fortune: {e}")

    def get_fortune(self, fortune_db="fortunes_.txt"):
        ###le fichier qui contient toutes les fortunes est "fortunes_.txt",
        # donc, cette fonction lit le fichier puis renvoie une ligne aléatoire du fichier
        with open(fortune_db, "r") as f:
            fortunes = f.readlines()
        return random.choice(fortunes).strip()

    def stop_adding_fortunes(self):
          # nous terminons le thread fortune en définissant la variable "isrunning" -> false,
          # donc la boucle while s'arrête et nous terminons ensuite le thread en utilisant "self.fortune_thread.join()"
        if self.running & self.fortune_thread.is_alive():
            self.running = False
            self.fortune_thread.join()
            print("fortune stoped")# Wait for the thread to finish

    def refresh(self):
        ##lorsque l'utilisateur clique sur le bouton d'actualisation,
        # nous arrêtons d'ajouter des fortunes et nous chargeons à nouveau la liste
        self.stop_adding_fortunes()
        self.load_tasks()
    def load_tasks(self):
        """
        Charge les tâches depuis l'API et les affiche dans la liste des tâches .
        """
        try:
            self.label.setText("")  # Efface le texte du label
            self.label.setText("Chargement des tâches ........") # Affiche un message de chargement dans le label

            response = requests.get('http://localhost:5000/v1/tasks')
            # Effectue une requête GET à l'API Flask pour récupérer les tâches
            response.raise_for_status()
            # Lève une exception si le code de statut de la réponse est une erreur (4xx ou 5xx)


            self.label.setText("Tâches chargées ........")  # Affiche un message de succès dans le label

            tasks = response.json()  # Convertit la réponse JSON en un dictionnaire Python
            self.tasks_list.clear()  # Efface la liste des tâches dans l'interface utilisateur
            self.task_data = {}  # Initialise un dictionnaire pour stocker les tâches et leurs IDs

            # Parcourt chaque tâche récupérée de l'API
            for task in tasks:
                task_id = task['id']  # Extrait l'ID de la tâche
                description = task['description'] # Extrait la description de la tâche
                user = task['username'] # Extrait le nom d'utilisateur associé à la tâche

                # Ajoute la tâche à la liste dans l'interface utilisateur
                self.tasks_list.addItem(f"{user} | {description}")

                # Stocke l'ID de la tâche dans le dictionnaire `task_data`,
                # en utilisant la description comme clé
                self.task_data[description] = task_id

        # Gestion des erreurs de requête (problèmes de connexion, etc.)
        except requests.exceptions.RequestException as e:
            self.label.setText("Erreur lors du chargement des tâches ........") # Affiche un message d'erreur
            print(f"Error fetching tasks, comme back tomorrow || {e}")  # Affiche l'erreur dans la console

    def open_second_screen(self):
        """
        Ouvre une deuxième fenêtre et charge les données de la tâche sélectionnée dans cette fenêtre.
        """
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self.window)  # Initialise l'interface utilisateur de la deuxième fenêtre

        current_task_item = self.tasks_list.currentItem().text()
        # Récupère le texte de l'élément actuellement sélectionné dans la liste des tâches (self.tasks_list)

        user, description = current_task_item.split(" | ", 1)
        # Divise le texte de la tâche en deux parties (nom d'utilisateur et description) en utilisant " | " comme séparateur

        self.ui.username = user  # Affecte le nom d'utilisateur à un attribut de la deuxième fenêtre
        self.window.show()  # Affiche la deuxième fenêtre à l'utilisateur

        self.ui.load_data()  # Appelle la méthode load_data() de la deuxième fenêtre pour charger les données spécifiques à la tâche

    def add_task(self):
        """
        Ajoute une nouvelle tâche à la base de données.
        """
        item = self.lineEdit.text()  # Récupère le texte saisi
        if item.strip():  # Vérifie si le texte n'est pas vide après suppression des espaces
            try:

                self.label.setText("Ajout d'une nouvelle tâche ........")  # Affiche un message de chargement

                new_task = {'description': item, 'username': "Gestionnaire"}
                # Crée un dictionnaire avec la description et le nom d'utilisateur de la nouvelle tâche

                response = requests.post('http://localhost:5000/v1/new_task', json=new_task)
                # Envoie une requête POST à l'API Flask pour ajouter la nouvelle tâche


                response.raise_for_status()
                # Lève une exception si le code de statut de la réponse est une erreur (4xx ou 5xx)

                # Si la tâche a été ajoutée avec succès (code de statut 201 Created)
                if response.status_code == 201:
                    self.label.setText("Nouvelle tâche ajoutée ........")  # Affiche un message de succès
                    self.load_tasks()  # Recharge la liste des tâches depuis l'API


            # Gestion des erreurs de requête (problèmes de connexion, etc.)
            except requests.exceptions.RequestException as e:
                self.label.setText("Erreur lors de l'ajout de la tâche ........")  # Affiche un message d'erreur
                print(f"Error adding task: {e}")  # Affiche l'erreur dans la console

        # Cas où le texte saisi est vide
        else:
            self.label.setText("Impossible d'ajouter une tâche vide ........")  # Affiche un message d'erreur
            print("empty task")  # Affiche un message dans la console

    def delete_task(self):
        """
        Supprime la tâche sélectionnée de la base de données.
        """
        try:
            self.label.setText("Suppression en cours ........")  # Affiche un message de chargement dans le label

            current_list_item = self.tasks_list.currentItem().text()
            # Récupère le texte de l'élément actuellement sélectionné dans la liste des tâches

            user, description = current_list_item.split(" | ", 1)
            # Divise le texte de la tâche en deux parties (nom d'utilisateur et description)

            task_id = self.task_data.get(description)
            # Récupère l'ID de la tâche à partir du dictionnaire `task_data`, en utilisant la description comme clé

            delete_task = {'ID': task_id}  # Crée un dictionnaire avec l'ID de la tâche à supprimer
            print(task_id)  # Affiche l'ID de la tâche dans la console (pour le débogage)

            response = requests.delete('http://localhost:5000/v1/delete_task', json=delete_task)
            # Envoie une requête DELETE à l'API Flask pour supprimer la tâche


            response.raise_for_status()
            # Lève une exception si le code de statut de la réponse est une erreur (4xx ou 5xx)

            # Si la tâche a été supprimée avec succès (code de statut 200 OK)
            if response.status_code == 200:
                self.label.setText("Tâche supprimée ........")  # Affiche un message de succès
                self.load_tasks()  # Recharge la liste des tâches depuis l'API

        # Gestion des erreurs de requête (problèmes de connexion, etc.)
        except requests.exceptions.RequestException as e:
            self.label.setText("Erreur lors de la suppression de la tâche ........")  # Affiche un message d'erreur
            print(f"Error deleting task: {e}")  # Affiche l'erreur dans la console



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
