# -*- coding: utf-8 -*-
"""doc string"""

import abc
import datetime as dt
from typing import List, Optional, NoReturn, Union
from apollo.utils import Numerical


class Barrier(metaclass=abc.ABCMeta):
    """barrier base class"""

    def __init__(self, observe_dates: Optional[List[dt.date]] = None):
        """
        parameters
        ----------
        observe_dates: list of barrier observation dates
        """
        self.observe_dates = observe_dates or []

    def observe(self, date: dt.date, price: Numerical) -> bool:
        """
        observe if barrier is triggered under given price

        parameters
        ----------
        date: observe date
        price: asset price or performance

        returns
        -------
        barrier is observed or not (not triggered or not)
            * for triggered status, please call barrier.triggered
        """
        if date in self.observe_dates:
            return self._observe_impl(date, price)
        return False

    @abc.abstractmethod
    def _observe_impl(self, date: dt.date, price: Numerical) -> bool:
        pass

    def __repr__(self):
        return f'<{self.__class__.__name__}>'


def observe_schedule(*barriers: Union[Barrier, List[Barrier]]) -> List[dt.date]:
    observe_dates = set()
    for barrier in barriers:
        if isinstance(barrier, list):
            for each_barrier in barrier:
                observe_dates.update(each_barrier.observe_dates)
        else:
            observe_dates.update(barrier.observe_dates)
    return sorted(observe_dates)


if __name__ == '__main__':
    pass
