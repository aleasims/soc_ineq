import numpy as np
import random

FAIR_TRADE = 0.5


class Model:
    def __init__(self, N, S=None, stack=None):
        """Create new model.

        Args:
            N (int): number of people, must be even.
            S (int or None): initial number of coins, must be > 0.
            stack (List[int] or None): initial coins distribution.
        """
        if N % 2:
            raise ValueError("N must be even")

        self.N = N
        self.S = S if S else sum(stack)
        self.t = 0

        if self.S <= 0:
            raise ValueError("S must be > 0")

        self.stack = stack if stack is not None else np.array([self.S] * N)

        self.total = self.N * self.S
        self.C = (np.exp(-1 / self.S) - 1) / (np.exp(-(self.S * self.N + 1) / self.S) - 1)
        self.stack_lim = self. C * np.exp(-np.arange(self.total + 1) / self.S)

    def EDF(self, x):
        """Emperical distribution function.

        P(money <= x)
        """
        return np.where(self.stack <= x)[0].shape[0] / self.N

    def EPF(self, x):
        """Emperical probability function.

        P(money = x)
        """
        return np.where(self.stack == x)[0].shape[0] / self.N

    def coins(self):
        """Refers to c(t)"""
        coins = np.zeros_like(self.stack_lim)
        for c in self.stack:
            coins[c] = self.EPF(c)
        return coins

    def run(self, days=1):
        for _ in range(days):
            self.step()

    def step(self):
        for i, j in self._pairs():
            self._trade(i, j)
        self.t += 1

    def _pairs(self):
        return np.random.permutation(self.N).reshape(int(self.N / 2), 2)

    def _trade(self, i, j):
        pot = 0
        if self.stack[i] > 0:
            self.stack[i] -= 1
            pot += 1
        if self.stack[j] > 0:
            self.stack[j] -= 1
            pot += 1

        win = random.choice([i, j])
        self.stack[win] += pot
