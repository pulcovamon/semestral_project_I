# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go

# Incorporate data
df = pd.read_csv('patients.csv')
data = df.to_dict("records")
id_list = [str(patient["id"]) for patient in data]
key_list = [key.replace("_", " ").upper() for key in data[0].keys() if key != "id" and key != "codes"]
data_list = [
    [
    patient[key] for patient in data
    ] for key in data[0].keys() if key != "id" and key != "codes"
]
map_values = [
    [
    1 if (i+j) % 2 == 0 else 0 for i in range(len(id_list))
    ] for j in range(len(key_list))
]

# Initialize the app
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "AI Prediction Map"

def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("AI Prediction Map"),
            html.H3("Welcome to the Medical AI Prediction Map Dashboard"),
        ],
    )

def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    values = [
        f"{id_list[i]}-{id_list[-1]}" if i+9 >= len(id_list) else f"{id_list[i]}-{id_list[i+9]}" for i in range(len(id_list)) if i % 10 == 0
    ]
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Patient IDs"),
            dcc.Dropdown(
                values, values[0], id="dropdown"
            ),
        ],
    )

def generate_heat_map():
    fig = go.Figure(data=go.Heatmap(
        z=map_values,
        y=key_list,
        x=id_list[0:10],
        text=data_list,
        colorscale=[[0, "#caf3ff"], [1, "#2c82ff"]],
        showscale=False,
        hovertemplate="<b> %{x}  %{y} <br><br> %{text}",
    ))
    fig.layout.height=600
    fig.layout.width=1000
    return dcc.Graph(figure=fig)

def initialize_prediction   ():
    # header_row
    patient_id = id_list[0]
    header = [
        generate_table_row(patient_id, ("", "Ground Truth", "Prediction"))
    ]
    keys = [("Active Phase", key_list[0], key_list[1]), ("ICD10 Binary", key_list[2], key_list[3]), ("ICD10 Multiclass", key_list[4], key_list[5])]
    rows = [generate_table_row(patient_id, key) for key in keys]
    header.extend(rows)
    empty_table = header

    return empty_table


def generate_table_row(patient_id, keys):
    """ Generate table rows.

    :param id: The ID of table row.
    :param style: Css style of this row.
    :param col1 (dict): Defining id and children for the first column.
    :param col2 (dict): Defining id and children for the second column.
    :param col3 (dict): Defining id and children for the third column.
    """

    return html.Div(
        id="row",
        className="row table-row",
        children=[
            html.Br(),
            html.Div(
                style={"display": "table", "height": "100%"},
                className="four columns row-department",
                children=html.P(keys[0])
            ),
            html.Div(
                style={"display": "table", "height": "100%"},
                className="four columns row-department",
                children=html.P(keys[1])
            ),
            html.Div(
                style={"display": "table", "height": "100%"},
                className="four columns row-department",
                children=html.P(keys[2])
            ),
        ],
    )


@callback(
    Output("heat_map", "children"),
    Input("dropdown", "value")
)
def update_heat_map(patient_ids):
    i = id_list.index(patient_ids.split("-")[0])
    x = id_list[i:] if i+10 >= len(id_list) else id_list[i:i+10]
    text = [
        [
            None if j+i > len(column) else column[j+i] for j in range(10)
        ] for column in data_list
    ]
    fig = go.Figure(data=go.Heatmap(
        z=map_values,
        y=key_list,
        x=x,
        text=data_list,
        colorscale=[[0, "#caf3ff"], [1, "#2c82ff"]],
        hovertemplate="<b> ID %{x}:  %{y} <br><br> %{text}",
        showscale=False
    ))
    fig.layout.height=600
    fig.layout.width=1000
    return [dcc.Graph(figure=fig)]

def generate_app_layout():
    app.layout = html.Div(
        id="app-container",
        children = [
            html.Div(
                id="banner",
                className="banner",
                children=[html.Img(src=app.get_asset_url("medical_ai_prediction.png")), description_card()],
            ),
            html.Div(
                id="left_column",
                className="four columns",
                children=[
                    html.Div(
                        children=[generate_control_card()]
                    ),
                    html.Br(),
                    html.Div(
                        id="prediction",
                        children=[
                            html.H6(f"Patient's ID: {id_list[0]}"),
                            html.Div(id="prediction_data", children=initialize_prediction()),
                            html.Hr(),
                            html.P("Codes"),
                            html.Div(children=html.P(data[0]["codes"]))],
                    ),
                ]
            ),            
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                html.Div(
                    id="heat_map",
                    children=[generate_heat_map()]
                )
            ]
        )
    ]
    )

# Run the app
if __name__ == '__main__':
    generate_app_layout()
    app.run(debug=True)
