# Copyright (c) Mike Kipnis - Alpha Research Online

import os
import logging
from datetime import datetime, timedelta

import dash
import dash_bootstrap_components as dbc
import requests
from dash import html, dcc, Input, Output, State

import entity_grid
import market_data
import news_panel
import price_chart

import dash_ag_grid as dag

API_SETTINGS = {
    #"RAPID_API_URL": "http://localhost:8080",
    "RAPID_API_URL": "https://stock-ownership-intel.p.rapidapi.com/",
    "payload": "{}",
    "headers": {
        "x-rapidapi-key": "RAPID_API_KEY",
        "X-RapidAPI-Host": "stock-ownership-intel.p.rapidapi.com",
        "Content-Type": "application/json"
    }
}

# ----------------------------
# Logging configuration
# ----------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("stock_ownership_intel_adapter.log", "a"),
    ],
)

logger = logging.getLogger("StockOwnershipIntel")

# ----------------------------
# LiquiBook Sandbox class
# ----------------------------
class StockOwnershipIntel:
    def __init__(self, app: dash.Dash):
        self.app = app

        self.sector = entity_grid.EntityGrid("sector-list", self.app)
        self.industry = entity_grid.EntityGrid("industry-list", self.app)
        self.institution = entity_grid.EntityGrid("institution-list", self.app)
        self.stock = entity_grid.EntityGrid("stock-list", self.app)

        self.price_chart = price_chart.PriceChart(self.app)
        self.market_data = market_data.MarketData(self.app)
        self.news_panel = news_panel.NewPanel(self.app)

    def layout(self):
        return dbc.Container(
            [
                dbc.Navbar(
                    dbc.Container(
                        [
                            # Left side
                            dbc.NavbarBrand(
                                "Stock Ownership Intel",
                                href="#",
                                style={"fontSize": "20px"},
                            ),

                            # Right side
                            html.Div(
                                [
                                    dbc.Row(
                                        [
                                            dcc.Store(
                                                id="rapid-api-key",
                                                storage_type="local",
                                            ),

                                            dbc.Col(
                                                html.A(
                                                    "https://rapitapi.com",
                                                    href="https://rapidapi.com/mikekipnis/api/stock-ownership-intel",
                                                    className="text-info mt-2",
                                                    style={"display": "block", "fontSize": "14px"},
                                                ),

                                            ),
                                            dbc.Col(
                                                dcc.Input(
                                            id="api-input",
                                        type="text",
                                        placeholder="RAPID API TOKEN",
                                        debounce=True,
                                        style={
                                            "width": "300px",
                                            "backgroundColor": "transparent",
                                            "color": "white",
                                            "border": "1px solid #6c757d",
                                        },
                                        className="me-2",
                                    ),
                                    ),
                                        ]
                                    ),

                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Div(
                                                    id="rapid-api-warning",
                                                    style={
                                                        "color":"#f09d08",
                                                        "marginTop": "10px",
                                                        "fontSize": "14px",
                                                    },
                                                ),
                                            ),
                                        ]
                                    ),

                                    html.Div(id="status", className="text-white ms-2"),
                                ],
                                className="d-flex flex-column align-items-start ms-auto",
                            ),
                        ],
                        fluid=True,
                    ),
                    color="#0f2538",
                    dark=True,
                ),

                html.Div(
                    [
                dbc.Accordion(
                    [

                        # --- Sector / Industry ---
                        dbc.AccordionItem(
                            dbc.Row(
                                [
                                    dbc.Col(self.sector.layout()),
                                    dcc.Store(id=self.sector.selected_items_id()),

                                    dbc.Col(self.industry.layout()),
                                    dcc.Store(id=self.industry.selected_items_id()),
                                ],
                                className="p-3",
                            ),
                            title="Sector & Industry",
                            item_id="sector-industry",
                        ),

                        # --- Institution / Stock ---
                        dbc.AccordionItem(
                            dbc.Row(
                                [
                                    dbc.Col(self.institution.layout()),
                                    dcc.Store(id=self.institution.selected_items_id()),

                                    dbc.Col(self.stock.layout()),
                                    dcc.Store(id=self.stock.selected_items_id()),
                                ],
                                className="p-3",
                            ),
                            title="Institution & Stock",
                            item_id="institution-stock",
                        ),

                        # --- Price Chart / Market Data ---
                        dbc.AccordionItem(
                            dbc.Row(
                                [
                                    dcc.Store(id="stock-info-set"),

                                    # Left column: Price Chart
                                    dbc.Col(
                                        self.price_chart.layout(),
                                        width=6,  # takes half the row
                                        className="d-flex flex-column",
                                    ),

                                    # Right column: Market Data
                                    dbc.Col(
                                        self.market_data.layout(),
                                        width=6,  # takes half the row
                                        className="d-flex flex-column",
                                    ),
                                ],
                                className="p-3 flex-nowrap",  # flex-nowrap keeps them on the same row
                                style={"overflowX": "auto"},  # optional: allows horizontal scroll if content is wide
                                # no_gutters=True  # older versions of dash-bootstrap-components
                            ),
                            title="Price Chart & Market Data",
                        ),

                        # --- News ---
                        dbc.AccordionItem(
                            dbc.Row(
                                [
                                    dcc.Store(id="news-set"),
                                    dbc.Col(self.news_panel.layout()),
                                ],
                                className="p-3",
                            ),
                            title="News",
                        ),

                    ],
                    id="main-accordion",
                    start_collapsed=False,  # all collapsed on load
                    flush=True,  # cleaner look
                    always_open=True,  # allow multiple open at once
                    active_item=["sector-industry", "institution-stock"],
                )], id="accordion-wrapper",),

                html.Div(
                    [
                        "For support, contact: ",
                        html.A(
                            "mike.kipnis@gmail.com",
                            href="mailto:mike.kipnis@gmail.com",
                            style={
                                "textDecoration": "underline",
                                "color": "#AAAAAA",
                            },
                        ),
                    ],
                    style={
                        "fontSize": "12px",
                        "color": "#AAAAAA",
                        "marginTop": "8px",
                        "textAlign": "center",
                        "width": "100%",
                    },
                ),

                dcc.Interval(id="startup", n_intervals=0, max_intervals=1),
                dcc.Store(id="report_dates"),

            ],
            fluid=True,
            className="p-0",
        )
# =============================
# Dash App Initialization
# =============================
app = dash.Dash(
    __name__,
    title="Stock Ownership Intel",
    external_stylesheets=[dag.themes.BASE, dag.themes.BALHAM, dbc.themes.SUPERHERO],
)

server = app.server  # Gunicorn expects this

# ---------------------------
# Layout & Callback setup
# ---------------------------

# Create sandbox with this prefix
soi = StockOwnershipIntel(app)

# Set layout once
app.layout = soi.layout

@app.callback(
    Output("rapid-api-key", "data"),
    Input("api-input", "value"),
    prevent_initial_call=True,
)
def save_api_key(value):
    return value

@app.callback(
    Output("api-input", "value"),
    Output("rapid-api-warning", "children"),
    Input("api-input", "id"),  # fires once
    State("rapid-api-key", "data"),
)
def load_api_key(_, stored):
    if stored:
        return stored, dash.no_update
    return dash.no_update, "Please obtain the RAPID_API_KEY from the link above"

@app.callback(
    Output("accordion-wrapper", "style"),
    Input("stock-info-set", "data"),
    Input("stock-list", "selectedRows"),
)
def block_ui(stock_info_set,stock_list):

    if dash.ctx.triggered_id == "stock-list":
        return {"pointerEvents": "auto", "opacity": 1}
    return {
        "pointerEvents": "none",  # blocks all clicks
        "opacity": 0.5,           # visually greyed out
    }

@app.callback(
    Output("report_dates","data"),
    Input("rapid-api-key", "data"),
)
def setup_filing_dates(rapid_api_key):

    if rapid_api_key is None:
        return dash.no_update

    logger.info(f"Retrieving filing dates: key {rapid_api_key}")

    API_SETTINGS['headers']['x-rapidapi-key'] = rapid_api_key
    response = requests.post(url=API_SETTINGS['RAPID_API_URL'] + "/filing_dates/", json=API_SETTINGS['payload'], headers=API_SETTINGS['headers'])
    filing_dates = response.json()

    return filing_dates

@app.callback(
    Output("sector-list", "columnDefs"),
    Output("industry-list", "columnDefs"),
    Output("institution-list", "columnDefs"),
    Output("stock-list", "columnDefs"),
    Input("report_dates", "data")
)
def setup_grids(report_dates):

    BASE_LEFT_COL = {
        "minWidth": 60,
        "cellStyle": {"textAlign": "left", "color": "#70b676"},
        "pinned": "left",
        "lockPinned": True,
        "suppressMovable": True,
        "sortable": True,
    }

    def build_columns(left_field: str, filing_dates, left_width: int = 200):
        # Left pinned column
        columns = [
            {**BASE_LEFT_COL, "field": left_field, "width": left_width}
        ]

        # Date columns
        for i, filing_date in enumerate(filing_dates):
            col_def = {
                "field": filing_date,
                "width": 100,
                "minWidth": 100,
                "maxWidth": 100,
                "resizable": False,
                "sortable": True,
                "cellStyle": {"textAlign": "right"},
                "valueFormatter": {
                    "function": """
                        params.value != null
                            ? (Math.abs(params.value) >= 1e9
                                ? (params.value / 1e9).toFixed(2) + 'B'
                                : Math.abs(params.value) >= 1e6
                                    ? (params.value / 1e6).toFixed(2) + 'M'
                                    : Math.abs(params.value) >= 1e3
                                        ? (params.value / 1e3).toFixed(1) + 'K'
                                        : params.value.toLocaleString()
                              )
                            : ''
                    """
                }
            }

            # Apply initial sort ONLY to first filing_date column
            if i == 0:
                col_def["sort"] = "desc"  # change to "asc" if needed

            columns.append(col_def)

        return columns

    # Ensure report_dates is valid list
    if not report_dates:
        raise dash.exceptions.PreventUpdate

    # Convert to strings (safety)
    report_dates = [str(d) for d in report_dates]

    sector_columns = build_columns("sector", report_dates, 200)
    industry_columns = build_columns("industry", report_dates, 200)
    institution_columns = build_columns("institution", report_dates, 200)
    stock_columns = build_columns("stock", report_dates, 80)

    return sector_columns, industry_columns, institution_columns, stock_columns


@app.callback(
    Output(soi.sector.api_settings_id(), "data"),
    Input("sector-list", "columnDefs"),
)
def setup_sectors(_):
    logger.info(f"Retrieving Sectors")
    API_SETTINGS['end_point'] = "sector_values"
    API_SETTINGS['key'] = "sector"

    return API_SETTINGS

@app.callback(
    Output(soi.industry.api_settings_id(), "data"),
    Input(soi.sector.selected_items_id(), "data"),
    prevent_initial_callback = True
)
def setup_industries(selected_sector):

    if selected_sector is None:
        raise dash.exceptions.PreventUpdate

    logger.info(f"Retrieving Sectors {selected_sector}")

    payload = {}
    payload['sector'] = selected_sector[0]['sector']

    API_SETTINGS['payload'] = payload
    API_SETTINGS['end_point'] = "industry_values"
    API_SETTINGS['key'] = "industry"

    return API_SETTINGS

@app.callback(
    Output(soi.institution.api_settings_id(), "data"),
    Input(soi.industry.selected_items_id(), "data"),
)
def setup_institution(selected_industry):

    # Strong guard against invalid selection states
    if selected_industry is None:
        raise dash.exceptions.PreventUpdate

    industry = selected_industry[0]["industry"]

    payload = {
        "industry": industry
    }

    API_SETTINGS['payload'] = payload
    API_SETTINGS['end_point'] = "holdings_for_industry"
    API_SETTINGS['key'] = "institution"

    return API_SETTINGS


@app.callback(
    Output(soi.stock.api_settings_id(), "data"),
    Input(soi.industry.selected_items_id(), "data"),
    Input(soi.institution.selected_items_id(), "data"),
)
def setup_symbols(selected_industry, selected_institution):

    # Guard against empty or intermediate selection events
    if (
        not selected_industry
        or not selected_institution
        or "industry" not in selected_industry[0]
        or "institution" not in selected_institution[0]
    ):
        raise dash.exceptions.PreventUpdate

    payload = {}
    payload['industry'] = selected_industry[0]['industry']
    payload['institution'] = selected_institution[0]['institution']

    API_SETTINGS['payload'] = payload
    API_SETTINGS['end_point'] = "holdings_for_institution_and_industry"
    API_SETTINGS['key'] = "stock"

    return API_SETTINGS

@app.callback(
    Output("stock-info-set", "data"),
    Output("news-set", "data"),
    Input("stock-list", "selectedRows"),
)
def setup_symbols(selected_stock):
    if not selected_stock:
        return [], []

    # Ignore rowIndex-only selection event
    if "stock" not in selected_stock[0]:
        raise dash.exceptions.PreventUpdate

    payload = {}
    payload['tickers'] = ['SPY', selected_stock[0]['stock']]

    today = datetime.today()
    one_year_ago = today - timedelta(days=365)

    payload['start_date'] = one_year_ago.strftime("%Y%m%d")
    payload['end_date'] = today.strftime("%Y%m%d")

    try:
        response = requests.post(url=API_SETTINGS['RAPID_API_URL'] + "/security_info/", json=payload, headers=API_SETTINGS['headers'])
        response = response.json()
    except:
        return [], []

    chart_data = {}
    chart_data['index'] = 'SPY'
    chart_data['symbol'] = selected_stock[0]['stock']
    chart_data['data'] = response['data']

    #for news in response['news'][chart_data['symbol']]:
    #    print(news)
    news = response['news'][chart_data['symbol']]

    return chart_data, news


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    host = os.getenv("DASH_HOST", "127.0.0.1")
    port = int(os.getenv("DASH_PORT", "8050"))
    debug = os.getenv("DASH_DEBUG", "true").lower() == "true"

    app.run(host=host, port=port, debug=debug, use_reloader=False)
