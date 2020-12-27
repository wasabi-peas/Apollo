# -*- coding: utf-8 -*-
"""doc string"""

import datetime as dt
from apollo.product.barrier import (
    KnockOutBarrier,
    KnockInBarrier,
    BarrierObserver,
)
from apollo.product.payoff import (
    VanillaPutPayoff,
    ConstantPayoff,
)


class SnowBall:

    def __init__(self, parameters):
        ko_obs_date = [dt.date.fromisoformat(d)
                       for d in parameters['ObservationDate']]

        ki_obs_date = [dt.date.fromisoformat(d)
                       for d in parameters['KIObservationDate']]

        self.ko_barrier = KnockOutBarrier(
            direction='upper',
            position=parameters['UpperBarrier'],
            observe_dates=ko_obs_date,
            inclusive=True,
        )

        self.ki_barrier = KnockInBarrier(
            direction='lower',
            position=parameters['KIBarrier'],
            observe_dates=ki_obs_date,
            inclusive=True,
        )

        self.ko_payoff = {
            date: ConstantPayoff(rate=rebate)
            for date, rebate in zip(
                    ko_obs_date,
                    parameters['KnockOutRebate'],
            )
        }

        self.ki_payoff = VanillaPutPayoff(
            strike=parameters['Strike'],
            weight=-1,
        )

        self.mat_payoff = ConstantPayoff(
            rate=parameters['MaturityBonusCoupon'],
        )

    def payoff(self):
        price = 1.0
        barrier = BarrierObserver()
        barrier.add_barrier(self.ko_barrier, self.ki_barrier)
        for observer in barrier:
            observer.observe(price)
            if self.ko_barrier.triggered:
                payoff = self.ko_payoff[observer.date]
                return payoff.payoff(price)
            price -= 0.2
        payoff = self.ki_payoff if self.ki_barrier.triggered \
            else self.mat_payoff
        return payoff.payoff(price)


if __name__ == '__main__':
    test_param = {
        'UpperBarrier': [1.2, 1.2],
        'ObservationDate': ['2020-01-01', '2020-02-01'],
        'KnockOutRebate': [0.1, 0.2],
        'KIBarrier': [0.7, 0.7, 0.7],
        'Strike': 1.0,
        'MaturityBonusCoupon': 0.05,
        'KIObservationDate': ['2020-01-01', '2020-01-16', '2020-02-01'],
    }
    snowball = SnowBall(test_param)
    print(snowball.payoff())
