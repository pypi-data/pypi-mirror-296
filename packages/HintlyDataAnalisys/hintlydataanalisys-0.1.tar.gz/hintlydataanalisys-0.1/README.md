# HintlyDataAnalysis – Mathematical and Financial Library
# Spis treści
- [Description](#description)
- [Usage](#usage)
  - [Math](#calculate-mean)
  - [Finance](#financial-angles)
- [API](#api)
  - [Math](#math)
  - [Finance](#finance)
- [Authors](#authors)
- [License](#license)
## Description

HintlyDataAnalysis is a Python library that provides tools for mathematical and financial analysis. It offers functions for calculating means, percentage differences, data normalization, weighted averages, number repetition, financial angles, and financial chances.
Installation

You can install the library using pip:

    pip install HintlyAnalisysData

## Usage

After installation, you can import modules from the library and use the available functions.
Example Usage

    from HintlyAnalisysData.DataAnalisys import Math, Finance

### Calculate mean
    mean_value = Math.Mean([1, 2, 3, 4])

### Calculate percentage difference
    percent_diff = Math.Difference(100, 120)

### Normalize data
    normalized_data = Math.Normalize([10, 15, 20], 100)

### Weighted average
    weighted_avg = Math.WeightedAverage([10, 20, 30], [1, 2, 3])

### Number repetition
    num_repeats = Math.NumberRepeat([1, 2, 2, 3, 3, 3])

### Financial angles
    angles = Finance.FinancialAngle([100, 120, 80], 50)

### Financial chance
    chance = Finance.FinanceChance([1, 2, 2, 3, 3, 3])
###
    print(mean_value, percent_diff, normalized_data, weighted_avg, num_repeats, angles, chance)

# API
## Math

### Math.Mean(analisysData: list)

Calculates the arithmetic mean of a list of data.

Parameters:
        analisysData (list): List of numbers.

    Returns:
        The mean value of the data.

### Math.Difference(a: float, b: float)

Calculates the percentage difference between two numbers.

    Parameters:
        a (float): Base number.
        b (float): Number to compare.
    Returns:
        Percentage difference between a and b.

### Math.Normalize(analisysData: list, normalizeNumber: int)

Normalizes the values in the list relative to the largest value, scaling them to normalizeNumber.

    Parameters:
        analisysData (list): List of numbers to normalize.
        normalizeNumber (int): Target normalization value.
    Returns:
        List of normalized data.

### Math.WeightedAverage(analisysData: list, weights: list)

Calculates the weighted average of the data and corresponding weights.

    Parameters:
        analisysData (list): List of numerical data.
        weights (list): List of weights assigned to the data.
    Returns:
        The weighted average.

### Math.NumberRepeat(numbers: list)

Returns a dictionary with the count of occurrences of each number in the list.

    Parameters:
        numbers (list): List of numbers to analyze.
    Returns:
        A dictionary with counts of occurrences for each number.

## Finance

### Finance.FinancialAngle(amounts: list, max_change: int)

Calculates the financial angle (in degrees) based on changes in amounts.

    Parameters:
        amounts (list): List of amounts.
        max_change (int): Maximum possible change in the data.
    Returns:
        List of angles in degrees (0–180).

### Finance.FinanceChance(numbers: list)

Calculates the chances (in percentage) of each number occurring in the list.

    Parameters:
        numbers (list): List of numbers to analyze.
    Returns:
        A dictionary with percentage chances for each number.

## Authors

#### Franciszek Chmielewski (ferko2610@gmail.com)

## License

The project is licensed under the MIT License. Details can be found in the LICENSE file.
### Version History

    0.1 – Initial release.

### Future Plans

1. Add more advanced analytical tools.
2. Expand support for financial analysis.