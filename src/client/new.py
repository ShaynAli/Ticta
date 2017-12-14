
from abc import ABCMeta, abstractmethod


class TestMeta(metaclass=ABCMeta):

    @staticmethod
    def stat_met():
        pass

    @abstractmethod
    def test_abs(self):
        pass

    pass


