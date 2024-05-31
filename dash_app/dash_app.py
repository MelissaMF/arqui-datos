import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import requests

# URL de la API Flask
API_URL = "http://127.0.0.1:5000/toneladas_transferidas"

def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        return pd.DataFrame()  # Devuelve un DataFrame vacío si hay un error

# Obtener los datos de la API
df = fetch_data()

# Crear la aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Visualización de Toneladas Transferidas"),
    dcc.Dropdown(
        id='ep-dropdown',
        options=[{'label': ep, 'value': ep} for ep in df['ep'].unique()],
        value=df['ep'].unique()[0]
    ),
    dcc.Graph(id='toneladas-graph'),
    dcc.Graph(id='tipo-carga-graph')
])

@app.callback(
    Output('toneladas-graph', 'figure'),
    Input('ep-dropdown', 'value')
)
def update_toneladas_graph(selected_ep):
    filtered_df = df[df['ep'] == selected_ep]
    fig = px.line(filtered_df, x='mes', y='toneladas', color='año',
                  title=f"Evolución de toneladas transferidas por {selected_ep}")
    return fig

@app.callback(
    Output('tipo-carga-graph', 'figure'),
    Input('ep-dropdown', 'value')
)
def update_tipo_carga_graph(selected_ep):
    filtered_df = df[df['ep'] == selected_ep]
    fig = px.bar(filtered_df, x='mes', y='toneladas', color='tipo_carga', barmode='group',
                 title=f"Toneladas transferidas por tipo de carga para {selected_ep}")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
