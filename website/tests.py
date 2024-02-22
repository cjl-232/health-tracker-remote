# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# df = pd.DataFrame({'time': [1,2,3], 'output': [4, 5, 6], 'bar': [2,2,2]})

# fig = go.Figure()
# fig.add_trace(go.Scatter(x = df['time'], y = df['output'], name = 'Weight', mode = 'lines+markers'))

# #fig = px.line(df, x = 'time', y = 'output', name = 'Weight')
# fig.update_traces(showlegend=True)
# fig.add_hline(y=5, showlegend = True, name="TEST")
# fig.add_hline(y=6, showlegend = True)

# #fig.add_trace({'type': 'scatter', 'x': 'time', 'y': 'bar'})

# fig.show()

# #Work out how to fix the bottom at y = 0 with no overflow...

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_graph():
    # Your server-side data retrieval and processing here
    time_series_data = [1, 2, 3, 4, 5]
    horizontal_lines_data = [2, 4, 6]

    # Create subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Plot main time series
    fig.add_trace(go.Scatter(x=list(range(len(time_series_data))), y=time_series_data, mode='lines', name='Time Series'))

    # Define a color scale for consistent coloring
    color_scale = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22']

    # Add horizontal lines with consistent colors
    for i, line_value in enumerate(horizontal_lines_data):
        color = color_scale[i % len(color_scale)]  # Cycle through the color scale
        fig.add_shape(type="line", x0=0, x1=len(time_series_data)-1, y0=line_value, y1=line_value,
                      line=dict(color=color,width=2, dash="dash"),
                      name=f'Line at {line_value}', showlegend=True)

    # Update layout
    #fig.update_layout(legend=dict(x=0, y=1, traceorder='normal'))

    # Set y-axis range to start from 0
    fig.update_yaxes(range=[0,max(time_series_data+horizontal_lines_data) * 1.1])

    # Enable user to adjust x-axis range while keeping y-axis fixed
    fig.update_xaxes(rangeslider=dict(visible=True))

    # Update layout
    fig.update_layout(title='Your Plot Title')
    fig.show()

generate_graph()