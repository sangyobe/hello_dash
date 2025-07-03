from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Initialize the app - incorporate css
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['stylesheet/bWLwgP.css']
app = Dash(external_stylesheets=external_stylesheets)

# Incorporate data
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = pd.read_csv('data/gapminder2007.csv')
# print(df.head)

# Requires Dash 2.17.0 or later
app.layout = [
    html.Div(children='Hello Dash'),
    dash_table.DataTable(data=df.to_dict(orient = 'records'), page_size=10),
    dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg')),
    html.Hr(),
    html.Div(className='row', children=[
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'],
                       value='lifeExp',
                       inline=True,
                       id='controls-and-radio-item')
    ]),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dash_table.DataTable(data=df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='controls-and-graph')
        ])
    ])
    # dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    # dcc.Graph(figure={}, id='controls-and-graph')
]

# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

if __name__ == '__main__':
    app.run(debug=True)