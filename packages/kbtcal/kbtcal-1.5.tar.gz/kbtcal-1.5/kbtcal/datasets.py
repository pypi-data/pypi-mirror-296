import numpy as np

# Dataset
raw_data = np.array( [[12, 2, 5],
                  [16, 4, 4],
                  [18.5, 5, 5],
                  [20.8, 6, 2],
                  [23.1, 7, 3],
                  [26, 8, 5],
                  [30, 9, 4],
                  [32, 10, 4],
                  [40, 15, 6],
                  [47.3, 20, 7]])

data = np.array( [[12, 2],
                  [16, 4],
                  [18.5, 5],
                  [20.8, 6],
                  [23.1, 7],
                  [26, 8],
                  [30, 9],
                  [32, 10],
                  [40, 15],
                  [47.3, 20]])

target = np.array([1, 0, 0, 1, 1, 1, 0, 1, 0, 0])

target_names = np.array(['Female', 'Male'])

feature_names = ['Weight', 'Age', 'Height',]

DESCR = 'This is a dummy data used for training and demonstration purposes'

def load_cpen():
    dummy_data = {
            'data': raw_data,
            'target': target,
            'target_names': target_names,
            'DESCR': DESCR,
            'feature_names': feature_names     
            }
    return dummy_data

def load_fpen():
    dummy_data = {
            'data': data,
            }
    return dummy_data
