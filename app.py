from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('Mall_Customers.csv')
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1('Mall Customers Data Visualization', 
                style={'textAlign': 'center', 'marginBottom': 30, 'color': '#2c3e50'}),
        html.Hr(style={'borderTop': '2px solid #e1e8ed'}),
    ], style={'padding': '20px', 'backgroundColor': '#f8f9fa'}),
    
    html.Div([
        html.Div([
            html.Label('X-Axis:', style={'fontWeight': 'bold', 'marginBottom': 10}),
            dcc.Dropdown(
                id='x-axis', 
                options=[{'label': col, 'value': col} for col in df.columns if df[col].dtype in ['int64', 'float64']],
                value='Age',
                style={'width': '100%'}
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            html.Label('Y-Axis:', style={'fontWeight': 'bold', 'marginBottom': 10}),
            dcc.Dropdown(
                id='y-axis', 
                options=[{'label': col, 'value': col} for col in df.columns if df[col].dtype in ['int64', 'float64']],
                value='Annual Income (k$)',
                style={'width': '100%'}
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ], style={'padding': '20px', 'marginBottom': 20}),
    
    dcc.Graph(id='scatter-plot', style={'padding': '20px'}),

    html.Div([
        html.Label('Histogram Variable:', style={'fontWeight': 'bold', 'marginBottom': 10}),
        dcc.Dropdown(
            id='histogram-variable',
            options=[{'label': col, 'value': col} for col in df.columns if df[col].dtype in ['int64', 'float64']],
            value='Age',
            style={'width': '100%'}
        ),
        dcc.Graph(id='histogram', style={'padding': '20px'})  # ✅ inside the Div
    ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),

], style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '1200px', 'margin': '0 auto', 
          'backgroundColor': '#ffffff', 'borderRadius': '8px', 
          'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'padding': '20px'})


# ✅ Each callback immediately above its own function
@callback(
    Output('scatter-plot', 'figure'),
    [Input('x-axis', 'value'), Input('y-axis', 'value')]
)
def update_scatter_plot(x_axis, y_axis):
    fig = px.scatter(df, x=x_axis, y=y_axis,
                     title=f'{x_axis} vs {y_axis}',
                     template='plotly_white')
    fig.update_layout(font=dict(family='Arial', size=12), hovermode='closest')
    return fig


# ✅ Separate decorator directly on its own function
@callback(
    Output('histogram', 'figure'),
    [Input('histogram-variable', 'value')]
)
def update_histogram(variable):
    fig = px.histogram(df, x=variable, nbins=20, 
                       title=f'Distribution of {variable}', 
                       template='plotly_white')
    fig.update_layout(font=dict(family='Arial', size=12), hovermode='closest')
    return fig


if __name__ == '__main__':
    app.run(debug=True)
    server = app.server