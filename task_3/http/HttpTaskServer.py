import json
from copy import deepcopy
from datetime import datetime
from urllib import parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from task_3.http.HttpServer import HttpServer
from task_3.model.TaskType import TaskType
from task_3.model.StatusType import StatusType
from task_3.model.Task import Task
from task_3.model.SubTask import SubTask
from task_3.model.EpicTask import EpicTask
from task_3.InMemoryHistoryManager import LinkedList


class HttpTaskServer(BaseHTTPRequestHandler):
    server = HttpServer(" http://localhost", 8080)
    manager = server.manager

    def set_header(self, response_status):
        self.send_response(response_status)
        self.send_header('content-type', 'text/html')
        self.end_headers()

    def get_body(self):
        content_length = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_length)
        return post_body

    def get_url_params(self):
        parsed_url = parse.urlparse(self.path)
        path = parsed_url.path
        query = parsed_url.query
        return path, query

    def do_GET(self):
        path, query = self.get_url_params()
        if path == '/tasks/':
            tasks = self.tasks_handler()                             # получить все задачи
            self.set_header(200)
            self.wfile.write(json.dumps(tasks).encode('utf-8'))
        else:
            if path == '/tasks/history':
                history = self.get_search_history()                   # получить историю просмотров
                self.set_header(200)
                self.wfile.write(json.dumps(history).encode('utf-8'))
            else:
                path = self.path.split('/')
                task = self.get_task_by_id(query, path)                       # получить одну задачу
                if not isinstance(task, str):
                    task_serializable = self.make_serializable(task)
                    self.wfile.write(json.dumps(vars(task_serializable)).encode('utf-8'))
                    self.send_data_to_server()

    def do_POST(self):
        # self.set_header(200)
        path, query = self.get_url_params()
        post_body = self.get_body()
        self.task_handler(path, query, post_body)            # создать или изменить задачу
        self.send_data_to_server()

    def do_DELETE(self):
        path, query = self.get_url_params()
        if self.path == '/tasks/':
            self.set_header(200)
            self.delete_all()                                # удалить все задачи
        else:
            path = self.path.split('/')
            self.delete_task(query, path)                    # удалить одну задачу
        self.send_data_to_server()

    @staticmethod
    def error_dec(func):
        def wrapper(obj, *args):
            self = obj
            result = func(obj, *args)
            if isinstance(result, str):
                self.error_handler(result)
            else:
                self.set_header(200)
            return result
        return wrapper

    def tasks_handler(self):
        tasks = self.manager.get_list_of_tasks()
        tasks_list = list()
        for task in tasks:
            task_serializable = self.make_serializable(task)
            tasks_list.append(vars(task_serializable))
        return tasks_list

    @error_dec
    def task_handler(self, path, query, post_body):
        path = path.split('/')
        body = json.loads(post_body.decode('utf-8'))
        if path[2] == 'task':
            task_type = "TASK"
        elif path[2] == 'subtask':
            task_type = "SUB_TASK"
        elif path[2] == 'epic':
            task_type = "EPIC_TASK"
        if path[1] == 'tasks':
            if 'start_time' in body and body['start_time']:
                body['start_time'] = datetime.strptime(body['start_time'], "%Y-%m-%d").date()
            if 'update' in path[-1]:
                task_id = int(query.split('=')[1])
                result = self.manager.update_any_task(**body, task_id=task_id)
                return result
            else:
                result = self.manager.create_any_task(**body, task_type=task_type)
                return result
        else:
            self.error_handler("Incorrect request")

    @error_dec
    def delete_task(self, query, path):
        task_id = int(query.split('=')[1])
        if path[1] == 'tasks':
            if path[2].split("?")[0] in ['task', 'subtask', 'epic']:
                return self.manager.delete_task_by_id(task_id)
            else:
                self.error_handler()
        else:
            self.error_handler()

    def delete_all(self):
        self.manager.delete_all_tasks()

    @error_dec
    def get_task_by_id(self, query, path):
        task_id = int(query.split('=')[1])
        if path[1] == 'tasks':
            if path[2].split("?")[0] in ['task', 'subtask', 'epic']:
                task = self.manager.get_task_by_id(task_id)
                return task
            else:
                self.error_handler()
        else:
            self.error_handler()

    def get_search_history(self):
        history = self.manager.get_history()
        history = list(map(lambda x: x.data, history))
        tasks = list()
        for task in history:
            tasks.append(vars(self.make_serializable(task)))
        return tasks

    @staticmethod
    def make_serializable(task):
        task_serializable = deepcopy(task)
        task_serializable.status = task_serializable.status.name
        task_serializable.task_type = task_serializable.task_type.name
        if task_serializable.start_time:
            task_serializable.start_time = task_serializable.start_time.isoformat()
        return task_serializable

    def error_handler(self, message=None):
        self.send_response(400)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.send_error(400, message)

    @staticmethod
    def serialize_tasks(tasks):
        serializable_tasks = list()
        for task in tasks.values():
            serializable_task = HttpTaskServer.make_serializable(task)
            serializable_tasks.append(vars(serializable_task))
        return serializable_tasks

    @staticmethod
    def serialize_history(history):
        history = list(map(lambda x: x.data, history))
        serializable_history = list()
        for task in history:
            serializable_task = HttpTaskServer.make_serializable(task)
            serializable_history.append(vars(serializable_task))
        return serializable_history

    @staticmethod
    def make_deserializable(task_vars):
        task_vars['status'] = StatusType[task_vars['status']]
        task_vars['task_type'] = TaskType[task_vars['task_type']]
        task_vars['unic_task_id'] = int(task_vars['unic_task_id'])
        if task_vars['start_time']:
            task_vars['start_time'] = datetime.strptime(task_vars['start_time'], "%Y-%m-%d").date()
        if task_vars['task_type'].name == "TASK":
            del task_vars['task_type']
            return Task(**task_vars)
        elif task_vars['task_type'].name == "SUB_TASK":
            del task_vars['task_type']
            return SubTask(**task_vars)
        elif task_vars['task_type'].name == "EPIC_TASK":
            del task_vars['task_type']
            return EpicTask(**task_vars)

    @staticmethod
    def upload_tasks(tasks):
        uploaded_tasks = dict()
        for task in tasks:
            task = HttpTaskServer.make_deserializable(task)
            uploaded_tasks[task.unic_task_id] = task
        return uploaded_tasks

    @staticmethod
    def upload_history(history):
        history_list = LinkedList()
        uploaded_history = list()
        for task in history:
            deserializable_task = HttpTaskServer.make_deserializable(task)
            history_list.add_to_end(deserializable_task)
        uploaded_history = history_list
        return uploaded_history

    @staticmethod
    def upload_saved_data():
        server = HttpTaskServer.server
        saved_data = server.load_data()
        if saved_data:
            saved_tasks, saved_history = json.loads(saved_data)
            server.manager.created_tasks = HttpTaskServer.upload_tasks(saved_tasks)
            server.manager.search_history = HttpTaskServer.upload_history(saved_history)
            server.manager.unic_task_id = max(server.manager.created_tasks) + 1

    def send_data_to_server(self):
        tasks = self.serialize_tasks(self.manager.created_tasks)
        history = self.serialize_history(self.manager.get_history())
        HttpTaskServer.server.save_to_server(tasks, history)


serv = HTTPServer(("localhost", 8000), HttpTaskServer)
HttpTaskServer.upload_saved_data()
serv.serve_forever()
