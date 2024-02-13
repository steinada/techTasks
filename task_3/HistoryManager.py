from abc import ABC, abstractmethod


class HistoryManager(ABC):

    @abstractmethod
    def add_to_end(self, obj):
        pass

    @abstractmethod
    def add_to_start(self, obj):
        pass

    @abstractmethod
    def get_history(self):
        pass

    @abstractmethod
    def delete(self, obj):
        pass
