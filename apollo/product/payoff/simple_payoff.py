# -*- coding: utf-8 -*-
"""doc string"""

from apollo.product.payoff.base_payoff import Payoff
from apollo.utils import Numerical


class ConstantPayoff(Payoff):
    """constant payoff"""

    def __init__(self,
                 rate: Numerical = 0,
                 *args, **kwargs):
        """
        parameters
        ----------
        rate: constant payoff rate
        *args, **kwargs: see Payoff, including:
            rounding, accrual_basis, accrual_days
        """
        super().__init__(*args, **kwargs)
        self.rate = rate

    def _payoff_impl(self, price: Numerical) -> Numerical:
        return self.rate


class DeltaOnePayoff(Payoff):
    """delta one payoff"""

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
        return (price - self.strike) * self.weight


if __name__ == '__main__':
    pass
