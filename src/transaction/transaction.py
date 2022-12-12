import random
import numpy as np

def win_take_partial(population:np.ndarray, A:int, B:int) -> np.ndarray:
    """
    :param population: the population in which the transaction takes place
    :param A: the index of one person in the population to make transaction
    :param B: the index of the other person in the population to make transaction
    :return: the new population after (if exists) the transaction
    Description:
    - One of A and B will be chosen as the winner (receiving wealth) and the other as the loser (giving wealth)
    - The wealth of transaction is determined by a 0,1 continuous uniform random variate on the total wealth of the loser
    """
    result = np.copy(population)
    ratio = np.random.uniform(0, 1)
    if random.random() < 0.5:
        result[A] = population[A] + ratio * population[B]
        result[B] = population[B] - ratio * population[B]
    else:
        result[B] = population[B] + ratio * population[A]
        result[A] = population[A] - ratio * population[A]
    return result
