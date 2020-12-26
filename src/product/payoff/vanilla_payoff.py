# -*- coding: utf-8 -*-
"""doc string"""

from src.product.payoff.base_payoff import BasePayoff
from src.utils import Numerical


class VanillaPayoff(BasePayoff):
    """vanilla option payoff"""
    _sign = 0

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
        return max(self._sign * (price - self.strike), 0) * self.weight


class VanillaCallPayoff(VanillaPayoff):
    """
    vanilla call option
    payoff = max(S - K) * p
    """
    _sign = 1


class VanillaPutPayoff(VanillaPayoff):
    """
    vanilla put option
    payoff = max(K - S) * p
    """
    _sign = -1


if __name__ == '__main__':
    pass
