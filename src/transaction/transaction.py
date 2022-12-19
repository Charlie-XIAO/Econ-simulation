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
    :param layers: the number of layers that forces a resistance to loss from the loser
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

def win_with_tax(population:np.ndarray, A:int, B:int, tax:float, bias=0.6, layers=5):
    """
    :param population: the population in which the transaction takes place
    :param A: the index of one person in the population to make transaction
    :param B: the index of the other person in the population to make transaction
    :param tax: the porportion of tax taken from each transaction, and later distributed across the total population
    :param bias: the bias towards the richer party in the transaction, should be in [0, 1] <DEFAULT: 0.6>
    :param layers: the number of layers that forces a resistance to loss from the loser
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
    - Note that this transaction function involves a tax that take a proportion of wealth from the transaction
    - The tax taken in each transaction is later distributed across the total population
    """
    result = np.copy(population)
    ratio = np.sum(np.square(np.random.uniform(0, 1, layers)) / layers)
    if population[A] > population[B]:
        richer, poorer = A, B
    else:
        richer, poorer = B, A
    if bias == 1:
        exchange_amount = ratio * population[poorer]
        result += exchange_amount * tax / len(population)
        result[richer] = population[richer] + exchange_amount * (1 - tax)
        result[poorer] = population[poorer] - exchange_amount
    elif bias == 0:
        exchange_amount = ratio * population[richer]
        result += exchange_amount * tax / len(population)
        result[poorer] = population[poorer] + exchange_amount * (1 - tax)
        result[richer] = population[richer] - exchange_amount
    elif random.random() < bias:
        exchange_amount = ratio * population[poorer]
        result += exchange_amount * tax / len(population)
        result[richer] = population[richer] + exchange_amount * (1 - tax)
        result[poorer] = population[poorer] - exchange_amount
    else:
        exchange_amount = ratio * population[richer]
        result += exchange_amount * tax / len(population)
        result[poorer] = population[poorer] + exchange_amount * (1 - tax)
        result[richer] = population[richer] - exchange_amount
    return result

def win_mixed_tax(population:np.ndarray, A:int, B:int, init_mean:float, bias=0.6, layers=5):
    """
    :param population: the population in which the transaction takes place
    :param A: the index of one person in the population to make transaction
    :param B: the index of the other person in the population to make transaction
    :param init_mean: the mean of the initial wealth distribution, used for calculating the boundaries of different levels of tax
    :param bias: the bias towards the richer party in the transaction, should be in [0, 1] <DEFAULT: 0.6>
    :param layers: the number of layers that forces a resistance to loss from the loser
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
    - Note that this transaction function involves a tax that take a proportion of wealth from the transaction
    - The tax taken in each transaction is later distributed across the total population
    - The simulated tax policy refers to the law of People's Republic of China on the taxes on personal income
    - For more information, see https://taxsummaries.pwc.com/peoples-republic-of-china/individual/taxes-on-personal-income
    """
    result = np.copy(population)
    ratio = np.sum(np.square(np.random.uniform(0, 1, layers)) / layers)
    if population[A] > population[B]:
        richer, poorer = A, B
    else:
        richer, poorer = B, A
    if bias == 1:
        exchange_amount = ratio * population[poorer]
        tax = _mixed_tax_helper(exchange_amount, init_mean)
        result += tax / len(population)
        result[richer] = population[richer] + exchange_amount - tax
        result[poorer] = population[poorer] - exchange_amount
    elif bias == 0:
        exchange_amount = ratio * population[richer]
        tax = _mixed_tax_helper(exchange_amount, init_mean)
        result += tax / len(population)
        result[poorer] = population[poorer] + exchange_amount - tax
        result[richer] = population[richer] - exchange_amount
    elif random.random() < bias:
        exchange_amount = ratio * population[poorer]
        tax = _mixed_tax_helper(exchange_amount, init_mean)
        result += tax / len(population)
        result[richer] = population[richer] + exchange_amount - tax
        result[poorer] = population[poorer] - exchange_amount
    else:
        exchange_amount = ratio * population[richer]
        tax = _mixed_tax_helper(exchange_amount, init_mean)
        result += tax / len(population)
        result[poorer] = population[poorer] + exchange_amount - tax
        result[richer] = population[richer] - exchange_amount
    return result

def _mixed_tax_helper(exchange_amount:float, mean:float) -> float:
    """
    :param exchange_amount: the determined exchange amount in the transaction
    :param mean: the mean of the initial wealth distribution, used for calculating the boundaries of different levels of tax
    :return: the amount of tax extracted from the transaction according to the mixed tax policy
    Description:
    - This is the helper function for `win_mixed_tax`, which should not be called outside of `transaction.py`
    - The simulated tax policy refers to the law of People's Republic of China on the taxes on personal income
    - For more information, see https://taxsummaries.pwc.com/peoples-republic-of-china/individual/taxes-on-personal-income
    """
    tax, rest = 0.0, exchange_amount
    if exchange_amount <= 0.15 * mean:
        tax += rest * 0.03
    else:
        tax += 0.15 * mean * 0.03
        rest -= 0.15 * mean
        if exchange_amount <= 0.5 * mean:
            tax += rest * 0.1
        else:
            tax += 0.35 * mean * 0.1
            rest -= 0.35 * mean
            if exchange_amount <= 1.04 * mean:
                tax += rest * 0.2
            else:
                tax += 0.54 * mean * 0.2
                rest -= 0.54 * mean
                if exchange_amount <= 1.96 * mean:
                    tax += rest * 0.25
                else:
                    tax += 0.92 * mean * 0.25
                    rest -= 0.92 * mean
                    if exchange_amount <= 2.29 * mean:
                        tax += rest * 0.3
                    else:
                        tax += 0.33 * mean * 0.3
                        rest -= 0.33 * mean
                        if exchange_amount <= 3.33 * mean:
                            tax += rest * 0.35
                        else:
                            tax += 1.04 * mean * 0.35
                            rest -= 1.04 * mean
                            tax += rest * 0.45
    return tax
