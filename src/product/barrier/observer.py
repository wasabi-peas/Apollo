# -*- coding: utf-8 -*-
"""doc string"""

import datetime as dt
from typing import List
from src.product.barrier.base_barrier import BaseBarrier
from src.utils import Numerical


class BarrierObserver:

    def __init__(self,
                 observe_date: dt.date,
                 barrier_list: List[BaseBarrier]):
        self.observe_date = observe_date
        self.barrier_list = barrier_list

    def observe(self, price: Numerical) -> List[BaseBarrier]:
        for barrier in self.barrier_list:
            barrier.observe(price)
        return self.barrier_list


class _ObserverIterator:
    def __init__(self, date_list, barrier_list):
        self.date_list = date_list
        self.barrier_list = barrier_list
        self.date_index = 0

    def __next__(self) -> BarrierObserver:
        if self.date_index < len(self.date_list):
            observe_date = self.date_list[self.date_index]
            self.date_index += 1
            return BarrierObserver(
                observe_date=observe_date,
                barrier_list=[barrier for barrier in self.barrier_list
                              if observe_date in barrier.observe_dates],
            )
        else:
            raise StopIteration


class ObserverFactory:

    def __init__(self, barrier_list: List[BaseBarrier] = None):
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
    import datetime as dt
    from src.product.barrier import UpperBarrier, LowerBarrier
    barrier_1 = UpperBarrier(1.2, inclusive=True)
    barrier_2 = LowerBarrier(0.7, inclusive=False)
    barrier_1.register_observe_date([dt.date(2020, 1, 1), dt.date(2020, 2, 1)])
    barrier_2.register_observe_date([dt.date(2020, 1, 1), dt.date(2020, 1, 16), dt.date(2020, 2, 1)])
    for observer in ObserverFactory(barrier_list=[barrier_1, barrier_2]):
        print(observer.observe_date)
        print(observer.barrier_list)
        print('\n')
