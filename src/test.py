from transaction import population
from transaction import transaction

uniform_population = population.Population(100, 100.00)
uniform_population.simulate(transaction.win_take_partial, 5000)
uniform_population.plot_gini(verbose=True, save=True)
uniform_population.plot_percentiles(verbose=True, save=True)
uniform_population.plot_ordered_curves(save=True)
uniform_population.plot_hist(save=True)
uniform_population.animate_hist()