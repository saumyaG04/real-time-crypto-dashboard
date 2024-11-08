import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import requests
import plotly.graph_objs as go
import time

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def fetch_exchange_rate():
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=EUR&apikey=YOUR_API_KEY'
    response = requests.get(url).json()
    return float(response["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

exchange_rates = []
timestamps = []

app.layout = dbc.Container([
    html.H1("Real-Time BTC to EUR Exchange Rate"),
    dcc.Graph(id="exchange-rate-graph"),
    dcc.Interval(id="interval-component", interval=1*60*1000, n_intervals=0)
])

@app.callback(Output("exchange-rate-graph", "figure"), [Input("interval-component", "n_intervals")])
def update_graph(n):
    rate = fetch_exchange_rate()
    exchange_rates.append(rate)
    timestamps.append(time.strftime('%H:%M:%S'))
    
    fig = go.Figure([go.Scatter(x=timestamps, y=exchange_rates, mode="lines+markers")])
    fig.update_layout(title="BTC to EUR Exchange Rate", xaxis_title="Time", yaxis_title="Exchange Rate (EUR)")
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)