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

def fit_on_previous(bias:float, layers:int):
    print("Fitting with transaction function win_take_layer, simulating 200000 steps")
    print("Testing on equal population of size=2000, mean=100.00, transaction bias={:.0%}, layers={}".format(bias, layers))
    equal_population = population.Population(2000, 100.00)
    equal_population.simulate(transaction.win_take_layer, 200000, bias, layers)
    equal_population.fit_hist(distributions=None, verbose=True, save=True)

def final_test_on_simple_tax(tax:float):
    print("Equal population, size=2000, mean=100.00, simulating 20000 steps")
    print("Exchange strategy: winner takes some proportion of wealth from the loser")
    print("                   with the loser resisting the loss of wealth at Lvl. 5")
    print("                   the richer party has 60% chance of winning")
    print("                   there is a {:.0%} tax for each exchange, later distributed among all".format(tax))
    equal_population = population.Population(2000, 100.00)
    equal_population.simulate(transaction.win_with_tax, 20000, tax, 0.6, 5)
    equal_population.plot_gini_and_percentiles(verbose=True, save=True)
    equal_population.plot_ordered_curves(save=True)
    equal_population.plot_hist(save=True)
    equal_population.animate_hist()

def final_test_on_combined_tax():
    print("Equal population, size=2000, mean=100.00, simulating 200000 steps")
    print("Exchange strategy: winner takes some proportion of wealth from the loser")
    print("                   with the loser resisting the loss of wealth at Lvl. 5")
    print("                   the richer party has 60% chance of winning")
    print("Tax policy: part of the exchange is taken and equally distributed among all")
    print("            below 0.15 times initial mean    |  3%")
    print("            0.15 to 0.50 times initial mean  |  10%")
    print("            0.50 to 1.04 times initial mean  |  20%")
    print("            1.04 to 1.96 times initial mean  |  25%")
    print("            1.96 to 2.29 times initial mean  |  30%")
    print("            2.29 to 3.33 times initial mean  |  35%")
    print("            above 3.33 times initial mean    |  45%")
    equal_population = population.Population(2000, 100.00)
    equal_population.simulate(transaction.win_mixed_tax, 200000, 100.00, 0.6, 5)
    equal_population.plot_gini_and_percentiles(verbose=True, save=True)
    equal_population.plot_ordered_curves(save=True)
    equal_population.plot_hist(save=True)
    equal_population.fit_hist(verbose=2, save=True)
    equal_population.animate_hist()

if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    "Configuration: None"
    # equal_win_take_partial(2000, 100.00, 20000)
    # uniform_win_take_partial(2000, 100.00, 20000)
    # normal_win_take_partial(2000, 100.00, 20.00, 20000)
    "Configuration: {0.8, 0.6, 0.4, 0.2, 0.0}"
    # equal_win_take_biased(2000, 100.00, 20000, 0.8)
    # uniform_win_take_biased(2000, 100.00, 20000, 0.8)
    # normal_win_take_biased(2000, 100.00, 20.00, 20000, 0.8)
    "Configuration: {0.8, 0.6, 0.4, 0.2, 0.0}, {2, 5}"
    # equal_win_take_layer(2000, 100.00, 20000, 0.8, 2)
    # uniform_win_take_layer(2000, 100.00, 20000, 0.8, 2)
    # normal_win_take_layer(2000, 100.00, 20.00, 20000, 0.8, 2)
    """
    Final tests: - fit_on_previous              {0.5, 0.6}, {1, 5}
                 - final_test_on_simple_tax     {0.03, 0.1, 0.2, 0.45}
                 - final_test_on_combined_tax   None
    """
    # fit_on_previous(0.5, 1)
    # final_test_on_simple_tax(0.03)
    # final_test_on_combined_tax()
