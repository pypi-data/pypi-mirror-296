import backtrader as bt
import numpy as np
import dash
from dash import dash_table
from dash import dcc, html
import pandas as pd

def init_analyzers(cerebro):
    cerebro.addanalyzer(bt.analyzers.Returns, 
                        _name='returns', 
                        timeframe=bt.TimeFrame.Minutes, 
                        compression=1,
                        tann=252 * 6.5 * 60)

    cerebro.addanalyzer(bt.analyzers.TimeReturn, 
                        _name='timereturn',
                        timeframe=bt.TimeFrame.Minutes, 
                        compression=1)

    cerebro.addanalyzer(bt.analyzers.SharpeRatio, 
                        _name='sharpe',
                        timeframe=bt.TimeFrame.Minutes,
                        compression=1,
                        annualize=True)

    cerebro.addanalyzer(bt.analyzers.DrawDown, 
                        _name='drawdown')

def show_performance(strats):
    for strat in strats:
        returns = strat.analyzers.returns.get_analysis()
        print(f"Total Compound Return: {returns['rtot']:.2%}")
        print(f"Annualized Return: {returns['rnorm']:.2%}")

        sharpe = strat.analyzers.sharpe.get_analysis()
        print(f"Sharpe Ratio: {sharpe['sharperatio']:.2f}")

        timereturn = strat.analyzers.timereturn.get_analysis()
        timereturn_list = list(timereturn.values())
        volatility = np.std(timereturn_list)
        annual_volatility = volatility * np.sqrt(252)
        print(f"Annualized Volatility: {annual_volatility:.2%}")

        drawdown = strat.analyzers.drawdown.get_analysis()
        print(f"Max Drawdown: {drawdown.max.drawdown:.2f}%")
        print(f"Max Drawdown Duration: {drawdown.max.len}")

        data = {
            "Metrics": [
                "Total Compound Return", 
                "Annualized Return", 
                "Sharpe Ratio", 
                "Annualized Volatility", 
                "Max Drawdown", 
                "Max Drawdown Duration"
            ],
            "Result": [
                f"{returns['rtot']:.2%}", 
                f"{returns['rnorm']:.2%}", 
                f"{sharpe['sharperatio']:.2f}", 
                f"{annual_volatility:.2%}",
                f"{drawdown.max.drawdown:.2f}%",
                f"{drawdown.max.len}"
            ]
        }

        df = pd.DataFrame(data)
        app = dash.Dash(__name__)
        app.layout = html.Div([
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'lightgrey',
                    'fontWeight': 'bold'
                },
                style_table={'width': '100%'}
            )
        ])

        app.run_server(host='0.0.0.0', 
            port=8050, 
            jupyter_mode="jupyterlab",
            jupyter_server_url="http://192.168.25.144:8050", 
            debug=True
        )