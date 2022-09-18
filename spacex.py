# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
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
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'site1'},
                                    {'label': 'VAFB SLC-4E', 'value': 'site2'},
                                    {'label': 'KSC LC-39A', 'value': 'site3'},
                                    {'label': 'CCAFS SLC-40', 'value': 'site4'}],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success')
        return fig
    elif entered_site == 'site1':
        fig2 = px.pie(filtered_df[filtered_df['Launch Site']== 'CCAFS LC-40'], values='class', names='class', 
        title='Total success')
        return fig2
    elif entered_site == 'site2':
        fig2 = px.pie(filtered_df[filtered_df['Launch Site']== 'VAFB SLC-4E'], names='class', 
        title='Total success')
        return fig2
    elif entered_site == 'site3':
        fig2 = px.pie(filtered_df[filtered_df['Launch Site']== 'KSC LC-39A'], names='class',  
        title='Total success')
        return fig2
    else:
        fig2 = px.pie(filtered_df[filtered_df['Launch Site']== 'CCAFS SLC-40'], names='class', 
        title='Total success')
        return fig2
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), 
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value"))
def get_scatter_plot(site_entered, slider_range):
    df = spacex_df
    low, high = slider_range
    mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)

    if site_entered == 'ALL':
        fig = px.scatter(df[mask], x='Payload Mass (kg)', y='class', color="Booster Version Category")
        return fig
    elif site_entered == 'site1':
        fig = px.scatter(df[mask][df['Launch Site']== 'CCAFS LC-40'], x='Payload Mass (kg)', y='class', color="Booster Version Category")
        return fig
    elif site_entered == 'site2':
        fig = px.scatter(df[mask][df['Launch Site']== 'VAFB SLC-4E'], x='Payload Mass (kg)', y='class', color="Booster Version Category")
        return fig
    elif site_entered == 'site3':
        fig = px.scatter(df[mask][df['Launch Site']== 'KSC LC-39A'], x='Payload Mass (kg)', y='class', color="Booster Version Category")
        return fig
    else:
        fig = px.scatter(df[mask][df['Launch Site']== 'CCAFS SLC-40'], x='Payload Mass (kg)', y='class', color="Booster Version Category")
        return fig
    
# Run the app
if __name__ == '__main__':
    app.run_server()