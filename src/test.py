from transaction import population
from transaction import transaction

from datetime import datetime

def equal_win_take_partial(n:int, mean:float, steps:int) -> None:
    print("Equal population, size={}, mean={}, simulating {} steps".format(n, mean, steps))
    print("Exchange strategy: winner takes random proportion of wealth from the loser")
    equal_population = population.Population(n, mean)
    equal_population.simulate(transaction.win_take_partial, steps)
    equal_population.plot_gini_and_percentiles(verbose=True, save=True)
    equal_population.plot_ordered_curves(save=True)
    equal_population.plot_hist(save=True)
    equal_population.animate_hist()

def uniform_win_take_partial(n:int, mean:float, steps:int) -> None:
    print("Uniform population, size={}, mean={}, simulating {} steps".format(n, mean, steps))
    print("Exchange strategy: winner takes random proportion of wealth from the loser")
    uniform_population = population.UniformPopulation(n, mean)
    uniform_population.simulate(transaction.win_take_partial, steps)
    uniform_population.plot_gini_and_percentiles(verbose=True, save=True)
    uniform_population.plot_ordered_curves(save=True)
    uniform_population.plot_hist(save=True)
    uniform_population.animate_hist()

def normal_win_take_partial(n:int, mean:float, std:float, steps:int) -> None:
    print("Normal population, size={}, mean={}, std={}, simulating {} steps".format(n, mean, steps, std))
    print("Exchange strategy: winner takes random proportion of wealth from the loser")
    normal_population = population.NormalPopulation(n, mean, std)
    normal_population.simulate(transaction.win_take_partial, steps)
    normal_population.plot_gini_and_percentiles(verbose=True, save=True)
    normal_population.plot_ordered_curves(save=True)
    normal_population.plot_hist(save=True)
    normal_population.animate_hist()

def equal_win_take_biased(n:int, mean:float, steps:int, bias:float) -> None:
    print("Equal population, size={}, mean={}, simulating {} steps".format(n, mean, steps))
    print("Exchange strategy: winner takes random proportion of wealth from the loser")
    print("                   however, the richer party has {:.0%} chance of winning".format(bias))
    equal_population = population.Population(n, mean)
    equal_population.simulate(transaction.win_take_biased, steps, bias)
    equal_population.plot_gini_and_percentiles(verbose=True, save=True)
    equal_population.plot_ordered_curves(save=True)
    equal_population.plot_hist(save=True)
    equal_population.animate_hist()

def uniform_win_take_biased(n:int, mean:float, steps:int, bias:float) -> None:
    print("Uniform population, size={}, mean={}, simulating {} steps".format(n, mean, steps))
    print("Exchange strategy: winner takes random proportion of wealth from the loser")
    print("                   however, the richer party has {:.0%} chance of winning".format(bias))
    uniform_population = population.UniformPopulation(n, mean)
    uniform_population.simulate(transaction.win_take_biased, steps, bias)
    uniform_population.plot_gini_and_percentiles(verbose=True, save=True)
    uniform_population.plot_ordered_curves(save=True)
    uniform_population.plot_hist(save=True)
    uniform_population.animate_hist()

def normal_win_take_biased(n:int, mean:float, std:float, steps:int, bias:float) -> None:
    print("Normal population, size={}, mean={}, std={}, simulating {} steps".format(n, mean, std, steps))
    print("Exchange strategy: winner takes random proportion of wealth from the loser")
    print("                   however, the richer party has {:.0%} chance of winning".format(bias))
    normal_population = population.NormalPopulation(n, mean, std)
    normal_population.simulate(transaction.win_take_biased, steps, bias)
    normal_population.plot_gini_and_percentiles(verbose=True, save=True)
    normal_population.plot_ordered_curves(save=True)
    normal_population.plot_hist(save=True)
    normal_population.animate_hist()

def equal_win_take_layer(n:int, mean:float, steps:int, bias:float, layers:int) -> None:
    print("Equal population, size={}, mean={}, simulating {} steps".format(n, mean, steps))
    print("Exchange strategy: winner takes some proportion of wealth from the loser")
    print("                   with the loser resisting the loss of wealth at Lvl. {}".format(layers))
    print("                   the richer party has {:.0%} chance of winning".format(bias))
    equal_population = population.Population(n, mean)
    equal_population.simulate(transaction.win_take_layer, steps, bias, layers)
    equal_population.plot_gini_and_percentiles(verbose=True, save=True)
    equal_population.plot_ordered_curves(save=True)
    equal_population.plot_hist(save=True)
    equal_population.animate_hist()

def uniform_win_take_layer(n:int, mean:float, steps:int, bias:float, layers:int) -> None:
    print("Uniform population, size={}, mean={}, simulating {} steps".format(n, mean, steps))
    print("Exchange strategy: winner takes some proportion of wealth from the loser")
    print("                   with the loser resisting the loss of wealth at Lvl. {}".format(layers))
    print("                   the richer party has {:.0%} chance of winning".format(bias))
    uniform_population = population.UniformPopulation(n, mean)
    uniform_population.simulate(transaction.win_take_layer, steps, bias, layers)
    uniform_population.plot_gini_and_percentiles(verbose=True, save=True)
    uniform_population.plot_ordered_curves(save=True)
    uniform_population.plot_hist(save=True)
    uniform_population.animate_hist()

def normal_win_take_layer(n:int, mean:float, std:float, steps:int, bias:float, layers:int) -> None:
    print("Normal population, size={}, mean={}, std={}, simulating {} steps".format(n, mean, std, steps))
    print("Exchange strategy: winner takes some proportion of wealth from the loser")
    print("                   with the loser resisting the loss of wealth at Lvl. {}".format(layers))
    print("                   the richer party has {:.0%} chance of winning".format(bias))
    normal_population = population.NormalPopulation(n, mean, std)
    normal_population.simulate(transaction.win_take_layer, steps, bias, layers)
    normal_population.plot_gini_and_percentiles(verbose=True, save=True)
    normal_population.plot_ordered_curves(save=True)
    normal_population.plot_hist(save=True)
    normal_population.animate_hist()

if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # equal_win_take_partial(2000, 100.00, 20000)
    # uniform_win_take_partial(2000, 100.00, 20000)
    # normal_win_take_partial(2000, 100.00, 20.00, 20000)
    # equal_win_take_biased(2000, 100.00, 20000, 0.8)
    # uniform_win_take_biased(2000, 100.00, 20000, 0.8)
    # normal_win_take_biased(2000, 100.00, 20.00, 20000, 0.0)
    # equal_win_take_layer(2000, 100.00, 20000, 0.8, 5)
    # uniform_win_take_layer(2000, 100.00, 20000, 0.8, 5)
    # normal_win_take_layer(2000, 100.00, 20.00, 20000, 0.8, 5)