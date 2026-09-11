import pandas as pd
import numpy as np
print("hello world")

values = [[1, '2023-01-01 10:00:00', 'Area A', 5],
           [2, '2023-01-01 10:00:00', 'Area A', 5], 
           [3, '2023-01-01 10:00:00', 'Area A', 5], 
           [4, '2023-01-01 10:00:00', 'Area A', 5],
           [5, '2023-01-01 10:00:00', 'Area A', 5],
             [6, '2023-01-01 10:00:00', 'Area A', 5], 
             [7, '2023-01-01 10:00:00', 'Area A', 5], 
             [8, '2023-01-01 10:00:00', 'Area A', 5], 
             [9, '2023-01-01 10:00:00', 'Area A', 5],
             [10, '2023-01-01 10:00:00', 'Area A', 5]]

df = pd.DataFrame(values,columns=['Id', 'Time', 'Area', 'item_count'])


print(df.head())