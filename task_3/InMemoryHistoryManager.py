from task_3.HistoryManager import HistoryManager


class LinkedList(HistoryManager):
    def __init__(self, max_length=10):
        self.head = None
        self.tail = None
        self.max_length = max_length
        self.current_length = 0
        self.add_history = list()
        self.node_dict = dict()

    def add_to_end(self, obj):
        new_node = self.Node(self.tail, obj, None)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            prev_node = self.tail
            prev_node.next_ = new_node
            self.tail = new_node
        self.current_length += 1
        self.add_history.append(obj.unic_task_id)
        self.node_dict[obj.unic_task_id] = new_node
        if self.current_length > self.max_length:
            self.delete(self.head.data)

    def add_to_start(self, obj):
        new_node = self.Node(None, obj, self.head)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            next_node = self.head
            next_node.prev = new_node
            self.head = new_node
        self.current_length += 1
        self.add_history.append(obj.unic_task_id)
        self.node_dict[obj.unic_task_id] = new_node
        if self.current_length > self.max_length:
            self.delete(self.tail.data)

    def delete(self, obj):
        if obj == self.head.data:
            if self.head.next_ is None:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.next_
                self.head.prev = None
        elif obj == self.tail.data:
            self.tail = self.tail.prev
            self.tail.next_ = None
            if self.tail.prev is not None:
                prev_tail = self.tail.prev
                prev_tail.next_ = self.tail
        else:
            present_obj = self.node_dict[obj.unic_task_id]
            before_obj = present_obj.prev
            after_obj = present_obj.next_
            before_obj.next_ = present_obj.next_
            after_obj.prev = present_obj.prev
        self.add_history.remove(obj.unic_task_id)
        self.current_length -= 1

    def get_history(self):
        history_list = []
        present_obj = self.head
        for _ in range(self.current_length):
            history_list.append(present_obj)
            present_obj = present_obj.next_
        return history_list

    class Node:
        def __init__(self, prev, data, next_):
            self.prev = prev
            self.data = data
            self.next_ = next_
