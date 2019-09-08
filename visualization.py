import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import webbrowser
import warnings

def create_dashboard(params):
    filters = params['filters']
    data_pred = pd.concat([params['pred_data'],
                           pd.DataFrame(zip(params['output']['reach'],
                                            params['output']['ctr'],
                                            params['output']['cpc']))], axis=1).rename(
        columns={0: 'reach', 1: 'ctr', 2: 'cpc'})
    data_pred['conversion'] = data_pred['reach'] * data_pred['ctr']
    data_pred['total_cost'] = data_pred['cpc'] * data_pred['conversion']
    data_pred['total_revenue'] = data_pred['rpo'] * data_pred['conversion']

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        html.Div('Seach Engine Marketing Total Cost & Total Revenue'),
        html.Div([
            html.Div('aggresive_level', style={'width': '20%', 'float': 'left', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='crossfilter-aggresive_level',
                    options=[{'label': i, 'value': i} for i in filters['aggresive_level']],
                    multi=True,
                    value='agg_l_6'
                )

            ],
                style={'width': '20%', 'display': 'inline-block'}),

            html.Div('bid_limits', style={'width': '20%', 'float': 'right', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-bid_limits',
                    options=[{'label': i, 'value': i} for i in filters['bid_limits']],
                    value='bid_l_10',
                    multi=True,
                )
            ], style={'width': '20%', 'float': 'right', 'display': 'inline-block'})

        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '5px 2px',
            'width': '99%'
        }),

        html.Div([
            html.Div('content', style={'width': '20%', 'float': 'left', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-content',
                    options=[{'label': i, 'value': i} for i in filters['content']],
                    value='content_1',
                    multi=True,
                )

            ],
                style={'width': '20%', 'display': 'inline-block'}),
            html.Div('pop_level', style={'width': '20%', 'float': 'right', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-pop_level',
                    options=[{'label': i, 'value': i} for i in filters['pop_level']],
                    value='pop_l_3',
                    multi=True
                )
            ], style={'width': '20%', 'float': 'right', 'display': 'inline-block'})

        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '5px 2px',
            'width': '99%'
        }),

        html.Div([
            html.Div('SEM Bidding Strategy', style={'width': '20%', 'float': 'left', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-strategy',
                    options=[{'label': i, 'value': i} for i in filters['strategy']],
                    value='maximize_clicks',
                    multi=True,
                )

            ],
                style={'width': '20%', 'display': 'inline-block'}),
            html.Div('SEM Bidding Time Period', style={'width': '20%', 'float': 'right', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-time_period',
                    options=[{'label': i, 'value': i} for i in filters['time_period']],
                    value='weekend',
                    multi=True
                )
            ], style={'width': '20%', 'float': 'right', 'display': 'inline-block'})

        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '5px 2px',
            'width': '99%'
        }),

        html.Div([
            html.Div('Keyword 1st', style={'width': '20%', 'float': 'left', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-keyword_1',
                    options=[{'label': i, 'value': i} for i in filters['keyword_1']],
                    value='kw_2_1',
                    multi=True,
                )

            ],
                style={'width': '20%', 'display': 'inline-block'}),
            html.Div('keyword 2nd', style={'width': '20%', 'float': 'right', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-keyword_2',
                    options=[{'label': i, 'value': i} for i in filters['keyword_2']],
                    value='kw_1_2',
                    multi=True
                )
            ], style={'width': '20%', 'float': 'right', 'display': 'inline-block'})

        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '5px 2px',
            'width': '99%'
        }),

        html.Div([
            dcc.Graph(
                id='total-cost-revenue-scatter',
                hoverData={'points': [{'customdata': '2019-08-05'}]}
            )
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 10'}),

        html.Div([
            dcc.Graph(
                id='keyword-comparision-bar',
                hoverData={'points': [{'customdata': '5cca08a9f878f40008f9adae'}]}

            )
        ], style={'width': '51%', 'display': 'inline-block', 'padding': '0 20'})
    ])

    @app.callback(
        dash.dependencies.Output('total-cost-revenue-scatter', 'figure'),
        [dash.dependencies.Input('crossfilter-aggresive_level', 'value'),
         dash.dependencies.Input('crossfilter-bid_limits', 'value'),
         dash.dependencies.Input('crossfilter-content', 'value'),
         dash.dependencies.Input('crossfilter-pop_level', 'value'),
         dash.dependencies.Input('crossfilter-strategy', 'value'),
         dash.dependencies.Input('crossfilter-time_period', 'value'),
         dash.dependencies.Input('crossfilter-keyword_1', 'value'),
         dash.dependencies.Input('crossfilter-keyword_2', 'value')
         ]
    )
    def update_graph(aggresive_level, bid_limits, content, pop_level, strategy, time_period, keyword_1, keyword_2):

        def get_str(_str, arg):
            filters = arg[1] if type(arg[1]) == list else [arg[1]]
            if 'ALL' not in filters:
                arg_str = "', '".join(filters)
                is_started = " " if _str == "" else " and "
                _str += is_started + arg[0] + " in " + "('" + arg_str + "')"
            return _str

        query_str = ""
        values = [['aggresive_level', aggresive_level], ['bid_limits', bid_limits],
                  ['content', content], ['pop_level', pop_level], ['strategy', strategy],
                  ['time_period', time_period], ['keyword_1', keyword_1], ['keyword_2', keyword_2]]
        for fltr in values:
            query_str = get_str(query_str, fltr)
        dff_pivoted = data_pred.query(query_str) if query_str != "" else data_pred
        dff_pivoted = dff_pivoted.sort_values(by='total_cost', ascending=True)

        return {
            'data': [go.Scatter(
                x=dff_pivoted['total_cost'],
                y=dff_pivoted['total_revenue'],
                text=dff_pivoted['total_cost'],
                mode='markers',
                name='Control',
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            )],
            'layout': go.Layout(
                xaxis={
                    'title': 'total cost',
                },
                yaxis={
                    'title': 'total revenue'
                },
                margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                height=450,
                hovermode='closest'
            )
        }

    @app.callback(
        dash.dependencies.Output('keyword-comparision-bar', 'figure'),
        [dash.dependencies.Input('crossfilter-aggresive_level', 'value'),
         dash.dependencies.Input('crossfilter-bid_limits', 'value'),
         dash.dependencies.Input('crossfilter-content', 'value'),
         dash.dependencies.Input('crossfilter-pop_level', 'value'),
         dash.dependencies.Input('crossfilter-strategy', 'value'),
         dash.dependencies.Input('crossfilter-time_period', 'value'),
         dash.dependencies.Input('crossfilter-keyword_1', 'value'),
         dash.dependencies.Input('crossfilter-keyword_2', 'value')
         ]
    )
    def update_graph(aggresive_level, bid_limits, content, pop_level, strategy, time_period, keyword_1, keyword_2):
        def get_str(_str, arg):
            filters = arg[1] if type(arg[1]) == list else [arg[1]]
            if 'ALL' not in filters:
                arg_str = "', '".join(filters)
                is_started = " " if _str == "" else " and "
                _str += is_started + arg[0] + " in " + "('" + arg_str + "')"
            return _str

        query_str = ""
        values = [['aggresive_level', aggresive_level], ['bid_limits', bid_limits],
                  ['content', content], ['pop_level', pop_level], ['strategy', strategy],
                  ['time_period', time_period]]
        for fltr in values:
            query_str = get_str(query_str, fltr)
        dff_pivoted = data_pred.query(query_str) if query_str != "" else data_pred
        dff_pivoted = dff_pivoted.sort_values(by='total_cost', ascending=True)

        query_str_1 = get_str("", ['keyword_1', keyword_1])
        dff_pivoted_1 = dff_pivoted.query(query_str_1) if query_str_1 != "" else dff_pivoted
        query_str_2 = get_str("", ['keyword_2', keyword_2])
        dff_pivoted_2 = dff_pivoted.query(query_str_2) if query_str_2 != "" else dff_pivoted

        def get_descriptive_values(values):
            return [np.mean(values), np.median(values), max(values)]

        x = ['average', 'median', 'max']
        basic_values_cost_1 = get_descriptive_values(list(dff_pivoted_1['total_cost']))
        basic_values_cost_2 = get_descriptive_values(list(dff_pivoted_2['total_cost']))
        basic_values_revenue_1 = get_descriptive_values(list(dff_pivoted_1['total_revenue']))
        basic_values_revenue_2 = get_descriptive_values(list(dff_pivoted_2['total_revenue']))
        return {
            'data': [go.Bar(name='1st keyword Cost', x=x, y=basic_values_cost_1),
                     go.Bar(name='2nd keyword Cost', x=x, y=basic_values_cost_2),
                     go.Bar(name='1st keyword Revenue', x=x, y=basic_values_revenue_1),
                     go.Bar(name='2nd keyword Revenue', x=x, y=basic_values_revenue_2)
                     ],
            'layout': go.Layout(
                yaxis={
                    'title': 'Revenu & Cost Of Keywords'
                },
                margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                height=450,
                hovermode='closest'
            )
        }

    warnings.filterwarnings("ignore")
    webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=False)
