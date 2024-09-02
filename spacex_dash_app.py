# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
#Flight Number,Launch Site,class,Payload Mass (kg),
#Booster Version,Booster Version Category

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique()
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='id',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                 *[{'label': x, 'value': x} for x in launch_sites],
                                            ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                        ),
                                html.Br(),

                                # Add a range slider for payload mass
                                dcc.RangeSlider(id='payload-slider',
                                                min=min_payload, max=max_payload, step=1000,
                                                marks={int(i): str(i) for i in range(int(min_payload), int(max_payload)+1, 5000)},
                                                value=[min_payload, max_payload]),
])

# Define the callbacks
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('id', 'value'))
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Create pie chart for all sites
        fig = px.pie(spacex_df, names='Launch Site', values='class',
                     title='Total Success Launches by Site')
    else:
        # Filter data by selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f'Total Success Launches for site {selected_site}')
    return fig

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('id', 'value'), Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]
    
    if selected_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Payload vs. Outcome for {selected_site}')
    
    return fig

# Add the range slider to the layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(id='id',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     *[{'label': x, 'value': x} for x in launch_sites],
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=min_payload, max=max_payload, step=1000,
                    marks={int(i): str(i) for i in range(int(min_payload), int(max_payload)+1, 5000)},
                    value=[min_payload, max_payload]),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)