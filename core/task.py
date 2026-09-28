from abc import abstractmethod
class Task:
    @abstractmethod
    def to_string(self):
        pass