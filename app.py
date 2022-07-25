from dash import dcc, html
from dash_bootstrap_templates import load_figure_template
from visualizer import plot_multibars

import dash_bootstrap_components as dbc
import dash
import pandas as pd
import datetime
import pytz


app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])
server = app.server

load_figure_template("SKETCHY")

print("App Starting....")

now = datetime.datetime.now(pytz.timezone("Africa/Nairobi")).strftime("%Y-%m-%d %H:%M")

df_totals = pd.read_csv("data/totals_data.csv")
df_nation = pd.read_csv("data/nat_data.csv")
df_std = pd.read_csv("data/std_data.csv")


fig1, fig2 = plot_multibars(df_totals, df_nation, df_std)

app.layout= html.Div([
    html.H1("Tracking Digital Media Coverage of Presidential Candidates"),
    #html.H5("(Articles are counted from nation.africa and standardmedia.co.ke)"),
    html.Em(f"(Last Updated at : {now} EAT)"),
    html.Br(),
    html.Br(),
    html.P("This website tracks, in real-time, the number of articles that mention each of the main presidential candidates and their running mates. The data is collected from nation.africa and standardmedia.co.ke."),
    html.P("All data is recorded from 21st July 2022."),
    dcc.Graph(id= 'graph', figure=fig1),
    html.Br(),
    html.Br(),
    dcc.Graph(id= 'graph2', figure=fig2),
    html.Br(),
    html.Br(),
    html.Br(),
    html.P("For any queries reach out through o.owadenelson@gmail.com.")
    ])

if __name__ == "__main__":
    app.run(debug=True, port=8010, host='localhost')
