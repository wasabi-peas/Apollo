# -*- coding: utf-8 -*-
"""doc string"""

from src.product.payoff.base_payoff import Payoff
from src.utils import Numerical


class VanillaPayoff(Payoff):
    """vanilla option payoff"""
    _sign = 0

    def __init__(self,
                 strike: Numerical = 1,
                 weight: Numerical = 1,
                 *args, **kwargs):
        """
        parameters
        ----------
        strike: strike price or level
        weight: participation rate
        *args, **kwargs: see Payoff, including:
            rounding, accrual_basis, accrual_days
        """
        super().__init__(*args, **kwargs)
        self.strike = strike
        self.weight = weight

    def _payoff_impl(self, price: Numerical) -> Numerical:
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
