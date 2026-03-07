# Copyright (c) Mike Kipnis (mike.kipnis@gmail.com) - Alpha Research Online

import dash
from dash import Input, Output, html, dcc, State
import plotly.graph_objs as go

class PriceChart(object):

    def __init__(self, app: dash.Dash):
        self.app = app
        self.price_chart = dcc.Graph(id="price-chart")
        self._register_callbacks()

    def layout(self):
        return html.Div(
            self.price_chart,
            style={
                "flex": "1 1 50%",  # 50% of width
                "minHeight": "0",
                "display": "flex",
                "flexDirection": "column",
                "border": "1px solid #424242",
                "borderRadius": "1px",
                "padding": "6px",
                "backgroundColor": "#192231",
                }
            ),



    def _register_callbacks(self):

        @self.app.callback(
            Output("price-chart", "figure"),
            Input("stock-info-set", "data"),
            prevent_initial_call=True,
        )
        def update_graph(stock_info_set):
            if not stock_info_set:
                raise dash.exceptions.PreventUpdate

            symbol = stock_info_set['symbol']
            index = stock_info_set['index']

            symbol_chart_data = stock_info_set['data'][symbol]['chart_1Y']
            index_chart_data = stock_info_set['data'][index]['chart_1Y']

            price_dates = [p['price_date'] for p in index_chart_data]
            stock_price = [float(p['close_price']) for p in symbol_chart_data]
            benchmark_price = [float(p['close_price']) for p in index_chart_data]

            def pct_change(prices):
                start = prices[0] if prices else 1
                return [((p - start) / start) * 100 for p in prices]

            stock_pct = pct_change(stock_price)
            benchmark_pct = pct_change(benchmark_price)

            # Ensure customdata matches y-length
            stock_customdata = stock_price if len(stock_price) == len(stock_pct) else [None] * len(stock_pct)
            benchmark_customdata = benchmark_price if len(benchmark_price) == len(benchmark_pct) else [None] * len(
                benchmark_pct)

            # Colors
            delta = stock_price[-1] - stock_price[0] if stock_price else 0
            if delta > 0:
                stock_border = "rgb(152,195,121)"
                stock_fill = "rgba(152,195,121,0.1)"
            else:
                stock_border = "rgb(224,108,118)"
                stock_fill = "rgba(224,108,118,0.1)"

            benchmark_border = "rgb(101,210,242)"
            benchmark_fill = "rgba(101,210,242,0.1)"

            fig = go.Figure()

            # Stock trace
            fig.add_trace(go.Scatter(
                x=price_dates,
                y=stock_pct,
                mode='lines+markers',
                line=dict(color=stock_border, width=1.5, shape='spline'),
                fill='tozeroy',
                fillcolor=stock_fill,
                marker=dict(size=4),
                name=symbol,
                customdata=stock_customdata,
                hovertemplate=f'{symbol}: %{{customdata:.2f}} : %{{y:.2f}}%<extra></extra>'
            ))

            # Benchmark trace
            fig.add_trace(go.Scatter(
                x=price_dates,
                y=benchmark_pct,
                mode='lines+markers',
                line=dict(color=benchmark_border, width=1.5, shape='spline'),
                fill='tozeroy',
                fillcolor=benchmark_fill,
                marker=dict(size=4),
                name=index,
                customdata=benchmark_customdata,
                hovertemplate=f'{index}: %{{customdata:.2f}} : %{{y:.2f}}%<extra></extra>'
            ))

            fig.update_layout(
                paper_bgcolor="#192231",
                plot_bgcolor="#192231",
                font=dict(color="#ffeed9"),
                hovermode='closest',
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor="#424242"),
                showlegend=True,
                margin=dict(l=50, r=50, t=50, b=50)
            )

            return fig

