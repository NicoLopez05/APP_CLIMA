import os
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import requests
import plotly.express as px

# ======== Config API (para Docker) ========
# Prioridad: API_URL > BACKEND_URL > valor por defecto (nombre del servicio docker)
API_URL = os.getenv("API_URL") or os.getenv("BACKEND_URL") or "http://agro_backend:8000"

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

app.layout = dbc.Container([
    dcc.Store(id="auth-status", data={"logged": False, "token": ""}),
    dcc.Store(id="refresh-trigger", data=0),
    dcc.Store(id="sensor-edit", data=None),   # Aquí guardamos el sensor seleccionado para edición
    html.Div(id="page-content"),

    # Modal para editar sensor
    dbc.Modal(
        [
            dbc.ModalHeader("Editar Sensor"),
            dbc.ModalBody([
                dbc.Input(id="edit-nombre", placeholder="Nombre", type="text", className="mb-2"),
                dbc.Input(id="edit-ubicacion", placeholder="Ubicación", type="text", className="mb-2"),
                dbc.RadioItems(
                    id="edit-tipo",
                    options=[
                        {"label": "Temperatura", "value": "temperatura"},
                        {"label": "Humedad", "value": "humedad"},
                        {"label": "Lluvia", "value": "lluvia"},
                    ],
                    value="temperatura",
                    inline=True,
                ),
                html.Br(),
                dbc.Checkbox(id="edit-activo", value=True, className="me-2"),
                html.Label("Activo"),
                dbc.Checkbox(id="edit-alerta", value=False, className="me-2 ms-4"),
                html.Label("Alertas habilitadas"),
                html.Br(),
                dcc.Dropdown(
                    id="edit-zona",
                    options=[{"label": z, "value": z} for z in ["Norte", "Centro", "Sur"]],
                    value="Norte",
                    clearable=False,
                    className="mb-2"
                ),
                dcc.Dropdown(
                    id="edit-cultivo",
                    options=[{"label": c, "value": c} for c in ["Maíz", "Trigo", "Soja"]],
                    value="Maíz",
                    clearable=False,
                    className="mb-2"
                ),
            ]),
            dbc.ModalFooter(
                dbc.Button("Guardar Cambios", id="save-edit-btn", color="primary"),
            ),
        ],
        id="edit-modal",
        is_open=False,
    )
], fluid=True)


def login_layout():
    return dbc.Row([
        dbc.Col([
            html.H2("AgroClima - Login / Registro"),
            dbc.Input(id="username", placeholder="Usuario", type="text", className="mb-2"),
            dbc.Input(id="password", placeholder="Contraseña", type="password", className="mb-2"),
            dbc.Button("Login", id="login-btn", color="primary", className="me-2"),
            dbc.Button("Registrar", id="register-btn", color="secondary"),
            html.Div(id="login-alert", className="mt-2"),
        ], width=4)
    ], justify="center")


def crud_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H3("Sensores agrícolas"), width=10),
            dbc.Col(dbc.Button("Logout", id="logout-btn", color="danger"), width=2)
        ]),
        dbc.Row([
            dbc.Col(dbc.Button("Actualizar", id="refresh-btn", color="info", className="mb-2"), width=3),
            dbc.Col(html.Div(id="sensor-table-alert"), width=9)
        ]),
        dash_table.DataTable(
            id="tabla-sensores",
            columns=[
                {"name": "id", "id": "id"},
                {"name": "nombre", "id": "nombre"},
                {"name": "tipo", "id": "tipo"},
                {"name": "ubicacion", "id": "ubicacion"},
                {"name": "activo", "id": "activo"},
                {"name": "alertas", "id": "alertas"},
                {"name": "zona", "id": "zona"},
                {"name": "cultivo", "id": "cultivo"},
                {"name": "editar", "id": "editar", "presentation": "markdown"},
                {"name": "eliminar", "id": "eliminar", "presentation": "markdown"},
            ],
            data=[],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            style_data_conditional=[
                {"if": {"column_id": "eliminar"}, "color": "red"},
                {"if": {"column_id": "editar"}, "color": "blue"}
            ],
            markdown_options={"html": True}
        ),
        html.Hr(),
        html.H4("Registrar nuevo sensor"),
        dbc.Form([
            dbc.Row([
                dbc.Col(dbc.Input(id="nombre-sensor", placeholder="Nombre", type="text"), width=4),
                dbc.Col(dbc.Input(id="ubicacion-sensor", placeholder="Ubicación", type="text"), width=4),
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.RadioItems(
                        id="tipo-sensor",
                        options=[
                            {"label": "Temperatura", "value": "temperatura"},
                            {"label": "Humedad", "value": "humedad"},
                            {"label": "Lluvia", "value": "lluvia"},
                        ],
                        value="temperatura",
                        inline=True,
                    ), width=8),
            ], className="mt-2"),
            dbc.Row([
                dbc.Col(dbc.Checkbox(id="activo-sensor", value=True, className="me-2"), width="auto"),
                dbc.Col(html.Label("Activo"), width="auto"),
                dbc.Col(dbc.Checkbox(id="alerta-sensor", value=False, className="me-2"), width="auto"),
                dbc.Col(html.Label("Alertas habilitadas"), width="auto"),
            ], className="mt-2"),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id="zona-sensor",
                        options=[{"label": z, "value": z} for z in ["Norte", "Centro", "Sur"]],
                        value="Norte",
                        clearable=False
                    ), width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id="cultivo-sensor",
                        options=[{"label": c, "value": c} for c in ["Maíz", "Trigo", "Soja"]],
                        value="Maíz",
                        clearable=False
                    ), width=4),
            ], className="mt-2"),
            dbc.Button("Registrar Sensor", id="add-sensor-btn", color="success", className="mt-2"),
            html.Div(id="add-sensor-alert", className="mt-2")
        ]),
        html.Hr(),
        html.H5("Resumen por tipo de sensor"),
        dcc.Graph(id="sensor-bar"),
        html.H5("Resumen por tipo de cultivo"),
        dcc.Graph(id="sensor-cultivo-bar"),
    ], fluid=True)


@app.callback(
    Output("page-content", "children"),
    Input("auth-status", "data"),
)
def render_page(auth_status):
    if auth_status.get("logged"):
        return crud_layout()
    return login_layout()


@app.callback(
    Output("auth-status", "data", allow_duplicate=True),
    Output("login-alert", "children", allow_duplicate=True),
    Input("login-btn", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True,
)
def login_user(login_clicks, username, password):
    if not username or not password:
        return dash.no_update, dbc.Alert("Completa usuario y contraseña", color="danger")
    resp = requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password})
    if resp.status_code == 200:
        return {"logged": True, "token": resp.json().get("access_token", "")}, None
    return dash.no_update, dbc.Alert("Login inválido", color="danger")


@app.callback(
    Output("auth-status", "data"),
    Input("logout-btn", "n_clicks"),
    prevent_initial_call=True
)
def logout_user(n):
    return {"logged": False, "token": ""}


@app.callback(
    Output("login-alert", "children"),
    Input("register-btn", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def register_user(n, username, password):
    if not username or not password:
        return dbc.Alert("Completa usuario y contraseña para registrar", color="warning")
    resp = requests.post(f"{API_URL}/auth/register", json={"username": username, "password": password})
    if resp.status_code in (200, 201):
        return dbc.Alert("Registro exitoso. Ahora puedes hacer login.", color="success")
    return dbc.Alert("Usuario ya existe o error al registrar.", color="danger")


@app.callback(
    Output("tabla-sensores", "data"),
    Output("sensor-bar", "figure"),
    Output("sensor-cultivo-bar", "figure"),
    Input("refresh-btn", "n_clicks"),
    Input("refresh-trigger", "data"),
    prevent_initial_call=True
)
def refresh_table(n, refresh_trigger):
    resp = requests.get(f"{API_URL}/sensores/")
    data = []
    fig_tipo = px.bar(title="No hay sensores para mostrar")
    fig_cultivo = px.bar(title="No hay sensores para mostrar")
    if resp.status_code == 200:
        data = resp.json() or []
        if data:
            for row in data:
                row["editar"] = f"[✏️](#edit-{row['id']})"
                row["eliminar"] = f"[🗑️](#del-{row['id']})"
            tipo_counts = {}
            cultivo_counts = {}
            for s in data:
                tipo_counts[s["tipo"]] = tipo_counts.get(s["tipo"], 0) + 1
                cultivo_counts[s["cultivo"]] = cultivo_counts.get(s["cultivo"], 0) + 1
            fig_tipo = px.bar(x=list(tipo_counts.keys()), y=list(tipo_counts.values()),
                              labels={'x': 'Tipo de sensor', 'y': 'Cantidad'},
                              title="Cantidad de sensores por tipo")
            fig_cultivo = px.bar(x=list(cultivo_counts.keys()), y=list(cultivo_counts.values()),
                                 labels={'x': 'Tipo de cultivo', 'y': 'Cantidad'},
                                 title="Cantidad de sensores por tipo de cultivo")
    return data, fig_tipo, fig_cultivo


# Alta de sensor
@app.callback(
    Output("add-sensor-alert", "children"),
    Output("refresh-trigger", "data", allow_duplicate=True),
    Input("add-sensor-btn", "n_clicks"),
    State("nombre-sensor", "value"),
    State("tipo-sensor", "value"),
    State("ubicacion-sensor", "value"),
    State("activo-sensor", "value"),
    State("alerta-sensor", "value"),
    State("zona-sensor", "value"),
    State("cultivo-sensor", "value"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True
)
def add_sensor(n, nombre, tipo, ubicacion, activo, alerta, zona, cultivo, refresh_data):
    if not nombre or not ubicacion:
        return dbc.Alert("Completa todos los campos obligatorios", color="warning"), refresh_data
    payload = {
        "nombre": nombre,
        "tipo": tipo,
        "ubicacion": ubicacion,
        "activo": bool(activo),
        "alertas": bool(alerta),
        "zona": zona,
        "cultivo": cultivo
    }
    resp = requests.post(f"{API_URL}/sensores/", json=payload)
    if resp.status_code == 200:
        return dbc.Alert("Sensor registrado correctamente.", color="success"), refresh_data + 1
    return dbc.Alert("Error al registrar sensor.", color="danger"), refresh_data


# Eliminar / Editar sensor (ahora también actualiza el Store 'sensor-edit')
@app.callback(
    Output("refresh-trigger", "data"),
    Output("sensor-table-alert", "children"),
    Output("sensor-edit", "data", allow_duplicate=True),
    Input("tabla-sensores", "active_cell"),
    State("tabla-sensores", "data"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True
)
def delete_edit_sensor(active_cell, data, refresh_data):
    if not active_cell:
        raise dash.exceptions.PreventUpdate
    column = active_cell.get("column_id")
    row_idx = active_cell.get("row")
    if row_idx is None or row_idx >= len(data):
        raise dash.exceptions.PreventUpdate

    if column == "eliminar":
        sensor_id = data[row_idx]["id"]
        resp = requests.delete(f"{API_URL}/sensores/{sensor_id}")
        if resp.status_code == 200:
            return refresh_data + 1, dbc.Alert("Sensor eliminado.", color="success"), dash.no_update
        return refresh_data, dbc.Alert("Error al eliminar sensor.", color="danger"), dash.no_update

    if column == "editar":
        sensor = data[row_idx]
        return refresh_data, dash.no_update, sensor

    raise dash.exceptions.PreventUpdate


# Abrir modal de edición cuando cambia el store sensor-edit
@app.callback(
    Output("edit-modal", "is_open"),
    Output("edit-nombre", "value"),
    Output("edit-ubicacion", "value"),
    Output("edit-tipo", "value"),
    Output("edit-activo", "value"),
    Output("edit-alerta", "value"),
    Output("edit-zona", "value"),
    Output("edit-cultivo", "value"),
    Input("sensor-edit", "data"),
    prevent_initial_call=True,
)
def open_edit_modal(sensor):
    if not sensor:
        return False, None, None, None, None, None, None, None
    return True, sensor["nombre"], sensor["ubicacion"], sensor["tipo"], sensor["activo"], sensor["alertas"], sensor["zona"], sensor["cultivo"]


# Guardar cambios del sensor editado
@app.callback(
    Output("refresh-trigger", "data", allow_duplicate=True),
    Output("edit-modal", "is_open", allow_duplicate=True),
    Input("save-edit-btn", "n_clicks"),
    State("sensor-edit", "data"),
    State("edit-nombre", "value"),
    State("edit-ubicacion", "value"),
    State("edit-tipo", "value"),
    State("edit-activo", "value"),
    State("edit-alerta", "value"),
    State("edit-zona", "value"),
    State("edit-cultivo", "value"),
    State("refresh-trigger", "data"),
    prevent_initial_call=True
)
def save_edit_sensor(n, sensor, nombre, ubicacion, tipo, activo, alerta, zona, cultivo, refresh_data):
    if not sensor or not nombre or not ubicacion:
        return refresh_data, False
    payload = {
        "nombre": nombre,
        "tipo": tipo,
        "ubicacion": ubicacion,
        "activo": bool(activo),
        "alertas": bool(alerta),
        "zona": zona,
        "cultivo": cultivo
    }
    sensor_id = sensor["id"]
    resp = requests.put(f"{API_URL}/sensores/{sensor_id}", json=payload)
    if resp.status_code == 200:
        return refresh_data + 1, False
    return refresh_data, False


# ======== Run (solo esto al final) ========
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8058"))  # debe coincidir con docker-compose (ports)
    app.run(host="0.0.0.0", port=port, debug=False)
