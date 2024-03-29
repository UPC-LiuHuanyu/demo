# -*- coding:utf-8 -*-

import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta


def mh(q, p, m, n):
    # randomize a number
    x = random.uniform(0.1, 1)
    for t in range(0, m + n):
        x_sample = q.sample(x)
        try:
            accept_prob = min(1, p.prob(x_sample) * q.prob(x_sample, x) / (p.prob(x) * q.prob(x, x_sample)))
        except:
            accept_prob = 0

        u = random.uniform(0, 1)

        if u < accept_prob:
            x = x_sample

        if t >= m:
            yield x


class Exponential(object):
    def __init__(self, scale):
        self.scale = scale
        self.lam = 1.0 / scale

    def prob(self, x):
        if x <= 0:
            raise Exception("The sample shouldn't be less than zero")

        result = self.lam * np.exp(-x * self.lam)
        return result

    def sample(self, num):
        sample = np.random.exponential(self.scale, num)
        return sample


class Norm():
    def __init__(self, mean, std):
        self.mean = mean
        self.sigma = std

    def prob(self, x):
        return np.exp(-(x - self.mean) ** 2 / (2 * self.sigma ** 2.0)) * 1.0 / (np.sqrt(2 * np.pi) * self.sigma)

    def sample(self, num):
        sample = np.random.normal(self.mean, self.sigma, size=num)
        return sample


class Transition():
    def __init__(self, sigma):
        self.sigma = sigma

    def sample(self, cur_mean):
        cur_sample = np.random.normal(cur_mean, scale=self.sigma, size=1)[0]
        return cur_sample

    def prob(self, mean, x):
        return np.exp(-(x - mean) ** 2 / (2 * self.sigma ** 2.0)) * 1.0 / (np.sqrt(2 * np.pi) * self.sigma)


class Beta(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.bet_dist = beta(self.a, self.b)

    def prob(self, x):
        result = self.bet_dist.pdf(x)
        return result

    def sample(self, num):
        sample = np.random.beta(self.a, self.b, num)
        return sample


# 假设我们的转移核方差为10的正态分布
q = Transition(10)

m = 100
n = 10000  # 采样个数


def draw_exp():
    # 假设我们的目标概率密度函数p1(x)是指数概率密度函数
    scale = 5
    p1 = Exponential(scale)
    simulate_samples_p1 = [li for li in mh(q, p1, m, n)]
    plt.subplot(2, 3, 1)
    plt.hist(simulate_samples_p1, 100)
    plt.title("Simulated X ~ Exponential(1/5)")
    samples = p1.sample(n)
    plt.subplot(2, 3, 4)
    plt.hist(samples, 100)
    plt.title("True X ~ Exponential(1/5)")




def draw_norm():
    # 假设我们的目标概率密度函数p1(x)是均值方差分别为3,2的正态分布
    p2 = Norm(3, 2)
    simulate_samples_p2 = [li for li in mh(q, p2, m, n)]
    plt.subplot(2, 3, 2)
    plt.hist(simulate_samples_p2, 50)
    plt.title("Simulated X ~ N(3,2)")
    samples = p2.sample(n)
    plt.subplot(2, 3, 5)
    plt.hist(samples, 50)
    plt.title("True X ~ N(3,2)")




def draw_beta():
    p3 = Beta(0.5, 0.5)
    simulate_samples_p3 = [li for li in mh(q, p3, m, n)]
    plt.subplot(2, 3, 3)
    plt.hist(simulate_samples_p3, 50)
    plt.title("Simulated X ~ Beta(0.5,0.5)")
    samples = p3.sample(n)
    plt.subplot(2, 3, 6)
    plt.hist(samples, 50)
    plt.title("True X ~ Beta(0.5,0.5)")

draw_exp()
draw_norm()
draw_beta()

plt.suptitle("Transition Kernel N(0,10)simulation results")
plt.show()
