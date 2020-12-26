# -*- coding: utf-8 -*-
"""doc string"""

from typing import Callable
from src.product.barrier.base_barrier import BaseBarrier
from src.utils import Numerical, precision_8


class _PositionBarrier(BaseBarrier):
    """simple position barrier - compare asset price and barrier position"""
    _check_func = (Callable, Callable)

    def __init__(self, position: Numerical, inclusive: bool = True,
                 *args, **kwargs):
        """
        parameters
        ----------
        position: barrier position in price or performance
        inclusive: trigger when asset price equals to barrier position
        observe_dates: list of barrier observation dates
        """
        super().__init__(*args, **kwargs)
        self.position = position
        self.inclusive = inclusive

    def _observe_impl(self, price: Numerical) -> bool:
        if self.inclusive:
            check_func = self._check_func[0]
        else:
            check_func = self._check_func[1]
        if check_func(price, self.position):
            self.triggered = True
        return self.triggered

    def __repr__(self):
        status = 'trigger' if self.triggered else 'no-trigger'
        return f'<{self.__class__.__name__} @{self.position} {status}>'


class UpperBarrier(_PositionBarrier):
    """triggered when asset price is greater than barrier position"""
    _check_func = (precision_8.not_smaller, precision_8.greater)


class LowerBarrier(_PositionBarrier):
    """triggered when asset price is smaller than barrier position"""
    _check_func = (precision_8.not_greater, precision_8.smaller)


if __name__ == '__main__':
    pass
