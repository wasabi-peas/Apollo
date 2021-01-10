# -*- coding: utf-8 -*-
"""doc string"""

import datetime as dt
from typing import List, Tuple, Dict, NoReturn, Callable
from apollo.product.barrier.base_barrier import Barrier


class _ObserverIterator:

    def __init__(self, schedule, barriers):
        self.schedule = schedule
        self.barriers = barriers
        self.loop_idx = 0

    def __next__(self) -> Tuple[dt.date, Dict[str, Callable]]:
        if self.loop_idx >= len(self.schedule):
            raise StopIteration
        observe_date = self.schedule[self.loop_idx]
        barriers = {name: barrier.observe_func(observe_date)
                    for name, barrier in self.barriers.items()
                    if observe_date in barrier.observe_dates}
        self.loop_idx += 1
        return observe_date, barriers


class Observer:

    def __init__(self):
        self.barriers = {}

    def register_barrier(self, name: str, barrier: Barrier) -> NoReturn:
        self.barriers[name] = barrier

    @property
    def schedule(self) -> List[dt.date]:
        observe_dates = set()
        for barrier in self.barriers.values():
            observe_dates.update(barrier.observe_dates)
        return sorted(observe_dates)

    def __iter__(self) -> _ObserverIterator:
        return _ObserverIterator(
            schedule=self.schedule,
            barriers=self.barriers,
        )


if __name__ == '__main__':
    pass
