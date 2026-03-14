# Copyright (c) Mike Kipnis (mike.kipnis@gmail.com) - Alpha Research Online

import dash
import dash_ag_grid as dag
from dash import Input, Output, html, dcc, State
import dash_bootstrap_components as dbc
import revenue_and_income


def format_number(n):
    n = float(n)  # make sure it works with int or float
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.1f}B".rstrip("0").rstrip(".")
    elif n >= 1_000_000:
        return f"{n/1_000_000:.1f}M".rstrip("0").rstrip(".")
    elif n >= 1_000:
        return f"{n/1_000:.1f}K".rstrip("0").rstrip(".")
    else:
        return str(int(n))

class MarketData(object):

    def __init__(self, app: dash.Dash):
        self.app = app
        self.market_data = dag.AgGrid(
            id="market-data",
            rowData=[],
            defaultColDef={
                "resizable": False,
                "sortable": False,
                "filter": False,
            },
            columnDefs=[
                {
                    "field": "key",
                    "width": 120,
                    "cellStyle": {"fontWeight": "bold"},
                },
                {
                    "field": "value",
                    "flex": 1,
                },
            ],
            dashGridOptions={
                "rowSelection": "single",
                "animateRows": True,
                "suppressMaintainUnsortedOrder": True,
                "headerHeight": 0,
                "theme": "legacy",
            },
            className="ag-theme-balham-dark",
        )

        self.revenue_income = revenue_and_income.RevenueIncomeChart(app)
        self._register_callbacks()

    def layout(self):
        return dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            self.market_data,
                            width=4,
                        ),

                        dbc.Col(
                            [
                                dbc.Label(
                                    id="stock-name",
                                    className="text-end w-100"
                                ),
                                dbc.Label(id="stock-description"),
                                self.revenue_income.layout(),
                            ],
                            width=8,
                        ),
                    ],
                    className="p-3",
                ),
            ],
            fluid=True,
        )

    def _register_callbacks(self):

        @self.app.callback(
            Output("market-data", "rowData"),
            Output('stock-name', "children"),
            Output("stock-description", "children"),
            Input("stock-info-set", "data"),
            prevent_initial_call=True,
        )
        def update_market_data(stock_info_set):
            if not stock_info_set:
                raise dash.exceptions.PreventUpdate

            symbol = stock_info_set['symbol']
            market_data = stock_info_set['data'][symbol]['market_data']

            market_data_rows = []
            week_52 = market_data['52_week']
            ytd_data = market_data['ytd_data']
            price = market_data['price']
            open_close = market_data['open_close']

            financials = market_data.get('financials',{})

            #market_data_rows.append(
            #    {
            #        "key":"Name",
            #        "value": market_data['details']['name']
            #    }
            #)
            week_52_str = ""
            if 'low_52_week' in week_52 and 'high_52_week' in week_52:
                week_52_str = f"{week_52['low_52_week']} - {week_52['high_52_week']}"

            market_data_rows.append(
                {
                    "key":"52 Week Range",
                    "value": week_52_str
                }
            )

            ytd_str = ""
            if 'ytd_first_close' in ytd_data and 'ytd_last_close' in ytd_data:
                ytd_str = f"{ytd_data['ytd_first_close']} - {ytd_data['ytd_last_close']}"

            market_data_rows.append(
                {
                    "key":"YTD",
                    "value": ytd_str
                }
            )

            price_str = f"{price['real_time_price']} {price['price_change']} ({price['change_percent']}%)"
            market_data_rows.append(
                {
                    "key":"Price",
                    "value": price_str
                }
            )


            volume_str = f"{int(price['volume']):,}"
            market_data_rows.append(
                {
                    "key":"Volume",
                    "value": volume_str
                }
            )

            open_close_str = f"{open_close['prev_day_close']} - {open_close['today_open']}"
            market_data_rows.append(
                {
                    "key":"Open/Close",
                    "value": open_close_str
                }
            )

            if 'revenue' in financials:
                revenue_str = f"{format_number(financials['revenue'])}"
                market_data_rows.append(
                    {
                        "key":"Revenue",
                        "value": revenue_str
                    }
                )

            if 'net_income' in financials:
                net_income_str = f"{format_number(financials['net_income'])}"
                market_data_rows.append(
                    {
                        "key":"Net Income",
                        "value": net_income_str
                    }
                )

            if 'eps' in financials:
                eps_str = f"{round(financials['eps'],2)}"
                market_data_rows.append(
                    {
                        "key":"EPS",
                        "value": eps_str
                    }
                )

            name = symbol
            if 'name' in market_data['details']:
                name = market_data['details']['name']

            description = symbol
            if 'description' in market_data['details']:
                description = market_data['details']['description']


            return market_data_rows, name, description
