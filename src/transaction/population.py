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

    def simulate(self, transaction, n:int, *args) -> None:
        """
        :param function: the transaction function to use in the simulation
        :param n: the total number of transactions to simulate
        Description: simulate the specified type of transaction for n times in the population
        """
        for _ in range(n):
            A, B = random.sample(range(self.n), 2)
            self.update(transaction(self.current(), A, B, *args))
    
    def gini(self, wealth:np.ndarray) -> float:
        """
        :param wealth: the wealth distribution of the popualation to evaluate
        :return: the Gini coefficient of the current population
        """
        total = sum([np.sum(np.abs(xi - wealth[i:])) for i, xi in enumerate(wealth[:-1], 1)])
        return total / (self.n ** 2 * np.mean(wealth))
    
    def plot_gini_and_percentiles(self, verbose=True, save=True) -> None:
        """
        :param verbose: whether to print the verbose <DEFAULT: True>
        :param save: whether to save the plots <DEFAULT: True>
        Description: plot the change of the Gini coefficient and of each percentile (of interest) throughout the simulation
        """
        # Creating the verbose output table
        gini_history = []
        percentile_history = []
        table = PrettyTable()
        table.field_names = ["step", "gini", "std", "1%", "5%", "25%", "50%", "75%", "95%", "99%"]
        for step in range(len(self.history)):
            gini_history.append(self.gini(self.history[step]))
            percentile_history.append(np.percentile(self.history[step], [1, 5, 25, 50, 75, 95, 99]))
            if step % (max(len(self.history) // 10, 1)) == 0:
                new_row = [step, "{:.2f}".format(gini_history[-1]), "{:.2f}".format(np.std(self.history[step]))]
                for i in range(7):
                    new_row.append(int(percentile_history[-1][i]))
                table.add_row(new_row)
        if verbose: print(table.get_string())
        # Plotting the change of the Gini coefficient
        plt.title("The change of Gini coefficient")
        plt.xlabel("Number of exchanges")
        plt.ylabel("Gini coefficient")
        plt.plot(gini_history)
        if save: plt.savefig("plot_gini.png")
        plt.show()
        # Plotting the change of the wealth distribution (by percentiles)
        plt.title("The change of wealth distribution")
        plt.xlabel("Number of exchanges")
        plt.ylabel("Wealth")
        plt.plot(percentile_history)
        plt.legend(["1st", "5th", "25th", "50th", "75th", "95th", "99th"], loc="upper right")
        if save: plt.savefig("plot_percentiles.png")
        plt.show()
    
    def plot_ordered_curves(self, save=True):
        """
        :param save: whether to save the plot <DEFAULT: True>
        Description: plot the ordered curves of the population at the beginning and in the end
        """
        plt.title("The ordered curves in the start and the end")
        plt.xlabel("Order")
        plt.ylabel("Wealth")
        plt.plot(sorted(self.initial()))
        plt.plot(sorted(self.current()))
        plt.legend(["start", "end"], loc="upper right")
        if save: plt.savefig("plot_ordered_curves.png")
        plt.show()
    
    def plot_hist(self, save=True):
        """
        :param save: whether to save the plot <DEFAULT: True>
        Description: plot the histogram of the distribution of wealth among the population at the beginning and in the end
        """
        plt.title("The histograms in the start and the end")
        plt.xlabel("Wealth")
        plt.ylabel("Number of people")
        plt.hist([self.initial(), self.current()], bins=30, alpha=0.5, histtype="bar", rwidth=0.8)
        plt.legend(["start", "end"], loc="upper right")
        if save: plt.savefig("plot_hist.png")
        plt.show()
    
    def animate_hist(self):
        """
        Description: create an animation of the histogram of wealth distribution among the population across the whole process of simulation,
                     and save it as an html file containing the video of the animation. Note that we limit this to only 500 frames,
                     uniformly selected from the number of transaction processes, for the sake of computational complexity.
        """
        fig = plt.figure()
        def animate(frame):
            plt.clf()
            plt.title("The histogram at Transaction {}".format(frame))
            plt.xlabel("Wealth")
            plt.ylabel("Number of people")
            plt.hist([self.initial(), self.history[frame]], bins=30, alpha=0.5, histtype="bar", rwidth=0.8)
        anim = animation.FuncAnimation(fig, animate, frames=range(0, len(self.history), max(1, len(self.history) // 500)), interval=50, repeat=False)
        video = anim.to_html5_video()
        html = display.HTML(video)
        with open("anim_hist.html", "w") as file:
            file.write(html.data)
        plt.close()

class UniformPopulation(Population):

    # Overwrite initialization method
    def __init__(self, n: int, mean: float) -> None:
        """
        :param n: the size of the population to initialize
        :param mean: the mean wealth of the population to initialize
        """
        self.n = n
        sample = np.random.uniform(0, 200, n)
        factor = n * mean / np.sum(sample)
        self.history = [sample * factor]

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