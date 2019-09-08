import numpy as np

search_criteria = {'strategy': "RandomDiscrete", 'max_models': 50}
hyper_p_gbm = {'sample_rate': [0.7, 0.8, 0.9],
                'ntrees': list(np.arange(100, 1000, 100)),
                'stopping_metric': ['mse', 'rmse', 'mae'],
                'seed': [1234, 1000, 800],
                'max_depth': [5, 8, 10],
                'min_rows': [5, 10 , 15, 20],
                'nbins': [5, 10 , 15, 20],
                'learn_rate': [0.01, 0.02, 0.03, 0.04, 0.05]
              }
hyper_p_drf = {'ntrees': list(np.arange(50, 500, 50)),
               'max_depth': [3, 5, 7, 15, 20],
               'min_rows': [5, 10 , 12],
              }
hyper_p_dnn = {'activation': ['tanh', 'rectifier', 'maxout'],
                'hidden': [[10], [10, 10], [50], [50,50], [50,50,50]],
                'l1': [0, 1e-3, 1e-5],
                'l2': [0, 1e-3, 1e-5],
               'epochs': [20, 50, 100, 200]
              }
hyper_p_glm = hyper_params = {'lambda': [0.5, 0.5, 1.0, 1.2, 1.5],
                              'alpha': [0.01, 0.05, 0.5]
                             }
split_ratio = 0.8

model_features = {'CPC': {'num': None , 'cat': None},
                  'CTR': {'num': None , 'cat': None},
                  'reach': {'num': None , 'cat': None}
                  }
model_save_path = './'