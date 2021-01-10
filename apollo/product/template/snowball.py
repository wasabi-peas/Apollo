# -*- coding: utf-8 -*-
"""doc string"""

import time
import contextlib
import numpy as np
import datetime as dt
from state_machine import (
    acts_as_state_machine,
    State,
    Event,
    before,
    after,
)
from apollo.product.barrier import (
    KnockOutBarrier,
    KnockInBarrier,
    Observer,
)
from apollo.product.payoff import (
    VanillaPutPayoff,
    ConstantPayoff,
)
from apollo.utils.typing import Numerical


@contextlib.contextmanager
def timer(msg):
    beg = time.time()
    yield
    end = time.time()
    print(f'{msg} | {end - beg}')


class ProductPayoff:
    def __init__(self, date, tag, amount):
        self.date = date
        self.tag = tag
        self.amount = amount

    def __repr__(self):
        return f'{self.amount} @{self.date!s}'


@acts_as_state_machine
class SnowballProduct:
    name = 'SnowBall Option'

    normal = State(initial=True)
    knocked_out = State()
    knocked_in = State()

    knock_out = Event(
        from_states=(normal, knocked_in),
        to_state=knocked_out,
    )
    knock_in = Event(
        from_states=normal,
        to_state=knocked_in,
    )

    pending_payoff = 0
    retired = False

    def __init__(self):
        self.payoff = []

    @after('knock_out')
    def ko_payoff(self):
        self.retired = True

    def confirm_payoff(self, date, tag):
        self.payoff.append(ProductPayoff(date, tag, self.pending_payoff))
        self.pending_payoff = 0

    def make_payoff(self, date, tag, amount):
        self.payoff.append(ProductPayoff(date, tag, amount))

    def __repr__(self):
        return f'<{self.__class__.__name__} state={self.current_state}>'


class SnowBallSimulate:

    def __init__(self, product, parameters):
        self.product = product
        self.strike_date = dt.date.fromisoformat(parameters['StrikeDate'])
        self.maturity = dt.date.fromisoformat(parameters['Maturity'])

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

    def simulate(self, path_generator, num_of_path):
        with timer('prepare'):
            observer = Observer()
            observer.register_barrier('KO', self.ko_barrier)
            observer.register_barrier('KI', self.ki_barrier)
            product_list = np.array([self.product() for _ in range(num_of_path)])
            live_func = np.vectorize(lambda x: not x.retired)
            live_product = product_list
            live_path = np.ones(num_of_path)
            prev_date = self.strike_date
            ko_batch = np.vectorize(self.ko, cache=True)
            ki_batch = np.vectorize(self.ki, cache=True)
            retire_batch = np.vectorize(self.retire, cache=True)
        with timer('simulate'):
            for date, obs_func in observer:
                live_index = np.where(live_func(live_product))
                live_path = live_path[live_index]
                live_product = live_product[live_index]
                if len(live_product) == 0:
                    break
                new_path = path_generator.get_path(len(live_product))
                live_path = populate_path(live_path, new_path, date - prev_date)
                if 'KO' in obs_func:
                    ko = obs_func['KO'](live_path)
                    ko_product = live_product[np.where(ko)]
                    if len(ko_product) > 0:
                        ko_batch(self.ko_payoff[date], live_path[np.where(ko)], ko_product, date)
                    nko_path = live_path[np.where(~ko)]
                    nko_product = live_product[np.where(~ko)]
                else:
                    nko_path = live_path
                    nko_product = live_product
                if 'KI' in obs_func:
                    ki = obs_func['KI'](nko_path)
                    ki_product = nko_product[np.where(ki)]
                    if len(ki_product) > 0:
                        ki_batch(ki_product)
                if date == self.maturity:
                    retire_batch(nko_path, nko_product, date)
                prev_date = date
        with timer('payoff'):
            pv = np.vectorize(self.calculate_pv)(product_list)
            print(np.average(pv))

    def calculate_pv(self, product):
        r = 0.03
        pv = 0
        for payoff in product.payoff:
            t = (payoff.date - self.strike_date).days
            df = np.exp(- r * t / 365)
            pv += df * payoff.amount
        return pv

    def ko(self, payoff, price, product, date):
        product.knock_out()
        product.pending_payoff = payoff.payoff(price)
        product.confirm_payoff(date, 'knock out rebate rate')

    def ki(self, product):
        if product.current_state != product.knocked_in:
            product.knock_in()

    def retire(self, price, product, date):
        product.retired = True
        if product.current_state == product.knocked_in:
            product.pending_payoff = self.ki_payoff.payoff(price)
            product.confirm_payoff(date, 'knock in put value')
        else:
            product.pending_payoff = self.mat_payoff.payoff(price)
            product.confirm_payoff(date, 'maturity bonus coupon')


def populate_path(prev_path, new_path, date_pass):
    r = 0.03
    vol = 0.5
    t = date_pass.days / 365
    return prev_path * np.exp((r - 0.5 * vol ** 2) * t + vol * np.sqrt(t) * new_path)


if __name__ == '__main__':
    test_param = {
        'UpperBarrier': 1.2,
        'ObservationDate': ['2020-01-31', '2020-02-29', '2020-03-31', '2020-04-30', '2020-05-31', '2020-06-30', '2020-07-31', '2020-08-31', '2020-09-30', '2020-10-31', '2020-11-30', '2020-12-31'],
        'KnockOutRebate': [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
        'KIBarrier': 0.7,
        'Strike': 1.0,
        'StrikeDate': '2020-01-01',
        'MaturityBonusCoupon': 0.05,
        'Maturity': '2020-12-31',
        'KIObservationDate': ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05', '2020-01-06', '2020-01-07', '2020-01-08', '2020-01-09', '2020-01-10', '2020-01-11', '2020-01-12', '2020-01-13', '2020-01-14', '2020-01-15', '2020-01-16', '2020-01-17', '2020-01-18', '2020-01-19', '2020-01-20', '2020-01-21', '2020-01-22', '2020-01-23', '2020-01-24', '2020-01-25', '2020-01-26', '2020-01-27', '2020-01-28', '2020-01-29', '2020-01-30', '2020-01-31', '2020-02-01', '2020-02-02', '2020-02-03', '2020-02-04', '2020-02-05', '2020-02-06', '2020-02-07', '2020-02-08', '2020-02-09', '2020-02-10', '2020-02-11', '2020-02-12', '2020-02-13', '2020-02-14', '2020-02-15', '2020-02-16', '2020-02-17', '2020-02-18', '2020-02-19', '2020-02-20', '2020-02-21', '2020-02-22', '2020-02-23', '2020-02-24', '2020-02-25', '2020-02-26', '2020-02-27', '2020-02-28', '2020-02-29', '2020-03-01', '2020-03-02', '2020-03-03', '2020-03-04', '2020-03-05', '2020-03-06', '2020-03-07', '2020-03-08', '2020-03-09', '2020-03-10', '2020-03-11', '2020-03-12', '2020-03-13', '2020-03-14', '2020-03-15', '2020-03-16', '2020-03-17', '2020-03-18', '2020-03-19', '2020-03-20', '2020-03-21', '2020-03-22', '2020-03-23', '2020-03-24', '2020-03-25', '2020-03-26', '2020-03-27', '2020-03-28', '2020-03-29', '2020-03-30', '2020-03-31', '2020-04-01', '2020-04-02', '2020-04-03', '2020-04-04', '2020-04-05', '2020-04-06', '2020-04-07', '2020-04-08', '2020-04-09', '2020-04-10', '2020-04-11', '2020-04-12', '2020-04-13', '2020-04-14', '2020-04-15', '2020-04-16', '2020-04-17', '2020-04-18', '2020-04-19', '2020-04-20', '2020-04-21', '2020-04-22', '2020-04-23', '2020-04-24', '2020-04-25', '2020-04-26', '2020-04-27', '2020-04-28', '2020-04-29', '2020-04-30', '2020-05-01', '2020-05-02', '2020-05-03', '2020-05-04', '2020-05-05', '2020-05-06', '2020-05-07', '2020-05-08', '2020-05-09', '2020-05-10', '2020-05-11', '2020-05-12', '2020-05-13', '2020-05-14', '2020-05-15', '2020-05-16', '2020-05-17', '2020-05-18', '2020-05-19', '2020-05-20', '2020-05-21', '2020-05-22', '2020-05-23', '2020-05-24', '2020-05-25', '2020-05-26', '2020-05-27', '2020-05-28', '2020-05-29', '2020-05-30', '2020-05-31', '2020-06-01', '2020-06-02', '2020-06-03', '2020-06-04', '2020-06-05', '2020-06-06', '2020-06-07', '2020-06-08', '2020-06-09', '2020-06-10', '2020-06-11', '2020-06-12', '2020-06-13', '2020-06-14', '2020-06-15', '2020-06-16', '2020-06-17', '2020-06-18', '2020-06-19', '2020-06-20', '2020-06-21', '2020-06-22', '2020-06-23', '2020-06-24', '2020-06-25', '2020-06-26', '2020-06-27', '2020-06-28', '2020-06-29', '2020-06-30', '2020-07-01', '2020-07-02', '2020-07-03', '2020-07-04', '2020-07-05', '2020-07-06', '2020-07-07', '2020-07-08', '2020-07-09', '2020-07-10', '2020-07-11', '2020-07-12', '2020-07-13', '2020-07-14', '2020-07-15', '2020-07-16', '2020-07-17', '2020-07-18', '2020-07-19', '2020-07-20', '2020-07-21', '2020-07-22', '2020-07-23', '2020-07-24', '2020-07-25', '2020-07-26', '2020-07-27', '2020-07-28', '2020-07-29', '2020-07-30', '2020-07-31', '2020-08-01', '2020-08-02', '2020-08-03', '2020-08-04', '2020-08-05', '2020-08-06', '2020-08-07', '2020-08-08', '2020-08-09', '2020-08-10', '2020-08-11', '2020-08-12', '2020-08-13', '2020-08-14', '2020-08-15', '2020-08-16', '2020-08-17', '2020-08-18', '2020-08-19', '2020-08-20', '2020-08-21', '2020-08-22', '2020-08-23', '2020-08-24', '2020-08-25', '2020-08-26', '2020-08-27', '2020-08-28', '2020-08-29', '2020-08-30', '2020-08-31', '2020-09-01', '2020-09-02', '2020-09-03', '2020-09-04', '2020-09-05', '2020-09-06', '2020-09-07', '2020-09-08', '2020-09-09', '2020-09-10', '2020-09-11', '2020-09-12', '2020-09-13', '2020-09-14', '2020-09-15', '2020-09-16', '2020-09-17', '2020-09-18', '2020-09-19', '2020-09-20', '2020-09-21', '2020-09-22', '2020-09-23', '2020-09-24', '2020-09-25', '2020-09-26', '2020-09-27', '2020-09-28', '2020-09-29', '2020-09-30', '2020-10-01', '2020-10-02', '2020-10-03', '2020-10-04', '2020-10-05', '2020-10-06', '2020-10-07', '2020-10-08', '2020-10-09', '2020-10-10', '2020-10-11', '2020-10-12', '2020-10-13', '2020-10-14', '2020-10-15', '2020-10-16', '2020-10-17', '2020-10-18', '2020-10-19', '2020-10-20', '2020-10-21', '2020-10-22', '2020-10-23', '2020-10-24', '2020-10-25', '2020-10-26', '2020-10-27', '2020-10-28', '2020-10-29', '2020-10-30', '2020-10-31', '2020-11-01', '2020-11-02', '2020-11-03', '2020-11-04', '2020-11-05', '2020-11-06', '2020-11-07', '2020-11-08', '2020-11-09', '2020-11-10', '2020-11-11', '2020-11-12', '2020-11-13', '2020-11-14', '2020-11-15', '2020-11-16', '2020-11-17', '2020-11-18', '2020-11-19', '2020-11-20', '2020-11-21', '2020-11-22', '2020-11-23', '2020-11-24', '2020-11-25', '2020-11-26', '2020-11-27', '2020-11-28', '2020-11-29', '2020-11-30', '2020-12-01', '2020-12-02', '2020-12-03', '2020-12-04', '2020-12-05', '2020-12-06', '2020-12-07', '2020-12-08', '2020-12-09', '2020-12-10', '2020-12-11', '2020-12-12', '2020-12-13', '2020-12-14', '2020-12-15', '2020-12-16', '2020-12-17', '2020-12-18', '2020-12-19', '2020-12-20', '2020-12-21', '2020-12-22', '2020-12-23', '2020-12-24', '2020-12-25', '2020-12-26', '2020-12-27', '2020-12-28', '2020-12-29', '2020-12-30', '2020-12-31'],
    }
    simulate = SnowBallSimulate(SnowballProduct, test_param)

    class PathGenerator:

        def __init__(self, seed=888):
            self.seed = seed
            self.generator = np.random.mtrand.RandomState(seed=self.seed)

        def get_path(self, num_of_path):
            return self.generator.randn(num_of_path)

    # import cProfile
    # cProfile.run('simulate.simulate_live(PathGenerator(), 100000)')
    simulate.simulate(PathGenerator(), 100000)
