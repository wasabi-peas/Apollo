"""doc string"""

from apollo.product.payoff.base_payoff import Payoff
from apollo.utils import Numerical
from apollo.product.payoff.basic_functions import Constant, Linear


class ConstantPayoff(Payoff):
    """constant payoff"""
    _func_cls = [Constant]

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


class DeltaOnePayoff(Payoff):
    """delta one payoff"""
    _func_cls = [Linear]

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


if __name__ == '__main__':
    cp = ConstantPayoff(rate=0.12)
    print(cp.payoff(price=12))
    d1p = DeltaOnePayoff(strike=1, weight=2)
    print(d1p.payoff(price=1.25))
