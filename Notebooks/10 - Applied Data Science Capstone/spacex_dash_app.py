# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',   
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                value='ALL', 
                                placeholder="Select Launch Site", 
                                searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was 
                                
                                html.Div(dcc.Graph(id='success-pie-chart')),

                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(
                                    id='payload-slider', 
                                    min=0, max=10000, 
                                    step=1000, 
                                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                    value=[min_payload, max_payload])),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

def compute_info(spacex_df, entered_site):
    # Select data
    filtered_df =  spacex_df[spacex_df['Launch Site']==entered_site]
    site_success = spacex_df.groupby(['Launch Site'])['class'].sum().reset_index()
    launch_site_success = filtered_df.groupby(['class'])['class'].count()
    return filtered_df, site_success, launch_site_success

@app.callback( 
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    # Compute required information for creating graph from the data
    filtered_df, site_success, launch_site_success = compute_info(spacex_df, entered_site)

    if entered_site == 'ALL':
        fig = px.pie(site_success, values='class', 
        names='Launch Site', 
        title='Total Success Launches by site')
        return fig
    else:
        fig = px.pie(launch_site_success, values='class', 
        names='class',
        title='Launch outcome for ' + entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( 
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_plot(entered_site, slider_range):
    # Compute required information for creating graph from the data
    # filtered_payload_df = spacex_df.loc[(spacex_df['Launch Site']==entered_site) & (spacex_df['Payload Mass (kg)']>=min_mass) & (spacex_df['Payload Mass (kg)']<=max_mass)]
    filtered_df, site_success, launch_site_success = compute_info(spacex_df, entered_site)
    
    slider_filtered = spacex_df.where((spacex_df['Payload Mass (kg)'] >= slider_range[0]) & (spacex_df['Payload Mass (kg)'] <= slider_range[1]))
    slider_site_filtered = slider_filtered.where((spacex_df['Launch Site'] == entered_site))

    if entered_site == 'ALL':
        fig = px.scatter(slider_filtered, x="Payload Mass (kg)",y="class", color="Booster Version Category",
        title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        fig = px.scatter(slider_site_filtered, x="Payload Mass (kg)",y="class", color="Booster Version Category",
        title='Correlation between Payload and Success for ' + entered_site)
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()