import pandas as pd

def calculate_total_cost_revenue_conversion(data):
    data['conversion'] = data.apply(lambda row: int(row['reach'] * row['ctr']), axis=1)
    data[['keyword_1', 'keyword_2']] = data.apply(lambda row:
                                                  pd.Series([row['keywords'].split("-")[0] + "_1",
                                                             row['keywords'].split("-")[1] + "_2"]), axis=1)

    data['total_cost'] = data['cpc'] * data['conversion']
    data['total_revenue'] = data['rpo'] * data['conversion']
    data['cost_ratio'] = data['total_cost'] / data['total_revenue']
    return data

def converting_numeric_encoder(df, features):
    feature_set = []
    for col in features['cat']:
        _features = pd.get_dummies(df[col])
        df = pd.concat([df, _features], axis=1)
        feature_set += list(_features.columns)
    return df[feature_set + features['num']]