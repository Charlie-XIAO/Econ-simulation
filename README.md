# Simulation of the Inequality Process

> Modeling and Simulation in Science, Engineering, and Economics | Courant Institute of Mathematical Sciences | New York University

## Introduction

We are interested in how the wealth is distributed across the society. We simulate this using the random transaction of the surpluses of two random individuals, with some certains restrictions. Various different transaction functions are applied, following the Surplus Theory [1] and corresponding to different stages in the evolution of the society.

In this project, we use different distributions for the initial wealth of the population (namely equally-distributed, uniformly-distributed, and normally-distributed initial wealth) and different transaction functions (namely `win_take_partial`, `win_take_biased`, and `win_take_layer`). Also, with a chosen set of parameters according to the experiments with the previous distributions and functions, we implement `win_with_tax` and `win_mixed_tax` to simulate a modern society.

Various kinds of graphs and animations are provided for observing the pattern of the wealth distribution across the society:

- Printout about the change of Gini coefficient, the standard deviation of wealth, and different percentiles during the simulation.

- Plot of the change of Gini coefficient during the simulation.

- Plot of different percentiles and their changes during the simulation.

- Plot of the ordered curves during the simulation, demonstrating the change of wealth at different rankings during the simulation.

- Plot of the initial historgam versus the histogram at the end of the simulation.

- Animation of the change of histogram during the simulation.

- The distribution fitting of the *normalized* histogram at the end of the simulation. Note that the distributions come from `scipy.stats`, and the top 20 distributions that fit the normalized histogram best will be shown, along with a printout of their fitting errors.

## Requirements

1. Clone the Github repository to your local device.

2. Create a Python virtual environment on your local device.

3. Activate that virtual environment, and install the required modules for this repository. You can do the follwing:
```
pip3 install -r requirement.txt
```

4. Go to `src/`, select some test from `test.py`, and run `test.py`. Due to the limitation of time for this project, we did not implement a user-friendly testing module. You may have to read the test functions in `test.py` to see how to use the `Population` class from `population.py` and the transaction functions from `transaction.py`.

## Results

The video demonstration of our results and some distribution fitting plots can be found [here](https://charlie-xiao.github.io/pure/inequality-process-simulation-demonstration.html). The techinal report, presentation slides, and other resources of our project can be found under `Paper/`.

## References

Thanks for Professor [*Charles S. Peskin*](https://www.math.nyu.edu/~peskin/)'s tutoring and [notes](https://www.math.nyu.edu/~peskin/modsim_lecture_notes/index.html). Also thanks Teaching Assistant [Mengjian Hua](mailto:mh5113@nyu.edu) for his suggestion on this project.

[1] John Angle. The Surplus Theory of Social Stratification and the Size Distribution of Personal Wealth. *Social Forces*, 65(2): 293-326, 1986
