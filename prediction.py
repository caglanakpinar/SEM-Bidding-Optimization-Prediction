import pandas as pd
import numpy as np
import itertools
import warnings
import h2o
import datetime

def get_num_cols_quartiles(values):
    return [min(values), np.percentile(values, 0.25), np.percentile(values, 0.5), np.percentile(values, 0.75), max(values)]

def combination_data_preparation(data, paramters):
    comb = []
    filters = {}
    for i in paramters['comb_cat_columns']:
        comb.append(list(data[i].unique()))
        filters[i] = list(data[i].unique()) + ['ALL']
    for i in paramters['comb_num_columns']:
        comb.append(get_num_cols_quartiles(list(data[i])))
    pred_data = pd.DataFrame(list(itertools.product(*comb)))
    counter = 0
    for i in paramters['comb_cat_columns'] + paramters['comb_num_columns']:
        pred_data = pred_data.rename(columns={counter: i})
        counter += 1
    iters = int(len(comb) / paramters['prediction_batch_size'])
    return pred_data, filters, iters

def get_prediction(model_path, iters, data, batch_size):
    h2o.init(nthreads=-1)
    model = h2o.load_model(model_path)
    prediction = []
    warnings.filterwarnings("ignore")
    t1= datetime.datetime.now()
    for i in range(0, iters+1):
        _data = data.ix[(i*batch_size):((i+1)*batch_size)]
        _data_h20 = h2o.H2OFrame(_data)
        pred = model.predict(_data_h20)
        prediction += list(pred.as_data_frame(use_pandas=True)['predict'])
    t2 = datetime.datetime.now()
    print("total run time :", round((t2 - t1).total_seconds() / 60, 2))
    h2o.shutdown(prompt = False)
    return prediction

