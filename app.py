# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go


# Incorporate data
df = pd.read_csv('patients.csv')
data = df.to_dict("records")
value_dict_multiclas = {"0": "C340", "1": "C341", "2": "C342", "3": "C343", "4": "C348", "5": "C349", "6": "other"}
value_dict_binary = {"1": "C34", "0": "other"}
id_list = [str(patient["id"]) for patient in data]
key_list = [key for key in data[0].keys() if key != "id" and key != "codes"]
key_list_show = [key.replace("_", " ").upper() for key in key_list]
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
    return html.Div(
        id="description-card",
        children=[
            html.H5("AI Prediction Map"),
            html.H3("Welcome to the Lung Cancer Patients Catalog"),
        ],
    )

def generate_control_card():
    return html.Div(
        id="control-card",
        children=[
            dcc.RadioItems(options=[
                {"label": html.Span("1 patient detail", style={"font-family": "Courier New, monospace"}),
                "value": 1},
                {"label": html.Span("10 patients overview", style={"font-family": "Courier New, monospace"}),
                "value": 0}
                ], labelStyle={"display": "flex", "align-items": "center"}, 
                value=1, id="radio_button"),
            html.Br(),
            html.Div(
                id="dropdown_menu",
                children=[html.H5("Select Patient ID"), dcc.Dropdown(options=id_list, value=id_list[0], id="dropdown")]
            )
        ],
    )

def generate_heat_map(current_id_list, text):
    fig = go.Figure(data=go.Heatmap(
        z=map_values,
        y=key_list_show,
        x=current_id_list,
        text=text,
        colorscale=[[0, "#b9e9f5"], [1, "#00a3cc"]],
        showscale=False,
        hovertemplate="<b> %{x}  %{y} <br><br> %{text}",
    ))
    fig.layout.height=500
    fig.layout.width=1000
    fig.update_layout(xaxis={"title": "Patient IDs"},
                      margin={"r":0,"t":0,"l":0,"b":0},
                      font=dict(family="Courier New, monospace", size=14),
                      paper_bgcolor="#daf3ff")
    return [html.H6(f"Patiets IDs: {current_id_list[0]}-{current_id_list[-1]}  - Map of Codes"), dcc.Graph(id="heat_map", figure=fig)]


def parse_codes_into_list(key, index):
        if key == "icd10_binary_prediction":
            return [value_dict_binary[i] for i in data[index][key].replace("]", "").replace("[", "").replace("'", "").split(", ")]
        if key == "icd10_multiclass_prediction":
            return [value_dict_multiclas[i] for i in data[index][key].replace("]", "").replace("[", "").replace("'", "").split(", ")]
        return [i for i in data[index][key].replace("]", "").replace("[", "").replace("'", "").split(", ")]


def parse_codes_into_str(key, index):
    return ", ".join(parse_codes_into_list(key, index))


def get_index(patient_id):
    index = int(patient_id)
    while index >= len(id_list) or patient_id != id_list[index]:
        index-=1
    return index


def generate_one_patient_map(patient_id):
    index = get_index(patient_id if patient_id.isnumeric() else id_list[0])
    show_data = [parse_codes_into_list(key, index) for key in key_list]
    keys_to_show = ["ICD10 BINARY", "ICD10 MULTICLASS", "ACTIVE PHASE"]
    show_data = [
        [[show_data[i][j], show_data[i+1][j]] for j in range(len(show_data[i]))] for i in range(0, 6, 2)
    ]
    z_values = [
        [1 if code[0] == code[1] else 0 for code in code_list] for code_list in show_data
    ]
    colorscale = [[0, "#d3886b"], [1, " #aed36b"]]
    if not any(1 in value for value in z_values):
        colorscale = [[0, "#aed36b"], [1, " #aed36b"]]
    elif not any(0 in value for value in z_values):
        colorscale = [[0, "#aed36b"], [1, " #aed36b"]]
    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        y=keys_to_show,
        x=[str(i) for i in range(min(max([len(i) for i in show_data]), 5))],
        text=show_data,
        texttemplate="prediction: <b>%{text[0]}</b><br>ground truth: <b>%{text[1]}</b>",
        hoverinfo="skip",
        colorscale=colorscale,
        showscale=False,
        textfont={"size": 13},
    ))
    fig.layout.height=600
    fig.layout.width=1000
    fig.update_layout(xaxis={"title": "Code Indices"},
                      font=dict(family="Courier New, monospace", size=14),
                      margin={"r":0,"t":0,"l":0,"b":0},
                      paper_bgcolor="#daf3ff")
    return [html.H6(f"Patient ID: {patient_id} - Map of Codes"), dcc.Graph(id="heat_map", figure=fig)]


def initialize_prediction(index):
    header = [
        generate_table_row(("", "Ground Truth", "Prediction"))
    ]
    keys = [("Active Phase", parse_codes_into_str(key_list[0], index), parse_codes_into_str(key_list[1], index)),
             ("ICD10 Binary", parse_codes_into_str(key_list[2], index), parse_codes_into_str(key_list[3], index)),
             ("ICD10 Multiclass", parse_codes_into_str(key_list[4], index), parse_codes_into_str(key_list[5], index))]
    rows = [generate_table_row(key) for key in keys]
    header.extend(rows)
    empty_table = header

    return empty_table


def generate_table_row(keys):
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


def generate_app_layout():
    app.layout = html.Div(
        id="app-container",
        children = [
            html.Div(
                id="banner",
                className="banner",
                children=[html.Img(src=app.get_asset_url("medical_ai_prediction.png"), id="app_icon"), description_card()],
            ),
            html.Div(
                id="left_column",
                className="four columns",
                children=[
                    html.Br(),
                    html.Div(
                        children=[generate_control_card()]
                    ),
                    html.Br(),
                    html.Div(id="prediction"),
                ]
            ),            
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                html.Br(),
                html.Div(
                    id="patient_card",
                    children=[
                        html.P("Patiet Map"),
                        dcc.Graph(id="heat_map")
                    ]
                )
            ]
        )
    ]
    )
    

@app.callback(
    Output("dropdown_menu", "children"),
    Input("radio_button", "value")
)
def update_dropdown(option):
    if option == 0:
        values = [f"{id_list[i]}-{id_list[-1]}" if i+9 >= len(id_list) else f"{id_list[i]}-{id_list[i+9]}" for i in range(len(id_list)) if i % 10 == 0]
        return [html.P("Select Range of Patients IDs"), dcc.Dropdown(options=values, value=values[0], id="dropdown")]
    return [html.P("Select Patient ID"), dcc.Dropdown(options=id_list, value=id_list[0], id="dropdown")]


@app.callback(
    Output("patient_card", "children"),
    [
        Input("radio_button", "value"),
        Input("dropdown", "value")
    ]
)
def update_heat_map(option, value):
    if option == 0:
        i = id_list.index(value.split("-")[0])
        x = id_list[i:] if i+10 >= len(id_list) else id_list[i:i+10]
        text = [
            [
                None if j+i > len(column) else column[j+i] for j in range(10)
            ] for column in data_list
        ]
        return generate_heat_map(x, text)
    return generate_one_patient_map(value)


@app.callback(
    Output("prediction", "children"),
    [
        Input("heat_map", "clickData"),
        Input("radio_button", "value"),
        Input("dropdown", "value")
    ]
)
def uprate_prediction_table(patient, option, value):
    if option == 0:
        patient_id = id_list[0] if not patient else patient["points"][0]["x"]
    else:
        patient_id = value if value.isnumeric() else id_list[0]
    index = get_index(patient_id)
    return [html.H6(f"Patient's ID: {id_list[index]}"),
            html.Div(children=initialize_prediction(index)),
            html.Hr(),
            html.Div(children=[html.P("Codes"), html.P(data[index]["codes"])])]


# Run the app
if __name__ == '__main__':
    generate_app_layout()
    app.run(debug=True)