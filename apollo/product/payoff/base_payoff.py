# -*- coding: utf-8 -*-
"""doc string"""

import abc
from typing import Optional
from apollo.utils import Numerical


class Payoff(metaclass=abc.ABCMeta):
    """payoff base class"""

    def __init__(self,
                 rounding: Optional[int] = None,
                 accrual_basis: int = 365,
                 accrual_days: int = 365,
                 *args, **kwargs):
        """
        parameters
        ----------
        rounding: rounding digit of payoff
            None means no rounding
        accrual_basis: how many days in a year, typically 365
        accrual_days: accrual days, used to calculate annualised coefficient
            annualised coefficient = accrual days / accrual basis
            final payoff = payoff * annualised coefficient
        """
        self.rounding = rounding
        self.accrual_basis = accrual_basis
        self.accrual_days = accrual_days

    def payoff(self, price: Numerical) -> Numerical:
        """
        get payoff of given asset price

        parameters
        ----------
        price: asset price or performance

        returns
        -------
        payoff value
        """
        payoff = self._payoff_impl(price)
        payoff = payoff * self.accrual_days / self.accrual_basis
        if self.rounding:
            payoff = round(payoff, self.rounding)
        return payoff

    @abc.abstractmethod
    def _payoff_impl(self, price: Numerical) -> Numerical:
        pass

    def __repr__(self):
        return self.__class__.__name__


if __name__ == '__main__':
    pass
