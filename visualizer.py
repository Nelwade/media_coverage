from operator import add
from plotly.tools import mpl_to_plotly
from dash import dcc, html
from dash_bootstrap_templates import load_figure_template

import dash_bootstrap_components as dbc
import dash

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

sns.set_style("darkgrid")

def plot_multibars(df_totals, df_nation, df_std):
    df_totals = df_totals.sum(numeric_only=True)
    totals_list = df_totals.values
    #print(df_totals)

    df_nation = df_nation.sum(numeric_only=True)
    nation_list = df_nation.values

    df_std = df_std.sum(numeric_only=True)
    std_list = df_std.values

    x_variables = ["Nation Africa", "Standard Media", "Totals"]
    raila = [nation_list[0], std_list[0], totals_list[0]]
    ruto = [nation_list[1], std_list[1], totals_list[1]]
    karua = [nation_list[2], std_list[2], totals_list[2]]
    rigathi = [nation_list[3], std_list[3], totals_list[3]]

    

    # print(df_totals)
    # print(df_totals.values)

    #print(raila, ruto, karua, rigathi)
    #x_axis = np.arange(len(x_variables))
    
    def plot_individuals():
        fig=go.Figure(data=[
            go.Bar(name="Raila Odinga", x=x_variables, y=raila),
            go.Bar(name="William Ruto", x=x_variables, y=ruto),
            go.Bar(name="Martha Karua", x=x_variables, y=karua),
            go.Bar(name="Rigathi Gachagua", x=x_variables, y=rigathi),
        ])
        fig.update_layout(
            title="Number of Article Mentions Per Candidate Since July 15th",
            barmode='group',
            xaxis_tickangle=-45,
            yaxis=dict(title="Number of Articles", titlefont_size=16, tickfont_size=14),
            xaxis=dict(title="Digital Media Website", titlefont_size=16, tickfont_size=14)
            )
        
        #fig.show()

        # fig = plt.figure(figsize=(10,10))

        # plt.bar(x_axis +0.2, raila, width=0.2, label="Raila Odinga")
        # plt.bar(x_axis +0.2*2, ruto, width=0.2, label="William Ruto")
        # plt.bar(x_axis +0.2*3, karua, width=0.2, label="Martha Karua")
        # plt.bar(x_axis +0.2*4, rigathi, width=0.2, label="Rigathi Gachagua")

        # plt.xlabel("Candidates", fontsize=12, fontweight='bold')
        # plt.ylabel("Total Mentions", fontsize=12, fontweight='bold')
        # plt.title("Mentions Per Candidate on Digital News Sites Since July 15th")

        # #plt.xticks(x_axis, x_variables)
        # plt.xticks(x_axis + 0.5, x_variables)
        # plt.legend()
        # #plt.show()

        return fig

    def plot_parties():
        azimio = list(map(add, raila, karua))
        kenya_kwanza = list(map(add, ruto, rigathi))

        fig=go.Figure(data=[
            go.Bar(name="Azimio La Umoja", x=x_variables, y=azimio),
            go.Bar(name="Kenya Kwanza", x=x_variables, y=kenya_kwanza),
        ])
        fig.update_layout(
            title="Number of Article Mentions of Per Party Since July 15th",
            barmode='group', 
            xaxis_tickangle=-45,
            yaxis=dict(title="Number of Articles", titlefont_size=16, tickfont_size=14),
            xaxis=dict(title="Digital Media Website", titlefont_size=16, tickfont_size=14)
            )
        
        #fig.show()

        # fig = plt.figure(figsize=(4,4))
        # plt.bar(x_axis +0.2, azimio, width=0.2, label="Azimio La Umoja")
        # plt.bar(x_axis +0.2*2, kenya_kwanza, width=0.2, label="Kenya Kwanza")

        # plt.xlabel("Party", fontsize=12, fontweight='bold')
        # plt.ylabel("Total Mentions", fontsize=12, fontweight='bold')
        # plt.title("Total Mentions Per Party on Digital News Sites Since July 15th")

        # #plt.xticks(x_axis, x_variables)
        # plt.xticks(x_axis + 0.3, x_variables)
        # plt.legend()
        
        return fig

    fig1 = plot_individuals()
    fig2 = plot_parties()
    
    return fig1, fig2


