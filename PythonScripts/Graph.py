import dash
from dash import dcc, html
from dash.dependencies import Output, Input
from collections import deque
import plotly.graph_objs as go
import pandas as pd
import os

# Initialize the Dash app
app = dash.Dash(__name__)
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                margin: 0 !important;
                padding: 0 !important;
                background-color: transparent !important;
                overflow: hidden;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# The Layout: Simple and designed for transparency
app.layout = html.Div([
    #html.H2("Symboly Alertness Live HUD", 
    #        style={'color': 'transparent', 'textAlign': 'center', 'fontFamily': 'Arial'}),
    #
    dcc.Graph(
        id='live-graph', 
        animate=False, 
        config={'displayModeBar': False}, # Hides the plotly toolbar for a cleaner look
        style={'height': '100vh', 'width': '100%'}
    ),
    
    dcc.Interval(
        id='graph-update',
        interval=1000, # Updates every 1 second
        n_intervals=0
    ),
], style={'backgroundColor':'rgba(0,0,0,0)', 
          'margin': '0px', 
          'padding': '0px',
          'overflow': 'hidden'})

@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    log_path = 'Live Data\log.csv'# This should match the path used in Data.py
    
    # Default empty lists if file doesn't exist yet
    times = []
    scores = []

    # 1. Read the data from the live log
    if os.path.exists(log_path):
        try:
            # Open the file and read the last 30 lines directly
            with open(log_path, 'r') as f:
                # deque(f, 30) reads only the end of the file into memory
                last_lines = deque(f, 30)
            
            # Parse the CSV lines into lists
            for line in last_lines:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    times.append(parts[0])
                    scores.append(float(parts[1]))
        except Exception as e:
            print(f"Graph Error: {e}")

    # 2. Create the data trace
    trace = go.Scatter(
        x=times,
        y=scores,
        name='Alertness',
        mode='lines+markers',
        line=dict(color="#8e5ef6", width=3), # Neon Cyan
        marker=dict(size=8, color='white', symbol='circle')
    )
    # Calculate the X-axis range based on the last 30 points
    if len(times) > 0:
        # Set the window to show the most recent point and the one 30 steps back
        x_range = [times[0], times[-1]] 
    else:
        x_range = [0, 30]
    layout = go.Layout(
        title={
            'text': "SYMBOLY ALERTNESS MONITOR",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'color': 'white', 'size': 20, 'family': 'Courier New'},
        },
        xaxis=dict(
            title=dict(text="TIMELINE (REAL-TIME)", font=dict(color='white', size=14), standoff=20),
            color='white',
            tickangle=-25, # Rotates labels for better fit
            nticks=10,     # Limits the number of labels shown at once
            showgrid=False,
            gridcolor='rgba(255, 255, 255, 0.2)',
            showline=True,
            linecolor='white',
            #mirror=True,
            range=x_range,
            fixedrange=True,
        ),
        yaxis=dict(
            title=dict(text="Alertness Score/Level", font=dict(color='white', size=14)),
            range=[0, 11],
            fixedrange=True,
            color='white',
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.2)',
            showline=True,
            linecolor='white',
            #mirror=True
        ),
        paper_bgcolor='rgba(0,0, 0, 0.6)',
        plot_bgcolor='rgba(0,0,0,0)',
        # INCREASED MARGINS: l=left, r=right, t=top, b=bottom
        margin=dict(l=35, r=25, t=25, b=60), 
        autosize=True,
        #font=dict(color='white')
    )

    return {'data': [trace], 'layout': layout}

if __name__ == '__main__':
    # Force host and port to match Overlay.py expectations
    app.run(host='127.0.0.1', port=8050, debug=False)
