import pandas as pd
from sklearn.externals import joblib
import os

def get_data_from_csv(parameters):
    if parameters['path']:
        data = pd.read_csv(parameters['path'])
    else:
        data = pd.read_csv("sem_bidding.csv")
    return data


def pred_write_reader(fileName, y, isWriting, params):
    file_dir = './' + fileName + y +'.pkl'

    if isWriting:
        if os.path.exists(file_dir):
            os.remove(file_dir)
        joblib.dump(params['output'][y]['predicted'], file_dir)
        print("predicted values updated!")
    else:
        predicitions = joblib.load(file_dir)
        return predicitions