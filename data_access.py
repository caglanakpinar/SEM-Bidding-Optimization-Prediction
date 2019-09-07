import pandas as pd
from sklearn.externals import joblib

def get_data_from_csv(parameters):
    if parameters['path']:
        data = pd.read_csv(parameters['path'])
    else:
        data = pd.read_csv("sem_bidding.csv")
    return data


def predictWriterAndReader(fileName, isWriting, modelDict, isDeletingFile):
    file_dir = './predictions/' + fileName + '.pkl'

    if isWriting:
        if os.path.exists(file_dir):
            os.remove(file_dir)
        joblib.dump(modelDict, file_dir)
        print("predicted values updated!")
    else:
        modelDict_old = joblib.load(file_dir)
        return modelDict_old