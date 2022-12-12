from transaction import population
from transaction import transaction

uniform_population = population.NormalPopulation(50, 100.00, 20.00)
uniform_population.simulate(transaction.random_give_one_dollar, 500)
uniform_population.plot_gini()
uniform_population.plot_percentiles()
uniform_population.plot_ordered_curves()
uniform_population.plot_hist()
# uniform_population.animate_hist()