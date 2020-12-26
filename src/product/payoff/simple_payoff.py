# -*- coding: utf-8 -*-
"""doc string"""

from src.product.payoff.base_payoff import BasePayoff
from src.utils import Numerical


class ConstantPayoff(BasePayoff):
    """constant payoff"""

    def __init__(self, rate: Numerical):
        """
        parameters
        ----------
        rate: constant payoff rate
        """
        self.rate = rate

    def payoff(self, price: Numerical) -> Numerical:
        return self.rate


class DeltaOnePayoff(BasePayoff):
    """delta one payoff"""

    def __init__(self, strike: Numerical, weight: Numerical):
        """
        parameters
        ----------
        strike: strike price or level
        weight: participation rate
        """
        self.strike = strike
        self.weight = weight

    def payoff(self, price: Numerical) -> Numerical:
        return (price - self.strike) * self.weight


if __name__ == '__main__':
    pass
