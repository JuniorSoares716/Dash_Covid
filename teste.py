import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input


data = pd.read_csv("brazil_covid19.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Titulo da Dashbord!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Titulo da Das", className="header-title"
                ),
                html.P(
                    children="Subtitulo aqui",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Região", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": Region, "value": Region}
                                for Region in np.sort(data.Region.unique())
                            ],
                            value='Centro-Oeste',
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Estado", className="menu-stados"),
                        dcc.Dropdown(
                            id="state-filter",
                            options=[
                                {"label": State, "value": State}
                                for State in np.sort(data.State.unique())
                            ],
                            value='DF',
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                 html.Div(
                    children=[
                        html.Div(
                            children="Data",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
                 ],
            className="menu",
        ),
        html.Div(
            children=[
                
                html.Div(
                    children=dcc.Graph(
                        id="volume-casos", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    [Output("volume-casos","figure")],
    [
        Input("region-filter", "region"),
        Input("state-filter", "state"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),

    ],
)
def update_charts(region, state, start_date, end_date):
    mask =(
        (data.Region == region)
        & (data.State == state)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
        
    )
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Cases"],
                "y": filtered_data["Region"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Casos",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }


    return [price_chart_figure]
    

if __name__ == "__main__":
    app.run_server(debug=True)
# print(app.title)



    # volume_chart_figure = {
    #     "data": [
    #         {
    #             "x": filtered_data["Date"],
    #             "y": filtered_data["Region"],
    #             "type": "lines",
    #         },
    #     ],
    #     "layout": {
    #         "title": {"text": "Total de Casos", "x": 0.05, "xanchor": "left"},
    #         "xaxis": {"fixedrange": True},
    #         "yaxis": {"fixedrange": True},
    #         "colorway": ["#E12D39"],
    #     },
    # }