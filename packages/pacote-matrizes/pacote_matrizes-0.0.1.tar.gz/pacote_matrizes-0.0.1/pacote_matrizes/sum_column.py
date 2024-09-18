import pandas as pd

def sum_column(matrix, column_index):
    
    # Simple function to calculate the sum of numbers in a given column of a Pandas DataFrame.

    return matrix.iloc[:, column_index].sum()
