import pandas as pd

def sum_row(matrix, row_index):

    # Simple function to calculate the sum of numbers in a given row of a Pandas DataFrame using iloc.

    return matrix.iloc[row_index].sum()
