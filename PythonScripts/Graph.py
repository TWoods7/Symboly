import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import pandas as pd
import os

# Initialize the Dash app
app = dash.Dash(__name__)

# The Layout: Simple and designed for transparency
app.layout = html.Div([
    html.H2("Symboly Alertness Live HUD", 
            style={'color': 'white', 'textAlign': 'center', 'fontFamily': 'Arial'}),
    
    dcc.Graph(
        id='live-graph', 
        animate=True, 
        config={'displayModeBar': False} # Hides the plotly toolbar for a cleaner look
    ),
    
    dcc.Interval(
        id='graph-update',
        interval=1000, # Updates every 1 second
        n_intervals=0
    ),
], style={'backgroundColor': 'rgba(0,0,0,0)', 'padding': '10px'})

@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    log_path = 'log.csv'
    
    # Default empty lists if file doesn't exist yet
    times = []
    scores = []

    # 1. Read the data from the live log
    if os.path.exists(log_path):
        try:
            # We take the last 30 points to keep the graph moving
            df = pd.read_csv(log_path, names=['Time', 'Score']).tail(30)
            times = df['Time'].tolist()
            scores = df['Score'].tolist()
        except Exception as e:
            print(f"Graph Error: {e}")

    # 2. Create the data trace
    trace = go.Scatter(
        x=times,
        y=scores,
        name='Alertness',
        mode='lines+markers',
        line=dict(color='#00ebff', width=3), # Neon Cyan
        marker=dict(size=8, color='white', symbol='circle')
    )

    layout = go.Layout(
        title={
            'text': "Symboly Alertness HUD",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'color': 'white', 'size': 20},
            #'paper_bgcolor':'rgba(30, 30, 30, 0.6)', # Semi-transparent dark grey
            #'plot_bgcolor' :'rgba(0, 0, 0, 0)',       # Keep the inner plot clear
        },
        xaxis=dict(
            title=dict(text="Time (Last 30 Captures)", font=dict(color='white', size=14)),
            color='white',
            tickangle=-45, # Rotates labels for better fit
            nticks=10,     # Limits the number of labels shown at once
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.2)',
            showline=True,
            linecolor='white',
            mirror=True
        ),
        yaxis=dict(
            title=dict(text="Alertness Score", font=dict(color='white', size=14)),
            range=[0, 11],
            color='white',
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.2)',
            showline=True,
            linecolor='white',
            mirror=True
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # INCREASED MARGINS: l=left, r=right, t=top, b=bottom
        margin=dict(l=80, r=40, t=80, b=80), 
        font=dict(color='white')
    )

    return {'data': [trace], 'layout': layout}

if __name__ == '__main__':
    # Force host and port to match Overlay.py expectations
    app.run(host='127.0.0.1', port=8050, debug=False)


# import dash
# from dash.dependencies import Output, Input
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly
# import random
# import plotly.graph_objs as go
# from collections import deque

# # This is a simple Dash app that creates a live-updating graph. It uses a deque to store the last
# #  20 points of data for both X and Y axes. The graph updates every second with new random data, 
# # simulating a live data feed. The X values increment by 1, while the Y values fluctuate randomly 
# # around the previous value.

# X = deque(maxlen = 20)
# X.append(1)

# Y = deque(maxlen = 20)
# Y.append(1)

# app = dash.Dash(__name__)

# app.layout = html.Div(
#     [
#         dcc.Graph(id = 'live-graph', animate = True),
#         dcc.Interval(
#             id = 'graph-update',
#             interval = 1000,
#             n_intervals = 0
#         ),
#     ]
# )

# @app.callback(
#     Output('live-graph', 'figure'),
#     [ Input('graph-update', 'n_intervals') ]
# )

# def update_graph_scatter(n):
#     X.append(X[-1]+1)
#     Y.append(Y[-1]+Y[-1] * random.uniform(-0.1,0.1))

#     data = plotly.graph_objs.Scatter(
#             x=list(X),
#             y=list(Y),
#             name='Scatter',
#             mode= 'lines+markers'
#     )

#     return {'data': [data],
#             'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [min(Y),max(Y)]),)}

# if __name__ == '__main__':
#     app.run()