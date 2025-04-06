
# Requête SQL pour créer la table "tasks" si elle n'existe pas
CREATE_TASKS_TABLE = (
    "CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, description TEXT NOT NULL, username TEXT NOT NULL);"
)

# Requête SQL pour créer la table "added_fortunes" si elle n'existe pas

CREATE_ADDED_FORTUNE_TABLE = (
    "CREATE TABLE IF NOT EXISTS added_fortunes (fortune_id INTEGER NOT NULL);"
)

# Requête SQL pour récupérer toutes les tâches de la table "tasks"
GET_ALL_TASKS = (
    "SELECT * FROM tasks;"
)

# Fonction pour construire la requête de suppression d'une tâche
def delete_task_query(id: int):

    return "DELETE FROM tasks WHERE id = %s;"