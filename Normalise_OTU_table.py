
# coding: utf-8

# In[6]:

import pandas as pd
import numpy

input_1 = raw_input("Enter OTU table filename: ")


otu_table = input_1
data = pd.read_csv(otu_table , sep=',', index_col=0, skiprows=[1])


# In[8]:

sum_row = data.sum()
min_sum = min(data.sum())
normalise = data / sum_row * min_sum
print(normalise)


# In[9]:

normalise.to_csv('normalised_OTU.csv', sep=',', encoding='utf-8')


# In[ ]:



