import h2o
import data_access
import data_manipulation
import prediction
import model_train
import visualization
import constants

parameters = {
    'path': None,
    'model_train': False,
    'predict': False,
    'output': {
        'cpc': {'model_path': None, 'predicted': None,
                'model_features': {'num': None , 'cat': None}, 'best_model': None},
        'ctr': {'model_path': None, 'predicted': None,
                'model_features': {'num': None , 'cat': None}, 'best_model': None},
        'reach': {'model_path': None, 'predicted': None,
                  'model_features': {'num': None , 'cat': None}, 'best_model': None}
    },
    'comb_cat_columns': ['aggresive_level', 'bid_limits', 'content', 'pop_level',
                         'strategy', 'time_period', 'keyword_1', 'keyword_2'],
    'comb_num_columns': ['impression', 'rpo'],
    'pred_data': None,
    'dashboard_filters': None,
    'prediction_batch_size': 200000

}

def main(params):
    print("let`s get started!")
    data = data_access.get_data_from_csv(params)
    data = data_manipulation.calculate_total_cost_revenue_conversion(data)
    params['pred_data'], params['dashboard_filters'], iters = prediction.combination_data_preparation(data, params)
    for y in params['output']:
        _path = params['output'][y]['model_path'] if params['output'][y][
                                                         'model_path'] is not None else constants.model_save_path

        if params['model_train']:

            X = constants.model_features[y] if y['model_features']['X']['numeric'] is None else y['model_features']['X']
            _data = data_manipulation.converting_numeric_encoder(data, X)
            model_train.best_prediction_model(_data, constants.search_criteria,
                                              constants.hyper_p_gbm, constants.hyper_p_drf,
                                              constants.hyper_p_dnn,constants.hyper_p_glm
                                              )
            model_train.best_prediction_model.compute_train_process()
            model_train.best_prediction_model.compute_best_model()
            params['output'][y]['best_model'] = model_train.best_prediction_model.best_model
            h2o.save_model(model=params['output'][y]['best_model'], path=_path, force=True)
            h2o.shutdown(prompt=False)
        if params['predict']:
            params['output'][y]['predicted'] = prediction.get_prediction(params['output'][y]['model_path'],
                                                                         iters,
                                                                         params['pred_data'],
                                                                         params['prediction_batch_size'])
            data_access.pred_write_reader(_path, y, True, params)
        else:
            params['output'][y]['predicted'] = data_access.pred_write_reader(_path, y, False, [])

if __name__ == '__main__':
  main(parameters)
  visualization.create_dashboard(parameters)