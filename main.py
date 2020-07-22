#This script is the main script that imports all required libraries, calls all scripts, compiles and runs the code

#Import all required libraries 

import io
import base64
import numpy as np 
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.dash import no_update
from dash.exceptions import PreventUpdate
import folium
import plotly.express as px
import plotly.figure_factory as ff
from scipy.interpolate import interp1d
import plotly.graph_objects as go
import matplotlib.pyplot as plt 
import cufflinks as cf
import seaborn as sns
import webbrowser
import plots
import callbacks
import layouts
import logging


#Create dataframe of reduced csv
url = "global_terror_2.csv"
df = pd.read_csv(url, encoding = "ISO-8859-1")
df99 = pd.read_csv(url, encoding = "ISO-8859-1")
df999 = pd.read_csv(url, encoding = "ISO-8859-1")


df100 = df.dropna(axis=0, inplace=False)

#Call and store all figures and plots generated in 'plots' script
fig, fig1, fig10, fig3, fig4, fig82, fig31, fig32, fig42, fig40, fig50, fig51, filter_options, filter_india_options = plots.infographics(df, df99, df999)

#Save the app layout from script 'layouts'
app = layouts.layout_(df, fig, fig1, fig10, fig3, fig4, fig82, fig31, fig32, fig42, fig40, fig50, fig51, filter_options, filter_india_options)

#Call the script that has stored all the app callbacks
callbacks.callback_(app, df, df99, df999)


#Main function which initialises local server and opens webpage after running app
if __name__ == '__main__':

    logging.basicConfig(filename="test.log",level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s')
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=True)
