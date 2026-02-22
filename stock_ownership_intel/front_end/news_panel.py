# Copyright (c) Mike Kipnis - Alpha Research Online

import dash
import dash_ag_grid as dag
from dash import Input, Output, html, dcc, State
import dash_bootstrap_components as dbc


class NewPanel(object):

    def __init__(self, app: dash.Dash):
        self.app = app
        self.news_panel = dag.AgGrid(
            id="news_panel",
            rowData=[],
            defaultColDef={
                "resizable": False,
                "sortable": False,
                "filter": False,
            },
            columnDefs=[
                {
                    "field": "timestamp",
                    "width": 200,
                },
                {
                    "field": "title",
                    "flex": 1,
                },
                {
                    "field": "url",
                    "hide":True
                },
                {
                    "field": "description",
                    "hide": True
                },

            ],
            dashGridOptions={
                "rowSelection": "single",
                "animateRows": True,
                "suppressMaintainUnsortedOrder": True,
                "theme": "legacy",
            },
            className="ag-theme-balham-dark",
        )

        self._register_callbacks()

    def layout(self):
        return dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            self.news_panel,
                        ),

                        dbc.Col(
                            [
                                dbc.Label(id="news-description"),
                            ],
                        ),
                    ],
                    className="p-3",
                ),
            ],
            fluid=True,
        )

    def _register_callbacks(self):

        @self.app.callback(
            Output("news_panel", "rowData"),
            Output("news_panel", "selectedRows"),
            Input("news-set", "data"),
            prevent_initial_call=True,
        )
        def update_news_data(news_set):
            if not news_set or len(news_set) == 0:
                raise dash.exceptions.PreventUpdate

            # Automatically select the first row
            first_row = news_set[0]
            return news_set, [first_row]

        @self.app.callback(
            Output("news-description", "children"),
            Input("news_panel", "selectedRows"),
            prevent_initial_call=True,
        )
        def show_description(selected_rows):
            if not selected_rows or len(selected_rows) == 0:
                return "Select a news item to see description"

            row = selected_rows[0]
            description = row.get("description", "")
            url = row.get("url", "")

            return html.Div([
                html.P(description),
                html.A("Read more", href=url, target="_blank", style={"color": "lightblue"})
            ])