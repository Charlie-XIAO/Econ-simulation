import random
import numpy as np

def random_give_one_dollar(population:np.ndarray, A:int, B:int) -> np.ndarray:
    """
    :param population: the population in which the transaction takes place
    :param A: the index of one person in the population to make transaction
    :param B: the index of the other person in the population to make transaction
    :return: the new population after (if exists) the transaction
    Description:
    - If both A and B have no wealth, then no transaction will be made
    - If one of A and B has no wealth, then the one who has wealth will give one dollar to the other
    - If both A and B have wealth, then the one to give one dollar will be randomly chosen (equal chance)
    """
    result = np.copy(population)
    if result[A] != 0 and result[B] != 0:
        if random.random() < 0.5:
            result[A] += 1
            result[B] -= 1
        else:
            result[A] -= 1
            result[B] += 1
    elif result[A] != 0:
        result[A] -= 1
        result[B] += 1
    elif result[B] != 0:
        result[B] -= 1
        result[A] += 1
    return result