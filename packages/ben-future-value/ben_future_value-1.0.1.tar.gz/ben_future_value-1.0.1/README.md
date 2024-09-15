# Project Description

[Link_To_Wiki](https://github.com/Ben-Payton/ben_future_value/wiki)

This is a package for calculating future values and debt payoff in python.
Generally this is a small package so people can learn how to install and use packages. 
It is meant to pair well with [matplotlib](https://matplotlib.org/) and [seaborn](https://seaborn.pydata.org/) they are listed as dependancies to ensure they are installed.


# How to install and use

In the command line type:

`pip install ben-future-value`

Once installed then use by importing at the top of your python code.

Below is an example of how you might generate a graph to compare outcomes of different interest rates.

```python
# Here we import packages, the first one is for making graphs
# the second one allows us to calculate our future values
# The third one allows us to make our graphs a little prettier with less code. 
import matplotlib.pyplot as plt
import ben_future_value as bfv
import seaborn as sns

#These next lines makes our graph pretty later. You don't need them.
sns.set_context("notebook")
sns.set_style("darkgrid")


# These variables are for convenience of editing later.
NUMBER_OF_YEARS = 25
MATCHES_PER_YEAR = 4
PRINCIPLE_VALUE = 1000.00
AMMOUNT_CONTRIBUTED_PER_MATCH = 100.00

PERCENT_INCREASE_ONE = 5.0
PERCENT_INCREASE_TWO = 8.5
PERCENT_INCREASE_THREE = 12.0


# Here we use the ben_future_value package to calculate future values
high_yield_savings = bfv.Future_Value(
    PRINCIPLE_VALUE,
    PERCENT_INCREASE_ONE,
    AMMOUNT_CONTRIBUTED_PER_MATCH,
    NUMBER_OF_YEARS,
    MATCHES_PER_YEAR
)

low_interest_investment = bfv.Future_Value(
    PRINCIPLE_VALUE,
    PERCENT_INCREASE_TWO,
    AMMOUNT_CONTRIBUTED_PER_MATCH,
    NUMBER_OF_YEARS,
    MATCHES_PER_YEAR
)

average_interest_investment = bfv.Future_Value(
    PRINCIPLE_VALUE,
    PERCENT_INCREASE_THREE,
    AMMOUNT_CONTRIBUTED_PER_MATCH,
    NUMBER_OF_YEARS,
    MATCHES_PER_YEAR
)


# Next we plot our future values
plt.plot(high_yield_savings.get_future_values())
plt.plot(low_interest_investment.get_future_values())
plt.plot(average_interest_investment.get_future_values())

plt.legend(
    [
        "High Yield Savings (" + str(PERCENT_INCREASE_ONE) + "%)",
        "Low Interest Investment (" + str(PERCENT_INCREASE_TWO) + "%)",
        "Average Interest Investment (" + str(PERCENT_INCREASE_THREE) + "%)"
    ]
)

# These next two lines add axis titles
plt.xlabel("Number of Matches")
plt.ylabel("Dollar Value")
# This shows out graph when we run out code
plt.show()
```
![figure](https://github.com/Ben-Payton/ben_future_value/blob/main/fig/Interest_value_example_plot.png?raw=true)
