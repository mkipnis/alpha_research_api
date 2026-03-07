# Copyright (c) Mike Kipnis (mike.kipnis@gmail.com) - Alpha Research Online

import logging

import dash_ag_grid as dag
from dash import html, dcc, Input, Output, dash
import dash_bootstrap_components as dbc

import requests

logger = logging.getLogger("EntityGrid")

class EntityGrid:
    def __init__(self, entity_grid_id: str, app: dash.Dash):
        self.app = app
        self.entity_grid_id = entity_grid_id

        self.entity_grid = dag.AgGrid(
                id=self.entity_grid_id,
                columnDefs=[],
                rowData=[],
                defaultColDef={"minWidth": 100, "resizable": False},
                style={"height": "290px", "width": "100%"},
                dashGridOptions={
                    "rowSelection": "single",
                    "animateRows": True,
                    "suppressMaintainUnsortedOrder": True,
                    "theme": "legacy"
                },
                className="ag-theme-balham-dark",
            )

        self._register_callbacks()

    def grid_id(self):
        return self.entity_grid_id

    def selected_items_id(self):
        return self.entity_grid_id+"_selected_entity"

    def api_settings_id(self):
        return self.entity_grid_id+"_api_settings"

    def layout(self):
            return dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                self.entity_grid,
                            ),
                            dcc.Store(id=self.entity_grid_id+"_api_settings"),
                ],
            )])

    def extract_value_data(self, values:dict):
        result = {}
        for date, v in values.items():
            if isinstance(v, dict) and v.get("value") is not None:
                try:
                    result[date] = int(v["value"])
                except (ValueError, TypeError):
                    pass  # skip non-numeric values
        return result

    def _register_callbacks(self):
        @self.app.callback(
            Output(self.entity_grid_id, "rowData"),
            Input(self.api_settings_id(), "data"),
            prevent_initial_call=True,
        )
        def setup_entity_grid(api_settings):
            logger.info(f"Retrieving data {api_settings}")

            end_point = api_settings['end_point']

            response = requests.post(url=api_settings['RAPID_API_URL'] + "/"+ end_point+"/", json=api_settings['payload'], headers=api_settings['headers'])
            values = response.json()
            if len(values) == 0:
                return dash.no_update, dash.no_update

            key = api_settings['key']
            values_list = []
            for sector_name, values in values.items():
                value = {}
                value[key] = sector_name
                value |= self.extract_value_data(values)
                values_list.append(value)

            return values_list

        @self.app.callback(
            Output(self.entity_grid_id, "selectedRows"),
            Input(self.entity_grid_id, "virtualRowData"),
            prevent_initial_call=True,
        )
        def select_first_row_after_sort(virtual_rows):
            if not virtual_rows:
                return dash.no_update

            # Select first row from sorted data
            return [virtual_rows[0]]

        @self.app.callback(
            Output(self.selected_items_id(), "data"),
            Input(self.entity_grid_id, "selectedRows"),
            prevent_initial_call=True,
        )
        def return_selected_row(selected_rows):
            if not selected_rows:
                return dash.no_update

            # Select first row from sorted data
            return [selected_rows[0]]
