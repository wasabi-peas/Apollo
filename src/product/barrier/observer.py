# -*- coding: utf-8 -*-
"""doc string"""

import datetime as dt
from typing import List
from src.product.barrier.base_barrier import BaseBarrier
from src.utils import Numerical


class _Observer:
    """barrier observer"""

    def __init__(self,
                 observe_date: dt.date,
                 barrier_list: List[BaseBarrier]):
        """
        barrier observer is created by _ObserverIterator
        * manually created by coder is not recommended

        parameters
        ----------
        observe_date: current observation date
        barrier_list: list of barriers that should be observed on the date
        """
        self.observe_date = observe_date
        self.barrier_list = barrier_list

    def observe(self, price: Numerical) -> List[BaseBarrier]:
        """
        do barrier observation one by one

        parameters
        ----------
        price: asset price or performance

        returns
        -------
        list of observed barriers
        """
        for barrier in self.barrier_list:
            barrier.observe(price)
        return self.barrier_list


class _ObserverIterator:
    """iterator for barrier observers"""

    def __init__(self,
                 date_list: List[dt.date],
                 barrier_list: List[BaseBarrier]):
        """
        observer iterator is created by BarrierObserver
        * manually created by coder is not recommended

        parameters
        ----------
        date_list: list of observation dates
            union list for all barriers
        barrier_list: list of barriers to be observed
        """
        self.date_list = date_list
        self.barrier_list = barrier_list
        self.date_index = 0

    def __next__(self) -> _Observer:
        if self.date_index < len(self.date_list):
            observe_date = self.date_list[self.date_index]
            self.date_index += 1
            return _Observer(
                observe_date=observe_date,
                barrier_list=[barrier for barrier in self.barrier_list
                              if observe_date in barrier.observe_dates],
            )
        else:
            raise StopIteration


class BarrierObserver:
    """
    barrier observer
    call it as an iterator to observe all barriers

    examples
    --------
    >>> from src.product.barrier import UpperBarrier, LowerBarrier
    >>> up_barrier = UpperBarrier(1.2, inclusive=True)
    >>> lw_barrier = LowerBarrier(0.7, inclusive=False)
    >>> up_barrier.register_observe_date(
    >>>     [dt.date(2021, 1, 1), dt.date(2021, 2, 1)],
    >>> )
    >>> lw_barrier.register_observe_date(
    >>>     [dt.date(2021, 1, 1), dt.date(2021, 1, 16), dt.date(2021, 2, 1)]
    >>> )
    >>> price = 1.0
    >>> for observer in BarrierObserver(barrier_list=[up_barrier, lw_barrier]):
    >>>     observer.observe(price)
    >>>     print(observer.observe_date)
    >>>     print(observer.barrier_list)
    >>>     price += 0.1
    2021-01-01
    [<UpperBarrier @1.2 no-trigger>, <LowerBarrier @0.7 no-trigger>]
    2021-01-16
    [<LowerBarrier @0.7 no-trigger>]
    2021-02-01
    [<UpperBarrier @1.2 trigger>, <LowerBarrier @0.7 no-trigger>]
    """

    def __init__(self, barrier_list: List[BaseBarrier] = None):
        """
        parameters
        ----------
        barrier_list: list of barriers to be observed
        """
        self.barrier_list = barrier_list

    def __iter__(self) -> _ObserverIterator:
        observe_dates = set()
        for barrier in self.barrier_list:
            observe_dates.update(barrier.observe_dates)
        observe_dates = sorted(observe_dates)
        return _ObserverIterator(
            date_list=observe_dates,
            barrier_list=self.barrier_list,
        )


if __name__ == '__main__':
    pass
