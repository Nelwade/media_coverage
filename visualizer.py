from operator import add

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
    
    def plot_individuals():
        fig=go.Figure(data=[
            go.Bar(name="Raila Odinga", x=x_variables, y=raila),
            go.Bar(name="William Ruto", x=x_variables, y=ruto),
            go.Bar(name="Martha Karua", x=x_variables, y=karua),
            go.Bar(name="Rigathi Gachagua", x=x_variables, y=rigathi),
        ])
        fig.update_layout(
            title="Number of Article Mentions Per Candidate Since July 21st",
            barmode='group',
            xaxis_tickangle=-45,
            yaxis=dict(title="Number of Articles", titlefont_size=16, tickfont_size=14),
            xaxis=dict(title="Digital News Website", titlefont_size=16, tickfont_size=14)
            )

        return fig

    def plot_parties():
        azimio = list(map(add, raila, karua))
        kenya_kwanza = list(map(add, ruto, rigathi))

        fig=go.Figure(data=[
            go.Bar(name="Azimio La Umoja", x=x_variables, y=azimio),
            go.Bar(name="Kenya Kwanza", x=x_variables, y=kenya_kwanza),
        ])
        fig.update_layout(
            title="Number of Article Mentions Per Party Since July 21st",
            barmode='group', 
            xaxis_tickangle=-45,
            yaxis=dict(title="Number of Articles", titlefont_size=16, tickfont_size=14),
            xaxis=dict(title="Digital News Website", titlefont_size=16, tickfont_size=14)
            )
        
        return fig

    fig1 = plot_individuals()
    fig2 = plot_parties()
    
    return fig1, fig2


