from IPython.display import display, HTML
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
import math
import sys


def report_block_template(report_type, graph_url, caption=''):
    if report_type == 'interactive':
        graph_block = '<iframe style="border: none;" src="{graph_url}.embed" width="100%" height="600px"></iframe>'
    elif report_type == 'static':
        graph_block = (''
            '<a href="{graph_url}" target="_blank">' # Open the interactive graph when you click on the image
                '<img style="height: 400px;" src="{graph_url}.png">'
            '</a>')

    report_block = ('' +
        graph_block +
        '{caption}' + # Optional caption to include below the graph
        '<br>'      + # Line break
        '<a href="{graph_url}" style="color: rgb(190,190,190); text-decoration: none; font-weight: 200;" target="_blank">'+
            'Click to comment and see the interactive graph' + # Direct readers to Plotly for commenting, interactive graph
        '</a>' +
        '<br>' +
        '<hr>') # horizontal line                       

    return report_block.format(graph_url=graph_url, caption=caption)


long_df = pd.read_csv(sys.argv[1],index_col=0, header=None, sep=" ")
long_df = long_df.div(60)
#long_df = long_df.iloc[: , 1:]

#fig = px.bar(long_df, orientation='h', color_discrete_sequence=px.colors.qualitative.Vivid)
fig = px.bar(long_df, orientation='h', color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A'])#, '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52'])
fig.update_layout(showlegend=False)
fig.update_layout(title=sys.argv[2], font=dict( family="Arial", size=12, color="Black" ) )
fig.update_layout(yaxis=dict(title='Process',tickmode='linear'))
fig.update_layout(xaxis=dict(title='Time (min)'))
fig.update_xaxes(range=[0, int(sys.argv[3])])
pio.write_image(fig, sys.argv[4]+".png")
fig.show()

graph_url='http://127.0.0.1:44539/'

interactive_report = ''
static_report = ''

_static_block = report_block_template('static', graph_url, caption='')
_interactive_block = report_block_template('interactive', graph_url, caption='')

static_report += _static_block
interactive_report += _interactive_block

display(HTML(interactive_report))
