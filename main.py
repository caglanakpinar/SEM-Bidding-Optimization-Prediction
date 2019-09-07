import h2o

import data_access
import data_manipulation
import prediction
import model_train
import visualization
import constants

import h

parameters = {
    'model_train': True,
    'predict': True,
    'output':{
        'CPC': {'model_path': None, 'predicted': None, 'model_features': {'X': None}, 'best_model': None},
        'CTR': {'model_path': None, 'predicted': None, 'model_features': {'X': None}, 'best_model': None},
        'reach': {'model_path': None, 'predicted': None, 'model_features': {'X': None}, 'best_model': None}
    },
    'comb_cat_columns': [],
    'comb_num_columns': []
}

def main(parameters):
    print("let`s get started!")
    data = data_access.get_data_from_csv(parameters)
    data = data_manipulation.calculate_total_cost_revenue_conversion(data, parameters)
    pred_data, iters = prediction.combination_data_preparation(data, parameters)
    for y in parameters['output']:
        if parameters['model_train']:
            X = constants.model_features[y]['X'] if y['model_features']['X'] is None else y['model_features']['X']
            model_train.best_prediction_model(data, constants.search_criteria, constants.hyper_p_gbm,
                                              constants.hyper_p_drf, constants.hyper_p_dnn,constants.hyper_p_glm)
            model_train.best_prediction_model.compute_train_process()
            model_train.best_prediction_model.compute_best_model()
            parameters['output'][y]['best_model'] = model_train.best_prediction_model.best_model
        else:
            if parameters['predict']:
                parameters['output'][y]['predicted'] = prediction.get_prediction(parameters['model_path'],
                                                                                 iters, pred_data)
            else:
                prediction_cpc = prediction.get_prediction(parameters['CPC_model_path'], iters, pred_data)




if __name__ == '__main__':
  main(parameters)
  visualization.create_dashboard(parameters)