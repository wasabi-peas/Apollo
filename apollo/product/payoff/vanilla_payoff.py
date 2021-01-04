# -*- coding: utf-8 -*-
"""doc string"""

from apollo.product.payoff.base_payoff import Payoff
from apollo.utils import Numerical
from apollo.product.payoff.basic_functions import Ramp


class VanillaPayoff(Payoff):
    """vanilla option payoff"""
    _func_cls = [Ramp]
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
    c = VanillaCallPayoff(strike=1.2, weight=0.8)
    print(c.payoff(1))
    print(c.payoff(1.4))
    p = VanillaPutPayoff(strike=0.8, weight=1.2)
    print(p.payoff(1.4))
    print(p.payoff(0.5))
