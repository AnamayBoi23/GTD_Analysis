#This script contains the layout of the app; It uses html and css components to style the page which are available 
#through Dash

#Import all required libraries

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


#Function to create layout and to display the plots
#def layout_(df, fig, fig1, fig10, fig3, fig4, fig72, fig82, fig31, fig32, fig42, fig40, fig50, fig51, filter_options, filter_india_options):
def layout_(df, fig, fig1, fig10, fig3, fig4, fig82, fig31, fig32, fig42, fig40, fig50, fig51, filter_options, filter_india_options):
    #Pre=defined CSS styles to be used for tab style, text colour etc
    colors = {
        'background': '#141e30',
        'text': '#000000'
    }

    tabs_styles = {
        'height': '44px'
    }

    tab_style = {
        'borderBottom': '1px solid #d6d6d6',
        'padding': '6px',
        'fontWeight': 'bold'
    }

    tab_selected_style = {
        'borderTop': '1px solid #d6d6d6',
        'borderBottom': '1px solid #d6d6d6',
        'backgroundColor': '#012a47',
        'color': 'white',
        'padding': '6px'
    }
    tab_style_sub = {
        'borderBottom': '1px solid #d6d6d6',
        'padding': '6x',
        'fontWeight': 'bold'
    }

    tab_selected_style_sub = {
        'borderTop': '1px solid #d6d6d6',
        'borderBottom': '1px solid #d6d6d6',
        'backgroundColor': '#274052',
        'color': 'white',
        'padding': '6px'
    }


    #code to get region names according to number; countries_dict contains an iterator where each region is paired
    #with its region number, then region_options contains a list of the names of each region mapped with its number 
    #and then the list is sorted and displayed with an all regions option
    regions = df.region_txt.unique()
    region_numbers = df.region.unique()
    regions_dict = dict(zip(regions, region_numbers))
    region_options = [{'label': region, 'value': number} for region, number in regions_dict.items()]
    region_options = sorted(region_options, key = lambda i: i['label'])
    region_options.insert(0, {'label' : 'ALL', 'value' : 0})


    #Import standard stylesheet to be used and initialise the app
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


    #Main layout of webpage
    app.layout = html.Div(style={'background': 'url("assets/terror-min.png") no-repeat center center fixed', 'backgroundRepeat': 'no-repeat', 'backgroundSize': 'cover', 'width': '100%', 'height': '100%'}, children=[
        
        #Create tabs
        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            
            #First tab to display the map; also the default tab
            dcc.Tab(label='Map tab', value='tab-1', style=tab_style, selected_style=tab_selected_style, children=[

            html.Br(),

            #Header
            html.H1(
                children='Welcome to Global Terrorism Database Dashboard',
                style={
                    'textAlign': 'center',
                    'color': '#FFFFFF'
                }
            ),
            
            html.Br(),

            #Sub-Header
            html.Div(children='Enter the details to generate infographics.', style={
                'textAlign': 'center',
                'fontSize': '20px',
                'color': '#FFFFFF'
            }),

            html.Br(),

            #Define div component that contains month and region filters
            html.Div(style={'width' : '20%', 'display' : 'inline-block', 'verticalAlign' : 'left', 'textAlign' : 'center', 'color' : colors['text'], 'marginLeft' : '120px'}, children=[
                html.Br(),
                html.Br(),
            
                html.Label('Select Month', style={'color' : '#FFFFFF', 'fontSize': '16px'}),
                dcc.Dropdown(
                    id='Month',
                    options = [
                        {'label' : 'January', 'value' : 1},
                        {'label' : 'February', 'value' : 2},
                        {'label' : 'March', 'value' : 3},
                        {'label' : 'April', 'value' : 4},
                        {'label' : 'May', 'value' : 5},
                        {'label' : 'June', 'value' : 6},
                        {'label' : 'July', 'value' : 7},
                        {'label' : 'August', 'value' : 8},
                        {'label' : 'September', 'value' : 9},
                        {'label' : 'October', 'value' : 10},
                        {'label' : 'November', 'value' : 11},
                        {'label' : 'December', 'value' : 12},
                    ],
                    placeholder = 'Choose a month'
                ),

                html.Br(),

                html.Label('Select Region', style={'color' : '#FFFFFF'}),
                dcc.Dropdown(
                    id = 'Region',
                    options = region_options[0:12],
                    placeholder = 'Choose a region'    
                ),  
            ]),

            #Define div component that contains date and country filters
            html.Div(style={'width' : '20%', 'display' : 'inline-block', 'verticalAlign' : 'left', 'textAlign' : 'center', 'color' : colors['text'], 'marginLeft' : '135px'}, children=[
                html.Br(),
                html.Br(),

                html.Label('Select Date', style={'color' : '#FFFFFF', 'fontSize': '16px'}),
                dcc.Dropdown(
                    id='Date',
                    options = [{'label': date, 'value': date} for date in range(1, 32)],
                    placeholder = 'Choose a date'
                ),

                html.Br(),

                html.Label('Select Country', style={'color' : '#FFFFFF', 'fontSize': '16px'}),
                dcc.Dropdown(
                    id='Country',
                    placeholder = 'Choose a country'
                ),
            ]),

            #Define div component that contains type of attack and city filters
            html.Div(style={'width' : '20%', 'display' : 'inline-block', 'verticalAlign' : 'right', 'textAlign' : 'center', 'color' : colors['text'], 'marginLeft' : '150px'}, children=[
                html.Br(),
                html.Br(),

                html.Label('Select Type of Attack', style={'color' : '#FFFFFF', 'fontSize': '16px'}),
                dcc.Dropdown(
                    id='Type of Attack',
                    options = [
                        {'label' : 'ALL', 'value' : 0},
                        {'label' : 'Assasination', 'value' : 1},
                        {'label' : 'Armed Assault', 'value' : 2},
                        {'label' : 'Bombing/Explosion', 'value' : 3},
                        {'label' : 'Hijacking', 'value' : 4},
                        {'label' : 'Barricade Incident', 'value' : 5},
                        {'label' : 'Kidnapping', 'value' : 6},              
                        {'label' : 'Facility/Infrastructure Attack', 'value' : 7},
                        {'label' : 'Unarmed Assault', 'value' : 8},
                        {'label' : 'Unknown', 'value' : 9},
                    ],
                    placeholder = 'Choose an attack type'
                ),

                html.Br(),
                
                html.Label('Select City', style={'color' : '#FFFFFF', 'fontSize': '16px'}),
                dcc.Dropdown(
                    id='City',
                    placeholder = 'Choose a city'    
                ),  
            ]),

            html.Br(),
            html.Br(),
            html.Br(),

            #Div that contains the 2 buttons- Generate Map and Clear Fields
            html.Div(style={'width' : '100%', 'display' : 'inline-block', 'textAlign' : 'center', 'color' : colors['text'], 'marginLeft' : '10px'}, children=[
                
                html.Br(),
                html.Br(),
                html.Br(),

                html.Button('Generate Map', id = 'generate', style={'color' : '#FFFFFF', 'fontSize' : '12px', 'width': '180px', 'display' : 'inline-block', 'marginRight': '30px', 'textAlign' : 'center'}, hidden=False),
                #html.Button('Clear', id = 'clear', style={'color' : '#FFFFFF', 'fontSize' : '12px', 'width': '180px', 'display': 'inline-block', 'marginRight': '30px', 'textAlign' : 'center'}),
                html.Br(),
                html.Br(),
                html.Br(),
            ]),

            html.Div(id='mymap', style={'width' : '100%', 'display' : 'inline-block', 'verticalAlign' : 'middle', 'textAlign' : 'center', 'color' : colors['text']}, children=[
            html.Div(id='mapmessage', style={'color' : '#FFFFFF', 'fontSize' : '20px', 'marginTop' : '-20px'}, hidden=True),
            html.Br(),
            html.Br(),
            html.Iframe(id='map', srcDoc=None, width='100%', height='600', hidden=True)
            ]),
        ]),


        #Second tab that contains all the infographics 
        dcc.Tab(label='Infographics tab', id='info_', value='tab-2', style=tab_style, selected_style=tab_selected_style ,children=[

            #Create subtabs
            dcc.Tabs(id='subtabs', value='subtab', children=[

                
                #First subtab that displays region-wise and world infographics 
                dcc.Tab(label='World Infographics', id='subtab1', value='subtab1', style=tab_style_sub, selected_style=tab_selected_style_sub, children=[

                    #html.Div(style={'background': 'url("assets/terrorism-1.png") no-repeat center center fixed', 
                    #        'background-repeat': 'no-repeat', 'backgroundSize': 'cover', 'width': '100%', 'height': '100%'}, children=[
            
                    html.Div(style={'width': '100%', 'height': '100%'}, children=[
            
                    
                    
                        #Div that contains different infographics and plots
                        html.Div(id='plots',style={'width' : '100%', 'display' : 'none'}, children=[
                            

                            #Display the attack density map that shows the concentration of attacks worldwide over all years
                            html.Div(children=[
                                dcc.Graph(id='densitymap', figure=fig, style={'width': 1370, 'height': 700, 'marginLeft': '-20px', 'marginBottom' : '-45px'}),
                            ]),


                            #Display stacked bar chart that displays number of attacks according to attack type
                            #for each region per year
                            html.Div(children=[
                                dcc.Graph(id='stackedbarmap', figure=fig1, style={'width': 1370, 'height': 700, 'marginLeft': '-20px', 'marginBottom' : '0px'}),
                            ]),


                            #Display animated bar plot that shows the people killed in each region per year
                            html.Div(children=[
                                dcc.Graph(id='barplot', figure=fig10, style={'width': 1370, 'height': 700, 'marginLeft': '0px', 'marginBottom' : '0px'}),
                            ]),

                            
                            #Display heatmap that shows the number of attacks per region over all years
                            html.Div(children=[
                                dcc.Graph(id='regionheatmap', figure=fig3, style={'width': 1370, 'height': 700, 'marginLeft': '0px', 'marginBottom' : '-45px'}),
                            ]), 

                            
                            #Display scatter geo plot that shows an animated plot of attacks worldwide per year
                            html.Div(children=[
                                dcc.Graph(id='scattergeo', figure=fig4, style={'width': 1370, 'height': 600, 'marginLeft': '0px', 'marginBottom' : '0px'}),
                            ]),       
                        ]),
                    ]),
                ]),


                #Second subtab that displays India specific infographics 
                dcc.Tab(label='India Infographics', id='subtab2', value='subtab2', style=tab_style_sub, selected_style=tab_selected_style_sub, children=[
                    
                    html.Div(style={'width': '100%', 'height': '100%'}, children=[

                        #Div that contains different infographics and plot
                        html.Div(id='plots2',style={'width' : '100%', 'display' : 'none'}, children=[

                            #Stacked bar graph showing number of attacks per state over all years
                            html.Div(children=[
                            dcc.Graph(id='indgeo', figure=fig40, style={'width': 1365, 'height': 650, 'marginLeft': '-5px', 'marginBottom' : '-38px'}),
                            ]),

                            html.Br(),
                            html.Br(),


                            #Animated bar chart that displays the fatalities for each state per year
                            html.Div(children=[
                                dcc.Graph(id='indbar-3', figure=fig31, style={'width': 1370, 'height': 700, 'marginLeft': '0px', 'marginBottom' : '-19px'}),
                            ]),

                            html.Br(),

                            
                            #Bar chart displaying people killed in each state over all years
                            html.Div(children=[
                            dcc.Graph(id='indbar-4', figure=fig32, style={'width': 1370, 'height': 700, 'marginLeft': '0px', 'marginBottom' : '-45px'}),
                            ]), 

                            html.Br(),
                            html.Br(),
                            

                            #Pie chart displaying the percentage of type of weapons used in attacks over all years
                            html.Div(children=[
                                dcc.Graph(id='indbar-2', figure=fig82, style={'width': 1365, 'height': 600, 'marginLeft': '0px', 'marginBottom' : '0px'}),
                            ]), 


                            #A world map that plays the locations of each attack in India for each year
                            html.Div(children=[
                                dcc.Graph(id='indpie', figure=fig42, style={'width': 1370, 'height': 600, 'marginLeft': '0px', 'marginBottom' : '0px'}),
                            ]),       
                        ]),    
                    ]),            
                ]),
            ]),
        ]),


        
        #Third tab that displays the Database Explorer
        dcc.Tab(label='Explorer tab', id='exp', value='tab-3', style=tab_style, selected_style=tab_selected_style ,children=[
            
            dcc.Tabs(id='subtabs2', value='subtab2', children=[

                dcc.Tab(label='World Explorer', id='subtab3', value='subtab3', style=tab_style_sub, selected_style=tab_selected_style_sub, children=[

                    html.Div(style={'backgroundColor': '#FFFFFF'}, children=[
                    html.Br(),

                    html.H1(style={'textAlign': 'center', 'color': '#000000', 'textDecoration': 'underline', 'marginTop': '20px'}, children='Global Terrorism Database Explorer'),
                    html.Br(),
                    html.Div(style={'width': '80%'}, children=[

                        html.Div(style={'width': '100%', 'display': 'flex', 'textAlign': 'center', 'marginLeft': '350px'}, children=[
                            html.Label('Incidents per Year Grouped by ', style={'color' : '	#000000', 'fontSize': '30px', 'textAlign': 'center', 'float': 'left'}),
                            dcc.Dropdown(
                                id='filter',
                                options=[{'label': j, 'value': i} for i, j in enumerate(filter_options)],
                                value=6,
                                clearable=False,
                                style={'width': '250px', 'marginLeft': '10px', 'marginTop': '3px'}
                            ),
                        ]),

                        html.Br(),
                        html.Br(),

                        dcc.Graph(id='plots3', figure=fig50, style={'width': 1300, 'height': 600}),

                        html.Br(),
                        html.Br(),

                        html.Div(style={'width': '40%', 'display': 'inline-block', 'textAlign': 'center', 'marginLeft': '450px'}, children=[
                            dcc.Input(id='searchtext', style={'color' : '#000000', 'textAlign': 'center',  'width': '300px'}, placeholder='Enter filter text.'),
                            html.Div(id='msg', children="")
                        ]),

                        html.Br(),
                        html.Br(),
                        html.Br(),

                        html.Div(style={'marginLeft': '250px', 'marginBottom': '40px'}, children=[
                            dcc.RangeSlider(
                                id='yearslider',
                                min=1970,
                                max=2018,
                                value=[1970, 2018],
                                marks={str(i): str(i) for i in range(1970, 2019, 5)},
                                allowCross=False,

                                )
                            ]),

                        html.Br(),

                        ]),
                    ]),
                ]),

                dcc.Tab(label='India Explorer', id='subtab4', value='subtab4', style=tab_style_sub, selected_style=tab_selected_style_sub, children=[

                    html.Div(style={'backgroundColor': '#FFFFFF'}, children=[
                    html.Br(),

                    html.H1(style={'textAlign': 'center', 'color': '#000000', 'textDecoration': 'underline', 'marginTop': '20px'}, children='Global Terrorism Database Explorer'),
                    html.Br(),
                    html.Div(style={'width': '80%'}, children=[

                        html.Div(style={'width': '100%', 'display': 'flex', 'textAlign': 'center', 'marginLeft': '350px'}, children=[
                            html.Label('Incidents per Year Grouped by ', style={'color' : '	#000000', 'fontSize': '30px', 'textAlign': 'center', 'float': 'left'}),
                            dcc.Dropdown(
                                id='filter2',
                                options=[{'label': j, 'value': i} for i, j in enumerate(filter_india_options)],
                                value=5,
                                clearable=False,
                                style={'width': '250px', 'marginLeft': '10px', 'marginTop': '3px'}
                            ),
                        ]),

                        html.Br(),
                        html.Br(),

                        dcc.Graph(id='plots4', figure=fig51, style={'width': 1370, 'height': 600}),

                        html.Br(),
                        html.Br(),

                        html.Div(style={'width': '40%', 'display': 'inline-block', 'textAlign': 'center', 'marginLeft': '450px'}, children=[
                            dcc.Input(id='searchtext2', style={'color' : '#000000', 'textAlign': 'center',  'width': '300px'}, placeholder='Enter filter text.'),
                            html.Div(id='msg2', children="")
                        ]),

                        html.Br(),
                        html.Br(),
                        html.Br(),

                        html.Div(style={'marginLeft': '250px', 'marginBottom': '40px'}, children=[
                            dcc.RangeSlider(
                                id='yearslider2',
                                min=1970,
                                max=2018,
                                value=[1970, 2018],
                                marks={str(i): str(i) for i in range(1970, 2019, 5)},
                                allowCross=False,

                                )
                            ]),

                        html.Br(),

                        ]),
                    ]),
                ]),               
            ]),
        ]),
    ]),

    ])

    return app