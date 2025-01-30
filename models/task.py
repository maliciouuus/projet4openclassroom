class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def update(self, title, description):
        self.title = title
        self.description = description 