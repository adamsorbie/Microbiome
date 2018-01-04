


import pandas as pd
import numpy

input_file = input("Enter OTU table filename: ")
input_selection = input("0 = Normalization, 1 = Relative Abundance: ")

otu_table = input_file
data = pd.read_csv(otu_table , sep=',', index_col=0, skiprows=[1])


if input_selection == "0":
    sum_row = data.sum()
    min_sum = min(data.sum())
    normalise = data / sum_row * min_sum
    normalise.to_csv('normalised_OTU.csv', sep=',', encoding='utf-8')

elif input_selection == "1":
    sum_row = otu.sum()
    min_sum = min(otu.sum())
    rel_abund = otu * 100 / sum_row
    rel_abund.to_csv('relative_abundance.csv', sep=',', encoding='utf-8')





