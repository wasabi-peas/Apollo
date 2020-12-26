# -*- coding: utf-8 -*-
"""doc string"""

import abc


class BasePayoff(metaclass=abc.ABCMeta):
    """payoff base class"""

    @abc.abstractmethod
    def payoff(self, price: float) -> float:
        """
        get payoff of given asset price

        parameters
        ----------
        price: asset price or performance

        returns
        -------
        payoff value
        """
        pass

    def __repr__(self):
        return self.__class__.__name__


if __name__ == '__main__':
    pass
