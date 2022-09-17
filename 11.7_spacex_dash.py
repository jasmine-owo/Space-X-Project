# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("/Users/jasmine/Desktop/python/final_project_data_spacex/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # 1: Add a dropdown list to enable Launch Site selection

                                dcc.Dropdown(id='site-dropdown',
                                                    options=[
                                                        {'label':'All Sites','value':'ALL'},
                                                        {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                                        {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                                        {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                                        {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}
                                                    ],
                                                    value='ALL',
                                                    placeholder='Select a Launch Site here',
                                                    searchable=True),
                                html.Br(),
                                # 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),


                                html.P("Payload range (Kg):"),
                                # 3: Add a slider to select payload range

                                dcc.RangeSlider(id='payload-slider',
                                                min=0,max=10000,step=1000,
                                                marks={0:'0',
                                                        100:'100'},
                                                value=[min_payload,max_payload]),
                                # 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    #when all of the Launch Sites are selected
    if entered_site == 'ALL':
        fig = px.pie(values=filtered_df.groupby('Launch Site')['class'].mean(),
        names=filtered_df.groupby('Launch Site')['Launch Site'].first(),
        title='Total Success Lauches by Site')

    else:
    # return the outcomes piechart for a selected site
        fig = px.pie(values=filtered_df[filtered_df['Launch Site']==str(entered_site)]['class'].value_counts(normalize=True),
        names=filtered_df['class'].unique(),
        title=f'Total success launches by {entered_site}')
    return fig
# 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])
def get_scatter_plot(entered_site,mass_slider):

    if entered_site == 'ALL':
        df = spacex_df
        #link up the slider and the payload mass
        low, high = mass_slider
        mask = (df['Payload Mass (kg)']>low) & (df['Payload Mass (kg)']< high)
        #plot scatter graph
        fig = px.scatter( df[mask], x='Payload Mass (kg)',
                        y='class', color='Booster Version Category'
                        )
    else:
        df = spacex_df[spacex_df['Launch Site']==str(entered_site)]
        low, high = mass_slider
        mask = (df['Payload Mass (kg)']>low) & (df['Payload Mass (kg)']< high)
        #plot scatter graph
        fig = px.scatter( df[mask], x='Payload Mass (kg)',
                        y='class', color='Booster Version Category'
                        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
