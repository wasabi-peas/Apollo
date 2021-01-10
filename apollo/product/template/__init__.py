# -*- coding: utf-8 -*-
"""doc string"""

import random
import decimal
import time
import contextlib
import numpy as np
from apollo.utils import precision_8


@contextlib.contextmanager
def timer(msg):
    beg = time.time()
    yield
    end = time.time()
    print(f'{msg} | {end - beg}')


with timer(0):
    for i in range(1000000):
        num = random.uniform(0, 1)
        num > 0.5


with timer(1):
    for i in range(1000000):
        num = random.uniform(0, 1)
        precision_8.greater(num, 0.5)


with timer(2):
    for i in range(1000000):
        num = decimal.Decimal(random.uniform(0, 1))
        num > 0.5


with timer(1):
    for i in range(1000000):
        num = random.uniform(0, 1)
        np.greater(num, 0.5)


if __name__ == '__main__':
    pass
