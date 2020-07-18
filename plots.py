import folium
import plotly.tools as tls 
import plotly.express as px
import plotly.figure_factory as ff
from scipy.interpolate import interp1d
import plotly.graph_objects as go
import matplotlib.pyplot as plt 
import cufflinks as cf
import numpy as np 
import pandas as pd
import seaborn as sns


def infographics(df, df99):

    #code to generate density heatmap of attacks all over the world; group csv by country_txt create column 'freq' that 
    #contains count of the number of times a country has been mentioned; create new df that contains country_txt, freq
    #lat and long and drops the duplicates in the original df; convert the number of attacks per country to a list;
    #create a variable that defines the size of the radius of the marker used in the map; plot map and store in fig
    df['freq'] = df.groupby('country_txt')['country'].transform('count')
    df8 = df.filter(['country_txt','freq','latitude','longitude']).drop_duplicates()
    df8=df8.rename(columns={'country_txt' : 'Country', 'freq' : 'Attacks','latitude' : 'Latitude','longitude' : 'Longitude'})
    list1 = df8.Attacks.values.tolist()
    m = interp1d([1,max(list1)],[5,20])
    circle = m(list1)
    fig = px.density_mapbox(df8, lat='Latitude', lon='Longitude', radius=circle, zoom=1, mapbox_style='open-street-map', hover_data=["Country", "Attacks"])
    fig.update_layout(
        title={"text" : "Density Map", 'x' : 0.5, 'y' : 0.95},
        font=dict(size=18)
        )


    #Code that creates stacked bar chart displaying the number of attacks per year for each attack type
    #Filter year and attacktype and find the number of attacks for each attacktype per year then plot the graph
    df60 = df.filter(["iyear", "attacktype1_txt"], axis=1)
    count_series = df60.groupby(["iyear", "attacktype1_txt"]).size()
    df61 = count_series.to_frame(name = 'size').reset_index()
    df62 = df61.pivot(index='iyear', columns='attacktype1_txt', values='size')
    fig1 = df62.iplot(kind='bar', barmode='stack', asFigure=True)
    fig1.update_layout(
        title={"text" : "Comparison of Attack Types using Stacked Bar Chart", 'x' : 0.5, 'y' : 0.95},
        font=dict(size=18),
        legend = dict(font = dict(size=14))
        )

    #Bar graph with a slider for year that shows number of people killed per region for every year
    df70 = df.filter(["region_txt", "nkill", "iyear"], axis=1)
    df70 = df70[df70['nkill']!=-1]
    count_series = df70.groupby(['iyear', 'region_txt'])['nkill'].sum()
    df71 = count_series.to_frame(name = 'kills').reset_index()
    fig10 = px.bar(df71, y="region_txt", x="kills", animation_frame="iyear", 
                    color="region_txt", hover_name="region_txt", hover_data=['iyear', 'kills'],
                labels={'iyear' : 'Year', 'region_txt' : 'Region', 'kills' : 'Fatalities'},
                width=1100, orientation='h')
    fig["layout"].pop("updatemenus")
    fig10.update_layout(
        title={"text" : "People killed according to region", 'x' : 0.5, 'y' : 0.95},
        font=dict(size=18),
        legend = dict(font = dict(size=14))
        )


    #Heatmap which shows a coloured representation of the total number of attacks per region
    #count the number of times each region has been mentioned in the csv and store that as the freq of attacks for 
    #that region. Reshape them to numpy arrays and create a heatmap
    df['freq'] = df.groupby('region_txt')['region_txt'].transform('count')
    dfr = df.filter(['region_txt', 'freq']).drop_duplicates()
    r=dfr['region_txt'].to_numpy().reshape(4, 3)
    fr=dfr['freq'].to_numpy().reshape(4, 3)
    fig3 = ff.create_annotated_heatmap(fr, annotation_text=r, colorscale='Viridis', hoverinfo='z', showscale=True)
    fig3.update_layout(
        title={"text" : "Region-Wise Concentration of Attacks using Heatmap", 'x' : 0.5, 'y' : 0.93},
        font=dict(size=18),
        )


    #Scattered GeoPlot that shows the total attacks per region per year along with date, city and location
    fig4 = px.scatter_geo(df, lat='latitude', lon='longitude',
                        hover_name="country_txt", hover_data=['iyear', 'city'],
                        labels={'iyear':'Year', 'city': 'City', 'latitude':'Latitude', 'longitude':'Longitude'},
                        animation_frame="iyear", color = "region_txt",
                        projection="natural earth")
    fig4.update_layout(
        title={"text" : "Global Terrorism History using ScatterGeo Plot", 'x' : 0.5, 'y' : 0.98},
        font=dict(size=18),
        )



    #create df for india infographics 
    df200 = df.loc[df['country_txt'] == 'India']
    df200['provstate'] = df200['provstate'].replace(['Andhra pradesh'],'Andhra Pradesh')

    #stacked bar chart of attack types and frequency per year for india
    df70_ = df200.filter(["iyear", "attacktype1_txt"], axis=1)
    count_series = df70_.groupby(["iyear", "attacktype1_txt"]).size()
    df71 = count_series.to_frame(name = 'size').reset_index()
    df72 = df71.pivot(index='iyear', columns='attacktype1_txt', values='size')
    fig72 = df72.iplot(kind='bar', barmode='stack', asFigure=True)
    fig72.update_layout(
        title={"text" : "Comparison of Attack Types using Stacked Bar Chart for India", 'x' : 0.48, 'y' : 0.95},
        font=dict(size=18),
        legend = dict(font = dict(size=14))
        )

    #Statewise attack types and frequency for all years
    df80 = df200.filter(["provstate", "attacktype1_txt"], axis=1)
    count_series = df80.groupby(["provstate", "attacktype1_txt"]).size()
    df81 = count_series.to_frame(name = 'size').reset_index()
    df82 = df81.pivot(index='provstate', columns='attacktype1_txt', values='size')
    fig82 = df82.iplot(kind='bar', barmode='stack', asFigure=True)
    fig82.update_layout(
        title={"text" : "Comparison of Attack Types using Stacked Bar Chart- statewise", 'x' : 0.48, 'y' : 0.95},
        font=dict(size=14),
        legend = dict(font = dict(size=15)),
        xaxis_tickangle=-45
        )

    #People killed in each state per year
    df30 = df200.filter(["provstate", "nkill", "iyear"], axis=1)
    df30 = df30[df30['nkill']!=-1]
    count_series = df30.groupby(['iyear','provstate'])['nkill'].sum()
    df31 = count_series.to_frame(name = 'kills').reset_index()
    fig31 = px.bar(df31, x='provstate', y='kills', animation_frame="iyear", animation_group="provstate",
                hover_data=['provstate', 'kills'], color='kills',
                labels={'provstate': 'States', 'kills': 'Total Fatalities'}, height=600, width=1000)
    fig31.update_layout(xaxis_tickangle=-45, 
                        width=1370,
                        height=700,
                        margin=dict(pad=20),
                    title={"text" : "People killed according to state per year", 'x' : 0.5, 'y' : 0.98})
    fig31.update_xaxes(automargin=True)


    #Total fatalities according to each state
    df32 = df200.filter(["provstate", "nkill", "iyear"], axis=1)
    df32 = df32[df32['nkill']!=-1]
    count_series = df32.groupby(['provstate'])['nkill'].sum()
    df33 = count_series.to_frame(name = 'kills').reset_index()
    fig32 = px.bar(df33, x='provstate', y='kills',
                hover_data=['provstate', 'kills'], color='kills',
                labels={'provstate': 'States', 'kills': 'Total Fatalities'}, height=600, width=1000)
    fig32.update_layout(xaxis_tickangle=-45, 
                        width=1350,
                        height=700,
                    title={"text" : "People killed according to state overall", 'x' : 0.5, 'y' : 0.97})
    fig32.update_xaxes(automargin=True)

    #pie chart of weapon types used in all attacks 
    df42 = df200.filter(["weaptype1_txt", "iyear"], axis=1)
    df42.head()
    count_series = df42.groupby(['weaptype1_txt'])['iyear'].count()
    df43 = count_series.to_frame(name = 'weap').reset_index()
    fig42 = px.pie(df43, values='weap', names='weaptype1_txt', labels={'weap':'No. of times weapon used', 'weaptype1_txt': 'Weapon_Type'},
                title='Types of weapons used in attacks in India', hole=.3)
    fig42.update_traces(textposition='inside', textinfo='percent+label')

    #Scatter geo plot of india
    fig40 = px.scatter_geo(df200, lat='latitude', lon='longitude',
                    hover_name="country_txt", hover_data=['iyear', 'city'],
                    labels={'iyear':'Year', 'city': 'City', 'latitude':'Latitude', 'longitude':'Longitude', 'attacktype1':'Attack Type'},
                    animation_frame="iyear", color = "attacktype1",
                    projection="natural earth")
    fig40.update_layout(
        title={"text" : "India's Terrorism History using ScatterGeo Plot", 'x' : 0.5, 'y' : 0.98},
        font=dict(size=18),
        showlegend=False
        )


    filter_options = ['Property Damage', 'Target Nationality', 'Target Type', 'Type of Attack', 'Weapon Type', 'Region', 'Country']
    df99['Attacks'] = df99.groupby(['country_txt', 'iyear'])['country_txt'].transform('count')
    dfr = df99.filter(['country_txt', 'Attacks', 'iyear']).drop_duplicates()
    fig50 = px.area(dfr, x="iyear", y="Attacks", color="country_txt", line_group="country_txt")

    return fig, fig1, fig10, fig3, fig4, fig72, fig82, fig31, fig32, fig42, fig40, fig50, filter_options
    