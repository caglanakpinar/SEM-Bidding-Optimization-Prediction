import h2o
import data_access
import data_manipulation
import prediction
import model_train
import visualization
import constants

# parameters shapes how we process CPC, CTR and reach prediction
parameters = {
    # this path must have .csv file it has data has CTR, CPS, reach and other features for prediction.
    # Ex: pls check sem_bidding.csv file
    'path': None,
    # this allows us the train our model again. If no need assign False
    # training process takes about 1 hour. Make sure have 1.7gb free ram before train model. It also works on h20.
    'model_train': True,
    # This also takes half an hour. It runs the model with combined features in order to find the optimum solutions
    'predict': False,
    # output of the project assigning on output dictionary.
    'output': {
        'cpc': {'model_path': None, 'predicted': None,
                'model_features': {'num': ['impression', 'rpo'],
                                   'cat': ['aggresive_level', 'bid_limits', 'content', 'pop_level',
                                           'strategy', 'time_period', 'keyword_1', 'keyword_2']
                                   },
                'best_model': None},
        'ctr': {'model_path': None, 'predicted': None,
                'model_features': {'num': ['cpc', 'impression', 'rpo'], # for ctr cpc is also adding to feature set
                                   'cat': ['aggresive_level', 'bid_limits', 'content', 'pop_level',
                                           'strategy', 'time_period', 'keyword_1', 'keyword_2']
                                   },
                'best_model': None},
        'reach': {'model_path': None, 'predicted': None,
                  'model_features': {'num': ['impression', 'rpo'],
                                     'cat': ['aggresive_level', 'bid_limits', 'content', 'pop_level', 'strategy',
                                             'time_period', 'keyword_1', 'keyword_2']
                                     },
                  'best_model': None}
    },
    # These are the categorical features of our model
    'comb_cat_columns': ['aggresive_level', 'bid_limits', 'content', 'pop_level',
                         'strategy', 'time_period', 'keyword_1', 'keyword_2'],
    # These are numerical features of our mode
    'comb_num_columns': ['impression', 'rpo'],
    # prediction data frame assigning
    'pred_data': None,
    # These are unique values of model features. We are using them as filters on our dashboard
    'dashboard_filters': None,
    # Combination of sample data set has 8 millions of rows. That is why we are running the in a batch size and
    # appending them in an array
    'prediction_batch_size': 200000,
    # This returns optimum solution for our sample data set. Minimum cost max revenue
    'solution': None
}

def main(params):
    print("let`s get started!")
    print("trained models are detected!") if not params['model_train'] else print("let`s train CTR, CPC and reach")
    print("predicted values are detected!") if not params['predict'] else print("let`s predict")

    # gather data from .csv.
    data = data_access.get_data_from_csv(params)
    # doing manipulations for parsing keywords and calculating total cost and revenue for each rows.
    data = data_manipulation.calculate_total_cost_revenue_conversion(data)
    # for sample data 8 million gathers combinations of each categorical features
    params['pred_data'], params['dashboard_filters'], iters = prediction.combination_data_preparation(data, params)

    # start prediction or training model procces of each metric
    for y in params['output']:
        # if we assign model path is gathers model from there. Othervise path is assigned in constans.
        _path = params['output'][y]['model_path'] if params['output'][y][
                                                         'model_path'] is not None else constants.model_save_path
        if params['model_train']:
            # inputs for training process
            if params['output'][y]['model_features']['num'] is None:
                X_decoded = constants.model_features[y]
            else:
                X_decoded = params['output'][y]['model_features']
            # this is for one-hot encoding for categorical features.
            _data, X_encoded = data_manipulation.converting_numeric_encoder(data, X_decoded, y)
            # each learning process assign for GGM, DRF, DNN, GLM machine Learning models.
            # At the end H2o allows us to find the best model by using stack Ensemble model
            _model = model_train.best_prediction_model(_data, constants.search_criteria,
                                                       constants.hyper_p_gbm, constants.hyper_p_drf,
                                                       constants.hyper_p_dnn,constants.hyper_p_glm,
                                                       y, X_encoded,
                                                       constants.split_ratio
                                                      )
            _model.compute_train_process()
            _model.compute_best_model()
            params['output'][y]['best_model'] = _model.best_model
            h2o.save_model(model=params['output'][y]['best_model'], path=_path, force=True)
            # shot down h2o instance. This project it runs on each available cores on your server or local comp.
            h2o.shutdown(prompt=False)

        if params['predict']:
            # prediction is initializing with trained model. batch size is crucial point at here
            params['output'][y]['predicted'] = prediction.get_prediction(params['output'][y]['model_path'],
                                                                         iters,
                                                                         params['pred_data'],
                                                                         params['prediction_batch_size'])
            # writing on a pickle the prediction values as array
            data_access.pred_write_reader(_path, y, True, params)
        else:
            # check existing path has the predictions
            params['output'][y]['predicted'] = data_access.pred_write_reader(_path, y, False, [])

if __name__ == '__main__':
  main(parameters)
  parameters = visualization.calcualtion_best_sem_options(parameters)
  visualization.create_dashboard(parameters) # this is for dashboard visualize the outputs
