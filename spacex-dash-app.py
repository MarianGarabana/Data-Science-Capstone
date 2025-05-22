# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Dropdown to select Launch Site
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'ALL SITES', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),

    # TASK 2: Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Payload slider
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    value=[min_payload, max_payload],
                    marks={0: '0', 2500: '2500', 5000: '5000',
                           7500: '7500', 10000: '10000'}),

    # TASK 4: Scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def build_pie_chart(site_dropdown):
    if site_dropdown == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site',
                     title='Total Successful Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        counts = filtered_df['class'].value_counts().reset_index()
        counts.columns = ['Outcome', 'Count']
        counts['Outcome'] = counts['Outcome'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(counts, values='Count', names='Outcome',
                     title=f'Success vs Failure for site {site_dropdown}')
        return fig

# TASK 4: Callback for scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def build_scatter_chart(site_dropdown, payload_range):
    low, high = payload_range
    if site_dropdown == 'ALL':
        filtered_df = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= low) &
            (spacex_df['Payload Mass (kg)'] <= high)
        ]
    else:
        filtered_df = spacex_df[
            (spacex_df['Launch Site'] == site_dropdown) &
            (spacex_df['Payload Mass (kg)'] >= low) &
            (spacex_df['Payload Mass (kg)'] <= high)
        ]

    fig = px.scatter(filtered_df,
                     x='Payload Mass (kg)',
                     y='class',
                     color='Booster Version Category',
                     title=f'Payload vs Outcome for site {site_dropdown if site_dropdown != "ALL" else "All Sites"}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(port=8060)
