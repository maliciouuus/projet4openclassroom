class TaskController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_task_details(self, title, description):
        self.model.update(title, description)

    def display_task(self):
        self.view.display_task(self.model.title, self.model.description) 