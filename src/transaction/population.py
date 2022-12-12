from abc import ABC, abstractmethod
from IPython import display
from prettytable import PrettyTable

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Population(ABC):

    def __init__(self, n:int, mean:float) -> None:
        """
        :param n: the size of the population to initialize
        :param mean: the mean wealth of the population to initialize
        """
        self.n = n
        self.history = [np.array([mean] * n)]

    def initial(self) -> np.ndarray:
        """
        :return: the initial wealth distribution of the population
        """
        return self.history[0]
    
    def current(self) -> np.ndarray:
        """
        :return: the current wealth distribution of the population
        """
        return self.history[-1]
    
    def update(self, new:np.ndarray) -> None:
        """
        :param new: the new population to update in the history
        Description: updates the wealth history of the population
        """
        self.history.append(new)

    def simulate(self, transaction, n:int) -> None:
        """
        :param function: the transaction function to use in the simulation
        :param n: the total number of transactions to simulate
        Description: simulate the specified type of transaction for n times in the population
        """
        for _ in range(n):
            A, B = random.sample(range(self.n), 2)
            self.update(transaction(self.current(), A, B))
    
    def gini(self, wealth:np.ndarray) -> float:
        """
        :param wealth: the wealth distribution of the popualation to evaluate
        :return: the Gini coefficient of the current population
        """
        total = sum([np.sum(np.abs(xi - wealth[i:])) for i, xi in enumerate(wealth[:-1], 1)])
        return total / (self.n ** 2 * np.mean(wealth))
    
    def plot_gini(self, verbose=True) -> None:
        """
        :param verbose: whether to print the verbose <DEFAULT: True>
        Description: plot the change of the Gini coefficient throughout the simulation
        """
        gini_history = []
        table = PrettyTable()
        table.field_names = ["step", "gini", "std"]
        for step in range(len(self.history)):
            gini_history.append(self.gini(self.history[step]))
            if step % (len(self.history) // 10) == 0:
                table.add_row([step, "{:.2f}".format(gini_history[-1]), "{:.2f}".format(np.std(self.history[step]))])
        if verbose: print(table.get_string())
        plt.title("The change of Gini coefficient")
        plt.xlabel("Number of exchanges")
        plt.ylabel("Gini coefficient")
        plt.plot(gini_history)
        plt.show()
    
    def plot_percentiles(self, verbose=True) -> None:
        """
        :param verbose: whether to print the verbose <DEFAULT: True>
        Description: plot the change of proportion of each percentile of the population
        - 5th percentile
        - 25th percentile (1st quartile)
        - 50th percentile (2nd quartile, median)
        - 75th percentile (3rd quartile)
        - 95th percentile
        """
        percentile_history = []
        table = PrettyTable()
        table.field_names = ["step", "5%", "25%", "50%", "75%", "95%"]
        for step in range(len(self.history)):
            percentile_history.append(np.percentile(self.history[step], [5, 25, 50, 75, 95]))
            if step % (len(self.history) // 10) == 0:
                table.add_row([step] + list(percentile_history[-1]))
        if verbose: print(table.get_string())
        plt.title("The change of wealth distribution")
        plt.xlabel("Number of exchanges")
        plt.ylabel("Wealth")
        plt.plot(percentile_history)
        plt.legend(["5th", "25th", "50th", "75th", "95th"])
        plt.show()
    
    def plot_ordered_curves(self):
        """
        Description: plot the ordered curves of the population at the beginning and in the end
        """
        plt.title("The ordered curves in the start and the end")
        plt.xlabel("Order")
        plt.ylabel("Wealth")
        plt.plot(sorted(self.initial()))
        plt.plot(sorted(self.current()))
        plt.legend(["start", "end"])
        plt.show()
    
    def plot_hist(self):
        """
        Description: plot the histogram of the distribution of wealth among the population at the beginning and in the end
        """
        plt.title("The histograms in the start and the end")
        plt.xlabel("Wealth")
        plt.ylabel("Number of people")
        plt.hist([self.initial(), self.current()], bins=30, stacked=True, alpha=0.5, histtype="bar", rwidth=0.8)
        plt.legend(["start", "end"])
        plt.show()
    
    def animate_hist(self):
        """
        Description: create an animation of the histogram of wealth distribution among the population across the whole process of simulation
        """
        fig = plt.figure()
        plt.title("The histograms in the start and the end")
        def animate(frame):
            plt.clf()
            plt.xlabel("Wealth")
            plt.ylabel("Number of people")
            plt.hist([self.history[frame]], bins=30, stacked=True, alpha=0.5, histtype="bar", rwidth=0.8)
        ani = animation.FuncAnimation(fig, animate, frames=range(len(self.history)), interval=50)
        plt.show()

class NormalPopulation(Population):

    # Overwrite initialization method
    def __init__(self, n:int, mean:float, std:float) -> None:
        """
        :param n: the size of the population to initialize
        :param mean: the mean wealth of the population to initialize
        :param std: the standard deviation of the wealth of population to initialize
        """
        self.n = n
        self.history = [np.random.normal(mean, std, n)]