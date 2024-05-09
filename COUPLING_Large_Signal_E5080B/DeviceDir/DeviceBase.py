from abc import ABCMeta, abstractmethod
import threading

class cDeviceBase():
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.__name = name
        self.locker = threading.Lock()

    def get_name(self):
        return self.__name

    def set_name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            raise ValueError

    @abstractmethod
    def Setup(self):
        return False

    @abstractmethod
    def Open(self):
        return False

    @abstractmethod
    def Close(self):
        return False