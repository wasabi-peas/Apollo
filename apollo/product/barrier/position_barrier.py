# -*- coding: utf-8 -*-
"""doc string"""

import datetime as dt
import numpy as np
from typing import List, Union, Callable
from apollo.product.barrier.base_barrier import Barrier
from apollo.utils import Numerical, LazyProperty, precision_8


class PositionBarrier(Barrier):
    """
    most common barrier to compare asset price and barrier position
    to decide if barrier should be triggered or not
    """

    def __init__(self,
                 position: Union[Numerical, List[Numerical]],
                 observe_dates: Union[List[dt.date]],
                 direction: str = 'upper',
                 inclusive: bool = True):
        """
        parameters
        ----------
        position: barrier position in price or performance to compare asset price with
            when position is given as list, dimension should match the dimension of observation dates
        observe_dates: list of barrier observation dates
        direction: upper barrier or lower barrier
        inclusive: trigger or not when asset price equals to barrier position
        """
        super().__init__(observe_dates)
        assert direction in ['upper', 'lower'], \
            f"direction should be either 'upper' or 'lower', " \
            f"got '{direction}'"
        self.direction = direction
        if isinstance(position, list):
            assert len(position) == len(self.observe_dates), \
                f'position dimension ({len(position)}) != ' \
                f'date dimension ({len(self.observe_dates)})'
            self.position = {date: pos for date, pos in
                             zip(self.observe_dates, position)}
        else:
            self.position = position
        self.inclusive = inclusive
        self.precision = precision_8

    def _position_on_date(self, date: dt.date) -> Numerical:
        if isinstance(self.position, dict):
            return self.position[date]
        else:
            return self.position

    @LazyProperty
    def _compare_func(self):
        if self.direction == 'upper':
            return self.precision.greater_equal \
                if self.inclusive else self.precision.greater
        else:
            return self.precision.less_equal \
                if self.inclusive else self.precision.less

    def observe(self, date: dt.date, price: Union[Numerical, np.array]
                ) -> Union[bool, np.array]:
        position = self._position_on_date(date)
        return self._compare_func(price, position)

    def observe_func(self, date: dt.date) -> Callable:
        position = self._position_on_date(date)

        def func(price: Numerical) -> bool:
            return self._compare_func(price, position)

        return func

    def __repr__(self):
        description = f'{self.direction}@{self.position}'
        return f'<{self.__class__.__name__} {description}>'


if __name__ == '__main__':
    pass
