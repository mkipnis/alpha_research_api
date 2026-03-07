# Copyright (c) Mike Kipnis (mike.kipnis@gmail.com) - Alpha Research Online

import dash
from dash import Input, Output, html, dcc
import plotly.graph_objs as go

class RevenueIncomeChart(object):

    def __init__(self, app: dash.Dash):
        self.app = app
        self.chart = dcc.Graph(id="revenue-income-chart",
                               style={
                                   "height": "100%",
                                   "width": "100%",
                               },
                               )
        self._register_callbacks()

    def layout(self):
        return html.Div(
            self.chart,
            style={
                "height": "30vh",  # 👈 was 10vh, now half
                "width": "100%",
                "display": "flex",
            },
        )

    def _register_callbacks(self):

        @self.app.callback(
            Output("revenue-income-chart", "figure"),
            Input("stock-info-set", "data"),
            prevent_initial_call=True,
        )
        def update_chart(stock_info_set):

            if not stock_info_set:
                raise dash.exceptions.PreventUpdate

            symbol = stock_info_set['symbol']
            market_data = stock_info_set['data'][symbol]['market_data']
            income_statements = market_data['income_statements']

            labels = []
            revenue = []
            income = []

            for period, values in income_statements.items():
                try:
                    labels.append(period)
                    revenue.append(
                        values["revenue"]
                    )
                    income.append(
                        values["income"]
                    )
                except Exception:
                    continue

            fig = go.Figure()

            # Revenue Bars (left axis)
            fig.add_trace(
                go.Bar(
                    x=labels,
                    y=revenue,
                    name="Revenue",
                    marker=dict(color="rgba(152,195,121,0.75)"),
                    yaxis="y1",
                )
            )

            # Income Bars (right axis)
            fig.add_trace(
                go.Bar(
                    x=labels,
                    y=income,
                    name="Income",
                    marker=dict(color="rgba(224,108,118,0.75)"),
                    yaxis="y2",
                )
            )

            fig.update_layout(
                barmode="group",
                paper_bgcolor="#192231",
                plot_bgcolor="#192231",
                font=dict(color="#ffeed9"),
                hovermode="x unified",
                margin=dict(l=50, r=50, t=50, b=50),

                xaxis=dict(showgrid=False),

                yaxis=dict(
                    title="Revenue",
                    gridcolor="#424242",
                ),

                yaxis2=dict(
                    title="Income",
                    overlaying="y",
                    side="right",
                    showgrid=False,
                ),

                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
            )

            return fig
