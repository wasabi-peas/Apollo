# -*- coding: utf-8 -*-
"""doc string"""

import datetime as dt
from typing import List, Union, NoReturn
from apollo.product.barrier.base_barrier import Barrier
from apollo.utils import Numerical


class _Observer:
    """barrier observer"""

    def __init__(self,
                 date: dt.date,
                 barrier_list: List[Barrier]):
        """
        barrier observer is created by _ObserverIterator
        * manually created by coder is not recommended

        parameters
        ----------
        date: current observation date
        barrier_list: list of barriers that should be observed on the date
        """
        self.date = date
        self.barrier_list = barrier_list

    def observe(self, price: Numerical) -> List[Barrier]:
        """
        do barrier observation one by one

        parameters
        ----------
        price: asset price or performance

        returns
        -------
        list of observed barriers
        """
        observed_barrier = []
        for barrier in self.barrier_list:
            if barrier.observe(self.date, price):
                observed_barrier.append(barrier)
        return observed_barrier


class _ObserverIterator:
    """iterator for barrier observers"""

    def __init__(self,
                 date_list: List[dt.date],
                 barrier_list: List[Barrier]):
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
                date=observe_date,
                barrier_list=self.barrier_list,
            )
        else:
            raise StopIteration


class BarrierObserver:
    """
    barrier observer
    call it as an iterator to observe all barriers

    examples
    --------
    >>> from apollo.product.barrier import KnockOutBarrier, KnockInBarrier
    >>> ko_barrier = KnockOutBarrier(position=1.2, direction='upper', inclusive=True,
    >>>                              observe_dates=[dt.date(2021, 1, 1), dt.date(2021, 2, 1)])
    >>> print(ko_barrier)
    <KnockOutBarrier upper@1.2>
    >>> ki_barrier = KnockInBarrier(position=0.7, direction='lower', inclusive=False,
    >>>                             observe_dates=[dt.date(2021, 1, 1), dt.date(2021, 1, 16), dt.date(2021, 2, 1)])
    >>> print(ki_barrier)
    <KnockInBarrier lower@0.7>
    >>> price = 1.0
    >>> for observer in BarrierObserver(barrier_list=[ko_barrier, ki_barrier]):
    >>>     observer.observe(price)
    >>>     print(observer.date)
    >>>     print(observer.barrier_list)
    >>>     price += 0.1
    2021-01-01
    [<KnockOutBarrier upper@1.2>, <KnockInBarrier lower@0.7>]
    2021-01-16
    [<KnockInBarrier lower@0.7>]
    2021-02-01
    [<KnockOutBarrier upper@1.2 [T]>, <KnockInBarrier lower@0.7>]
    """

    def __init__(self, barrier_list: List[Barrier] = None):
        """
        parameters
        ----------
        barrier_list: list of barriers to be observed
        """
        self.barrier_list = barrier_list or []

    def add_barrier(self, *barriers: Union[Barrier, List[Barrier]]) -> NoReturn:
        for barrier in barriers:
            if isinstance(barrier, list):
                self.barrier_list.extend(barrier)
            else:
                self.barrier_list.append(barrier)

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
