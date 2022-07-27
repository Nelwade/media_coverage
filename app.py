from dash import dcc, html
from dash_bootstrap_templates import load_figure_template
from visualizer import plot_multibars

import dash_bootstrap_components as dbc
import dash
import pandas as pd
import datetime
import pytz
import os

app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])
server = app.server

load_figure_template("SKETCHY")

print("App Starting....")

last_updated = os.path.getmtime("data/totals_data.csv")
last_updated = datetime.datetime.fromtimestamp(last_updated, pytz.timezone("Africa/Nairobi")).strftime("%Y-%m-%d %H:%M")
#now = datetime.datetime.now(pytz.timezone("Africa/Nairobi")).strftime("%Y-%m-%d %H:%M")

df_totals = pd.read_csv("data/totals_data.csv")
df_nation = pd.read_csv("data/nat_data.csv")
df_std = pd.read_csv("data/std_data.csv")


fig1, fig2 = plot_multibars(df_totals, df_nation, df_std)

graphs = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig1), lg=6),
                dbc.Col(dcc.Graph(figure=fig2), lg=6),
            ],
            className="mt-4",
        ),
       
    ]
)

date = html.Div([
    html.Em(f"(Last Updated at : {last_updated} EAT)"),
])

content = html.Div([
    html.Br(),
    html.P("This website tracks the number of news articles that mention each of the main presidential candidates and their running mates. The data is collected from nation.africa and standardmedia.co.ke. All data is recorded from 21st July 2022."),
])

title = html.Title("Media Coverage of Kenya's Presidential Candidates")
heading = html.H1("Tracking Digital News Media Coverage of Kenya's Presidential Candidates", className="bg-primary text-white p-2")

footer = html.Div([
    html.Br(),
    html.Footer("Contact: o.owadenelson@gmail.com")
])

app.layout = dbc.Container([title, heading, date, content, graphs, footer], fluid=True)

if __name__ == "__main__":
    app.run(debug=True, port=8010, host='localhost')
