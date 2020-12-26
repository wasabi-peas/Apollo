# -*- coding: utf-8 -*-
"""doc string"""

from src.product.payoff.base_payoff import BasePayoff
from src.utils import Numerical


class VanillaPayoff(BasePayoff):
    _sign = 0

    def __init__(self, strike: Numerical, weight: Numerical):
        self.strike = strike
        self.weight = weight

    def payoff(self, price: Numerical) -> Numerical:
        return max(self._sign * (price - self.strike), 0)


class VanillaCallPayoff(VanillaPayoff):
    _sign = 1


class VanillaPutPayoff(VanillaPayoff):
    _sign = -1


if __name__ == '__main__':
    pass
