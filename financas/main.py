import plotly.express as px
import pandas as pd
import glob

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


def read_data():
    path = r'./files'  # use your path
    all_files = glob.glob(path + "/*.csv")
    data = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        data.append(df)
    frame = pd.concat(data, axis=0, ignore_index=True)
    frame[['year', 'month', 'day']] = frame['date'].str.split(
        '-', 2, expand=True)
    frame.year = pd.to_numeric(frame.year, downcast='signed')
    frame.month = pd.to_numeric(frame.month, downcast='signed')
    frame.day = pd.to_numeric(frame.day, downcast='signed')
    frame = frame[frame.amount > 0.0]
    return frame  

def filter_date(data, year, month):
    data = data[data.year == year]
    data = data[data.month == month]
    return data
  
def remove_small_data(data) :
  data["percentege"] = data.amount / data.amount.sum()
  data = data.groupby(id).sum().reset_index()
  if not 'outros' in data[id]:
      data2 = data[data.percentege < 0.01]
      data3 = pd.DataFrame([['outros', data2.amount.sum(), data2.percentege.sum()]], columns=[
                            id, 'amount', 'percentege'])
      data = data.append(data3, ignore_index=True)
      data = data.drop(data2.index.values.tolist())  
  return data

###INTERFACE##
df = read_data()
app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
            step=None,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        dcc.Slider(
            id='month-slider',
            min=1,
            max=12,
            value=df['month'].min(),
            marks={str(month): str(month) for month in df['month'].unique()},
            step=None,
            tooltip={"placement": "bottom", "always_visible": True}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'} ), 
    html.Div([
        dcc.Graph(id='graph-aux')
    ], style={'display': 'inline-block', 'width': '49%'} )
])


###CALLBACKS##
@ app.callback(
    Output('month-slider', 'marks'),
    Output('month-slider', 'value'),
    Input('year-slider', 'value'))
def set_month_options(selected_year):
    filter_df=df[df.year == selected_year]
    marks={str(month): str(month) for month in filter_df['month'].unique()}
    value=df[df.year == selected_year].month.min()
    return marks, value


@ app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'),
    Input('month-slider', 'value'))
def update_figure(year, month):    
    filtered_df=filter_date(df, year, month)
    labels=filtered_df['category'].to_dict().values()
    sizes=filtered_df['amount'].to_dict().values()
    fig=px.pie(values=sizes, labels=sizes, names=labels)
    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(transition_duration=500)
    return fig
  
@app.callback(
    Output('graph-aux', 'figure'),
    Input('graph-with-slider', 'hoverData'),
    Input('year-slider', 'value'),
    Input('month-slider', 'value'))
def display_click_data(clickData, year, month):
    category = clickData['points'][0]['label']    
    if category in df.category.values :
      filtered_df = filter_date(df, year, month)
      filtered_df = filtered_df[filtered_df.category == category]
      labels=filtered_df['title'].to_dict().values()
      sizes=filtered_df['amount'].to_dict().values()
      fig=px.pie(values=sizes, labels=sizes, names=labels)
      fig.update_traces(textposition='outside', textinfo='percent+label')
      fig.update_layout(transition_duration=500)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
