import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify

from postgres_queries import *



load_dotenv()
app = Flask(__name__)




reading_db_connection = psycopg2.connect(host="localhost",
                                         database="postgres", user="postgres", password="postgresSuperUserPsw",
                                         port="5433")

writing_db_connection = psycopg2.connect(host="localhost",
                                         database="postgres", user="postgres", password="postgresSuperUserPsw",
                                         port="5432")



@app.post("/v1/new_task")
def create_task():
    """
    Route pour créer une nouvelle tâche dans la base de données PostgreSQL.
    """
    try:
        data = request.get_json()  # Récupère les données JSON de la requête POST
        description = data.get('description')  # Extrait la description de la tâche
        username = data.get('username')  # Extrait le nom d'utilisateur

        # Validation des données : vérification si la description et le nom d'utilisateur sont présents
        if not description:
            return jsonify({'error': 'La description est requise'}), 400  # Retourne une erreur 400 Bad Request
        if not username:
            return jsonify({'error': 'Le nom d\'utilisateur est requis'}), 400

        # Connexion à la base de données PostgreSQL (en mode écriture)
        with writing_db_connection:
            with writing_db_connection.cursor() as db_cur:


                # Prépare la requête d'insertion avec des paramètres pour éviter les injections SQL
                query = "INSERT INTO tasks (description, username) VALUES (%s, %s);"
                values = (description, username)  # Tuple contenant les valeurs à insérer

                db_cur.execute(query, values)  # Exécute la requête d'insertion avec les valeurs fournies

        return jsonify({'message': 'Tâche créée avec succès'}), 201  # Retourne un message de succès (code 201 Created)

    except Exception as e:
        print(f"On peut pas ajouter la tache, reviens demain || error : {e}")  # Affiche l'erreur dans la console
        return jsonify({'error': 'Échec de la création de la tâche'}), 500  # Retourne une erreur 500 Internal Server Error


@app.post("/v1/new_fortune")
def create_fortune():
    """
    Route pour créer une nouvelle "fortune" dans la base de données PostgreSQL et enregistrer son ID.
    """
    try:
        data = request.get_json()  # Récupère les données JSON de la requête POST
        description = data.get('description')  # Extrait la description (le texte de la fortune)
        username = data.get('username')  # Extrait le nom d'utilisateur

        # Validation des données : vérification si la description et le nom d'utilisateur sont présents
        if not description:
            return jsonify({'error': 'La description est requise'}), 400  # Retourne une erreur 400 Bad Request
        if not username:
            return jsonify({'error': 'Le nom d\'utilisateur est requis'}), 400

            # Connexion à la base de données PostgreSQL (en mode écriture)
        with writing_db_connection:
            with writing_db_connection.cursor() as db_cur:
                # Requête d'insertion dans la table "tasks" avec récupération de l'ID
                query = "INSERT INTO tasks (description, username) VALUES (%s, %s) RETURNING id;"
                values = (description, username)



                db_cur.execute(query, values)  # Exécute la requête d'insertion
                fortune_id = db_cur.fetchone()[0]  # Récupère l'ID de la fortune insérée

                # Insertion de l'ID dans la table "added_fortunes"
                db_cur.execute("INSERT INTO added_fortunes (fortune_id) VALUES (%s)", (fortune_id,))

            print("Added fortune to database!")  # Affiche un message de confirmation dans la console

        return jsonify(
            {'message': 'Fortune créée avec succès'}), 201  # Retourne un message de succès (code 201 Created)

    except Exception as e:
        print(f"On peut pas ajouter la tache, reviens demain || error : {e}")  # Affiche l'erreur dans la console
        return jsonify(
            {'error': 'Échec de la création de la fortune'}), 500  # Retourne une erreur 500 Internal Server Error
@app.delete("/v1/delete_task")
def delete_task():
    """
    Route pour supprimer une tâche de la base de données PostgreSQL.
    """
    try:
        data = request.get_json()  # Récupère les données JSON de la requête DELETE
        task_id = data.get('ID')  # Extrait l'ID de la tâche à supprimer

        # Validation : Vérification si l'ID de la tâche est présent dans la requête
        if not task_id:
            return jsonify({'error': 'L\'ID de la tâche est requis'}), 400  # Retourne une erreur 400 Bad Request

        # Connexion à la base de données PostgreSQL (en mode écriture)
        with writing_db_connection:
            with writing_db_connection.cursor() as db_cur:

                db_cur.execute(delete_task_query(task_id), (task_id,))  # Exécute la requête de suppression


        return jsonify({'message': 'Tâche supprimée avec succès'}), 200  # Retourne un message de succès (code 200 OK)

    except Exception as e:
        print(f"On peut pas supprimer la tache, reviens demain {e}")  # Affiche l'erreur dans la console
        return jsonify({'error': 'Échec de la suppression de la tâche'}), 500  # Retourne une erreur 500 Internal Server Error
@app.delete("/v1/delete_fortune")
def delete_All_fortune():
    """
    Route pour supprimer toutes les fortunes ajoutées de la base de données PostgreSQL.
    """
    try:
        # Connexion à la base de données PostgreSQL (en mode écriture)
        with writing_db_connection:
            with writing_db_connection.cursor() as db_cur:
                # Suppression des fortunes de la table "tasks"
                db_cur.execute("""
                                    DELETE FROM tasks
                                    WHERE id IN (SELECT fortune_id FROM added_fortunes);
                                """)

                # Effacement de la table "added_fortunes"
                db_cur.execute("DELETE FROM added_fortunes;")
                writing_db_connection.commit()  # Validation des modifications dans la base de données
                print("deleted all fortune ")  # Affiche un message de confirmation dans la console

        return jsonify({'message': 'Fortunes supprimées avec succès'}), 200  # Retourne un message de succès (code 200 OK)

    except Exception as e:
        print(f"On peut pas supprimer la tache, reviens demain {e}")  # Affiche l'erreur dans la console
        return jsonify({'error': 'Échec de la suppression des fortunes'}), 500  # Retourne une erreur 500 Internal Server Error
@app.get('/v1/tasks')
def get_tasks():
    """
    Route pour récupérer toutes les tâches de la base de données PostgreSQL.
    """
    try:
        # Connexion à la base de données PostgreSQL (en mode lecture)
        with reading_db_connection:
            print("Connexion à la base de données établie")  # Affiche un message de confirmation dans la console
            with reading_db_connection.cursor() as db_cur:

                db_cur.execute(GET_ALL_TASKS)  # Exécute la requête pour récupérer toutes les tâches
                tasks = db_cur.fetchall()  # Récupère toutes les tâches dans une liste de tuples

        # Conversion des tâches en une liste de dictionnaires pour une meilleure sérialisation JSON
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task[0],  # Extrait l'ID de la tâche
                'description': task[1],  # Extrait la description de la tâche
                'username': task[2],  # Extrait le nom d'utilisateur associé à la tâche
            })

        return jsonify(task_list), 200  # Retourne la liste des tâches au format JSON (code 200 OK)

    except Exception as e:
        print(f"Error fetching tasks: {e}")  # Affiche l'erreur dans la console
        return jsonify({'error': f'on peut pas afficher les taches, reviens demain || '}), 500  # Retourne une erreur 500 Internal Server Error


@app.get('/v1/user')
def get_user_tasks():
    """
    Route pour récupérer les tâches d'un utilisateur spécifique depuis la base de données PostgreSQL.
    """
    try:
        user_name = request.args.get(
            'username')  # Récupère le nom d'utilisateur depuis les paramètres de la requête GET

        # Validation : Vérification si le nom d'utilisateur est présent dans la requête
        if not user_name:
            return jsonify({'error': 'Le nom d\'utilisateur est requis'}), 400  # Retourne une erreur 400 Bad Request

        # Connexion à la base de données PostgreSQL (en mode lecture)
        with reading_db_connection:
            print("Connexion à la base de données établie")  # Affiche un message de confirmation dans la console
            with reading_db_connection.cursor() as db_cur:
                # Requête SQL paramétrée pour récupérer les tâches d'un utilisateur spécifique
                query = "SELECT * FROM tasks WHERE username = %s;"
                values = (user_name,)

                db_cur.execute(query, values)  # Exécute la requête avec le nom d'utilisateur
                tasks = db_cur.fetchall()  # Récupère toutes les tâches correspondantes

        # Conversion des tâches en une liste de dictionnaires pour une meilleure sérialisation JSON
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task[0],  # Extrait l'ID de la tâche
                'description': task[1],  # Extrait la description de la tâche
                'username': task[2],  # Extrait le nom d'utilisateur associé à la tâche
            })

        return jsonify(task_list), 200  # Retourne la liste des tâches au format JSON (code 200 OK)

    except Exception as e:
        print(f"Error fetching tasks: {e}")  # Affiche l'erreur dans la console
        return jsonify({
                           'error': f'On peut pas afficher les taches, reviens demain || '}), 500  # Retourne une erreur 500 Internal Server Error