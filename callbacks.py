#This script contains all the app callbacks used in the project; Callbacks are Python functions that are called by Dash
#Whenever an input component's property changes.

#Import all required libraries

import numpy as np 
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import folium
import plotly.express as px

clicks_map=0
empty_fields = None

#Define function that takes the app and the required dataframes as arguments
def callback_(app, df, df99, df999):

    clicks_map=0
    empty_fields = None

    #App callback and function that defines the date dropdown dropdown based on month selected
    @app.callback(
        dash.dependencies.Output('Date', 'options'),
        [dash.dependencies.Input('Month', 'value')]
    )
    def update_date_dropdown(month):
        if month is None:
                raise PreventUpdate
        elif month in [1, 3, 5, 7, 8, 10, 12]:
            return [{'label': str(i), 'value': i} for i in range(1, 32)]
        elif month in [4, 6, 9, 11]:
            return [{'label': str(i), 'value': i} for i in range(1, 31)]
        elif month in [2]:
            return [{'label': str(i), 'value': i} for i in range(1, 30)]



    #App callback and function that shows the countries dropdown according to the region selected
    @app.callback(
        dash.dependencies.Output('Country', 'options'),
        [dash.dependencies.Input('Region', 'value')]
    )
    def update_country_dropdown(region):
        if region==0:
            df6 = df
        else:
            df6 = df[df.region.eq(region)]
        countries = df6.country_txt.unique()
        country_numbers = df6.country.unique()
        countries_dict = dict(zip(countries, country_numbers))
        country_options = [{'label': country, 'value': number} for country, number in countries_dict.items()]
        country_options = sorted(country_options, key = lambda i: i['label'])
        country_options.insert(0, {'label' : 'ALL', 'value' : 0})
        return country_options



    #App callback and funtion that displays the city dropdown for the selected country
    @app.callback(
        dash.dependencies.Output('City', 'options'),
        [dash.dependencies.Input('Country', 'value')]
    )
    def update_city_dropdown(country):
        if country == 0:
            df2 = df
        else:
            df2 = df[df.country.eq(country)]
        
        city_options = [{'label' : i, 'value' : i} for i in df2.city.unique() if isinstance(i, str)==True and i!='unknown']
        city_options = sorted(city_options, key = lambda i: i['label'])
        return city_options
        


    #App callback and function to generate folium map which is saved as .html file
    @app.callback(dash.dependencies.Output('map', 'srcDoc'),
                [dash.dependencies.Input('Month', 'value'),
                dash.dependencies.Input('Date', 'value'),
                dash.dependencies.Input('Type of Attack', 'value'),
                dash.dependencies.Input('Region', 'value'),
                dash.dependencies.Input('Country', 'value'),
                dash.dependencies.Input('City', 'value')]
    )
    def generate_map(mnt, dte, att, reg, cou, cty):
        global df100
        global empty_fields
        df100 = df.dropna(axis=0, inplace=False)
        
        #Check if all fields entered are empty
        if not any([mnt, dte, att, reg, cou, cty]):
            empty_fields = True
        else:
            empty_fields = False

        #Store the unique values present for each dropdown
        month=df.imonth.unique()
        date=df.iday.unique()
        attack=df.attacktype1.unique()
        region=df.region.unique()
        country=df.country.unique()
        city=df.city.unique()

        #Check whether each dropdown is filled or not; Also checks if the user has entered 'ALL' option for 2 dropdowns
        if mnt!=None:
            month=[mnt]
        if dte!=None:
            date=[dte]
        if att==0:
            pass
        elif att!=None:
            attack=[att]
        if reg==0:
            pass
        elif reg!=None:
            region=[reg]
        if cou==0:
            pass
        elif cou!=None:
            country=[cou]
        if cty!=None:
            city=[cty]

        #Create a dataframe of the entered values
        df100 = df100[df100.imonth.isin(month) & df100.iday.isin(date) & df100.attacktype1.isin(attack) & df100.region.isin(region) & df100.country.isin(country) & df100.city.isin(city)]

        if df100.empty==True:
            return None  


        #Store the necessary values to generate the folium map
        lat = list(df100['latitude'])
        lon = list(df100['longitude'])
        regionname=list(df100['region_txt'])
        countryname=list(df100['country_txt'])
        cityname = list(df100['city'])
        kills = list(df100['nkill'])
        iyear = list(df100['iyear'])
        imonth = list(df100['imonth'])
        iday = list(df100['iday'])
        attack = list(df100['attacktype1_txt'])

        tooltip = 'Click for more info'

        f = folium.Figure(width=1000, height=1000)
        m=folium.Map([lat[0],lon[0]], zoom_start=4).add_to(f)

        #Create a marker for each matching record on the folium map
        for i in range(len(lat)):
            if kills[i]==-1:
                kills[i] = 'Unknown'
            else:
                kills[i] = str(int(kills[i]))
            iyear[i] = str(int(iyear[i]))
            imonth[i] = str(int(imonth[i]))
            iday[i] = str(int(iday[i]))
            pp = (
                "Region: {} <br>"
                "Country: {} <br>"
                "City: {} <br>"
                "Date: {} / {} / {} <br>"
                "Attack Type: {} <br>"
                "Fatalities: {} <br>"
                ).format(regionname[i], countryname[i], cityname[i], iday[i], imonth[i], iyear[i], attack[i], kills[i])

            colors={'Assassination' : 'red', 'Hostage Taking (Kidnapping)': 'blue', 'Bombing/Explosion' : 'gray', 
            'Facility/Infrastructure Attack' : 'darkred', 'Armed Assault' : 'orange', 'Hijacking' : 'beige', 'Unknown' : 'green', 
            'Unarmed Assault' : 'darkgreen', 'Hostage Taking (Barricade Incident)' : 'purple'}
            color=colors[attack[i]]
                
            popup = folium.Popup(pp, min_width=10, max_width=10000)
            if np.isnan(lat[i])==False and np.isnan(lon[i])==False:
                folium.Marker(location=[lat[i],lon[i]], popup=popup, tooltip=tooltip, icon=folium.Icon(color=color)).add_to(m)

        #Save the map in a .html file
        m.save("mymapnew.html")
        return open('mymapnew.html', 'r').read()



    #App callback and function to display folium map which is displayed if correct input is given and generate 
    #button is clicked
    @app.callback(
        [dash.dependencies.Output('mapmessage', 'children'),
        dash.dependencies.Output('map', 'hidden'),
        dash.dependencies.Output('mapmessage', 'hidden')],
        [dash.dependencies.Input('generate', 'n_clicks')]
    )
    def display_map(n_clicks):
        
        global clicks_map

        if n_clicks!=None:
            if n_clicks>clicks_map:
                clicks_map+=1
                if empty_fields==True:
                    return "All fields must not be empty!\n Clear page to enter fields again!", True, False
                if df100.empty==True:    
                    return "Map cannot be generated as no matching entries were found.", True, False
                #return "Scroll down to see the map.", False, False
        elif n_clicks==None:
            return "", True, True

        return "Scroll down to see the map.", False, False
        #return "Error!", True, False



    #App callback and function to display world infographics after clicking button; Upon clicking button again, the 
    #Section is hidden again
    @app.callback(
        dash.dependencies.Output('plots', 'style'),
        [dash.dependencies.Input('subtab1', 'value')]
    )
    def disp_plots(value):
        if value == 'subtab1':
            return {'color' : '#FFFFFF', 'fontSize' : '12px', 'width' : '180px', 'display': 'inline-block', 'marginRight': '30px', 'textAlign' : 'center'}
        
        else:
            return {'display' : 'none'}



    #App callback and function to display India infographics after clicking button; Upon clicking button again, the 
    #Section is hidden again    
    @app.callback(
        dash.dependencies.Output('plots2', 'style'),
        [dash.dependencies.Input('subtab2', 'value')]
    )
    def disp_plots2(value):
        if value == 'subtab2':
            return {'color' : '#FFFFFF', 'fontSize' : '12px', 'width' : '180px', 'display': 'inline-block', 'marginRight': '30px', 'textAlign' : 'center'}
        
        else:
            return {'display' : 'none'}



    #App callback and function to create GTD explorer
    @app.callback(
        [Output('plots3', 'figure'),
        Output('msg', 'children')],
        [Input('filter', 'value'),
        Input('yearslider', 'value'),
        Input('searchtext', 'value')]
    )
    def update_graph(fvalue, yrange, search):
        if fvalue==None:
            return None
        min=yrange[0]
        max=yrange[1]
        msg=""
        group = ['propextent_txt', 'natlty1_txt', 'targtype1_txt', 'attacktype1_txt', 'weaptype1_txt', 'region_txt', 'country_txt']
        data = df99[df99[group[fvalue]].notnull()]
        data['Attacks'] = data.groupby([group[fvalue], 'iyear'])[group[fvalue]].transform('count')
        data = data.filter([group[fvalue], 'Attacks', 'iyear']).drop_duplicates()
        data=data[(data['iyear']>=min) & (data['iyear']<=max)]
        if search!=None:
            dfr=data[data.iloc[:, 0].str.contains('^'+search, case=False, regex=True)]
            if dfr.empty==True:
                msg="No matches found!"
            else:
                data=dfr
        fig50 = px.area(data, x="iyear", y="Attacks", color=group[fvalue], line_group=group[fvalue])
        return fig50, msg
        

    @app.callback(
        [Output('plots4', 'figure'),
        Output('msg2', 'children')],
        [Input('filter2', 'value'),
        Input('yearslider2', 'value'),
        Input('searchtext2', 'value')]
    )
    def update_graph2(fvalue2, yrange2, search2):
        if fvalue2 == None:
            return None
        min=yrange2[0]
        max=yrange2[1]
        msg2=""
        group_india = ['gname', 'propextent_txt', 'targtype1_txt', 'attacktype1_txt', 'weaptype1_txt', 'provstate']    
        data2 = df999[df999[group_india[fvalue2]].notnull()]
        data2['Attacks'] = data2.groupby([group_india[fvalue2], 'iyear'])[group_india[fvalue2]].transform('count')
        data2 = data2.filter([group_india[fvalue2], 'Attacks', 'iyear']).drop_duplicates()
        data2 = data2[(data2['iyear']>=min) & (data2['iyear']<=max)]
        if search2!=None:
            dfr2 = data2[data2.iloc[:, 0].str.contains('^'+search2, case=False, regex=True)]
            if dfr2.empty==True:
                msg2 = "No matches found!"
            else:
                data2 = dfr2
        fig51 = px.area(data2, x="iyear", y="Attacks", color=group_india[fvalue2], line_group=group_india[fvalue2])
        return fig51, msg2