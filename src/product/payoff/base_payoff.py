# -*- coding: utf-8 -*-
"""doc string"""

import abc


class BasePayoff(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def payoff(self, price: float) -> float:
        pass


if __name__ == '__main__':
    pass
