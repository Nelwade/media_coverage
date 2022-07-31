from dash import dcc, html
from dash_bootstrap_templates import load_figure_template
from visualizer import plot_multibars, line_graph

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
fig3 = line_graph(df_nation, "Nation Africa")
fig4 =  line_graph(df_std, "Standard Media")
fig5 = line_graph(df_totals, "Totals")

# app.html_layout = """<!DOCTYPE html>
# <html>
#     <head>
        
#             <!-- Google Tag Manager -->
#         <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
#         new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
#         j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
#         'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
#         })(window,document,'script','dataLayer','GTM-MMPZZVX');</script>
#         <!-- End Google Tag Manager -->
# </head>

# """ 
app.index_string = """<!DOCTYPE html>
<html>
    <head>
                <!-- Google Tag Manager -->
        <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
        new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })(window,document,'script','dataLayer','GTM-MMPZZVX');</script>
        <!-- End Google Tag Manager -->
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1792676010155720"
        crossorigin="anonymous"></script>
        {%metas%}
        <title>Media Coverage of Kenya's Presidential Candidates</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
                <!-- Google Tag Manager (noscript) -->
        <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MMPZZVX"
        height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        <!-- End Google Tag Manager (noscript) -->
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

graphs = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig1), lg=6),
                dbc.Col(dcc.Graph(figure=fig2), lg=6),
            ],
            className="mt-4",
        ),
        html.Br(),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig3), lg=6),
                dbc.Col(dcc.Graph(figure=fig4), lg=6),
            ],
            className="mt-4",
        ),
        html.Br(),
        html.Hr(),
        html.Br(),
        dcc.Graph(figure=fig5)
    ]
)

date = html.Div([
    html.Em(f"(Last Updated at : {last_updated} EAT)"),
])

content = html.Div([
    html.Br(),
    html.P("This website tracks the number of news articles that mention each of the main presidential candidates and their running mates. The data is collected from nation.africa and standardmedia.co.ke. All data is recorded from 21st July 2022."),
    html.Hr()
])

title = html.Title("Media Coverage of Kenya's Presidential Candidates")
heading = html.H1("Tracking Digital News Media Coverage of Kenya's Presidential Candidates", className="bg-primary text-white p-2")

footer = html.Div([
    html.Br(),
    html.Hr(),
    html.Footer("Contact: o.owadenelson@gmail.com")
])

app.layout = dbc.Container([title, heading, date, content, graphs, footer], fluid=True)

if __name__ == "__main__":
    app.run(debug=True, port=8010, host='localhost')
