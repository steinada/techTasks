import json


class DTObject:
    def __init__(self, tasks, history):
        self.tasks = tasks
        self.history = history
        self.data = json.dumps([self.tasks, self.history])
