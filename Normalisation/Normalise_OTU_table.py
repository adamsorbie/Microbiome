
import pandas as pd
import numpy

def normalise_otu(otu): 
    sum_row = pd.otu.sum()
    min_sum = pd.otu.min(pd.otu.sum())
    normalise = otu / sum_row * min_sum
    return normalise









