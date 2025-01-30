from models.task import Task
from views.task_view import TaskView
from controllers.task_controller import TaskController

def main():
    # Créer les instances de Model, View et Controller
    task_model = Task("Apprendre MVC", "Comprendre le pattern MVC en Python")
    task_view = TaskView()
    task_controller = TaskController(task_model, task_view)

    # Utiliser le controller pour manipuler les données et la vue
    task_controller.update_task_details("Apprendre MVC", "Pattern MVC maîtrisé!")
    task_controller.display_task()

if __name__ == "__main__":
    main()
