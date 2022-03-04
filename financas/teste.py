import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import glob 

def read_data() :
  path = r'./files' # use your path
  all_files = glob.glob(path + "/*.csv")

  data = []
  for filename in all_files:
      df = pd.read_csv(filename, index_col=None, header=0)
      data.append(df)

  frame = pd.concat(data, axis=0, ignore_index=True)
  frame[['year', 'month', 'day']] = frame['date'].str.split('-', 2, expand=True)
  frame.year = pd.to_numeric(frame.year, downcast='signed')
  frame.month = pd.to_numeric(frame.month, downcast='signed')
  frame.day = pd.to_numeric(frame.day, downcast='signed')  
  frame = frame[frame.amount > 0.0]
  
  return frame

def get_figure_data(data, id, year, month):
  
  data = data[data.year == year]
  data = data[data.month == month]  
  data["percentege"] = data.amount / data.amount.sum()
  data = data.groupby(id).sum().reset_index()
  
  if not 'outros' in data[id]:
    data2 = data[data.percentege < 0.01]
    data3 = pd.DataFrame([['outros', data2.amount.sum(), data2.percentege.sum()]], columns=[id, 'amount', 'percentege'])
    data = data.append(data3, ignore_index=True)  
    data = data.drop(data2.index.values.tolist())
  
  return data
  

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

df = read_data()

filtered_df = get_figure_data(df, 'category', 2022, 1)

labels = filtered_df['category'].to_dict().values()
sizes = filtered_df['amount'].to_dict().values()

fig = px.pie(values=sizes, labels=sizes, names=labels)
fig.update_traces(textposition='outside', textinfo='percent+label')
fig.update_layout(transition_duration=500)

app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),

    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.

                Note that if `layout.clickmode = 'event+select'`, selection data also
                accumulates (or un-accumulates) selected data if you hold down the shift
                button while clicking.
            """),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Zoom and Relayout Data**

                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
                Clicking on legend items will also fire
                this event.
            """),
            html.Pre(id='relayout-data', style=styles['pre']),
        ], className='three columns')
    ])
])


@app.callback(
    Output('hover-data', 'children'),
    Input('basic-interactions', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(
    Output('click-data', 'label'),
    Input('basic-interactions', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)


@app.callback(
    Output('relayout-data', 'children'),
    Input('basic-interactions', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)