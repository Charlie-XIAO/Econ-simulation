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

def win_take_biased(population:np.ndarray, A:int, B:int, bias:float) -> np.ndarray:
    """
    :param population: the population in which the transaction takes place
    :param A: the index of one person in the population to make transaction
    :param B: the index of the other person in the population to make transaction
    :param bias: the bias towards the richer party in the transaction, should be in [0, 1]
    :return: the new population after (if exists) the transaction
    Description:
    - One of A and B will be chosen as the winner (receiving wealth) and the other as the loser (giving wealth)
    - The wealth of transaction is determined by a 0,1 continuous uniform random variate on the total wealth of the loser
    - However, in the reality, the richer and the poorer parties, most of the times, does not have equal probability to win or lose
    - With 0.0 < bias < 0.5, the poorer party is more likely to win the wealth
    - With 0.5 < bias < 1.0, the richer party is more likely to win the wealth
    - With bias = 0.5, this transaction function is the same as `win_take_partial(population, A, B)`
    - With bias = 1.0, the poorer party will definitely lose the wealth
    - With bias = 0.0, the poorer party will definitely win the wealth
    """
    assert(bias >= 0 and bias <= 1)
    result = np.copy(population)
    ratio = np.random.uniform(0, 1)
    if population[A] > population[B]:
        richer, poorer = A, B
    else:
        richer, poorer = B, A
    if bias == 1:
        result[richer] = population[richer] + ratio * population[poorer]
        result[poorer] = population[poorer] - ratio * population[poorer]
    elif bias == 0:
        result[poorer] = population[poorer] + ratio * population[richer]
        result[richer] = population[richer] - ratio * population[richer]
    elif random.random() < bias:
        result[richer] = population[richer] + ratio * population[poorer]
        result[poorer] = population[poorer] - ratio * population[poorer]
    else:
        result[poorer] = population[poorer] + ratio * population[richer]
        result[richer] = population[richer] - ratio * population[richer]
    return result

def win_take_layer(population:np.ndarray, A:int, B:int, bias:float, layers:int) -> np.ndarray:
    """
    :param population: the population in which the transaction takes place
    :param A: the index of one person in the population to make transaction
    :param B: the index of the other person in the population to make transaction
    :param bias: the bias towards the richer party in the transaction, should be in [0, 1]
    :param layers: the layers 
    :return: the new population after (if exists) the transaction
    Description:
    - One of A and B will be chosen as the winner (receiving wealth) and the other as the loser (giving wealth)
    - The wealth of transaction is determined by n 0,1 continuous uniform random variates, each representing a layer
    - The random variates are combined as L = sum_{k=1}^{n} U_k^k / n, so that the top layers are more fugitive
    - The larger the number of layers, the smaller the expected loss of the loser, thus stronger resistance
    - Also, in the reality, the richer and the poorer parties, most of the times, does not have equal probability to win or lose
    - With 0.0 < bias < 0.5, the poorer party is more likely to win the wealth
    - With 0.5 < bias < 1.0, the richer party is more likely to win the wealth
    - With bias = 0.5, this transaction function is the same as `win_take_partial(population, A, B)`
    - With bias = 1.0, the poorer party will definitely lose the wealth
    - With bias = 0.0, the poorer party will definitely win the wealth
    """
    result = np.copy(population)
    ratio = np.sum(np.square(np.random.uniform(0, 1, layers)) / layers)
    if population[A] > population[B]:
        richer, poorer = A, B
    else:
        richer, poorer = B, A
    if bias == 1:
        result[richer] = population[richer] + ratio * population[poorer]
        result[poorer] = population[poorer] - ratio * population[poorer]
    elif bias == 0:
        result[poorer] = population[poorer] + ratio * population[richer]
        result[richer] = population[richer] - ratio * population[richer]
    elif random.random() < bias:
        result[richer] = population[richer] + ratio * population[poorer]
        result[poorer] = population[poorer] - ratio * population[poorer]
    else:
        result[poorer] = population[poorer] + ratio * population[richer]
        result[richer] = population[richer] - ratio * population[richer]
    return result


