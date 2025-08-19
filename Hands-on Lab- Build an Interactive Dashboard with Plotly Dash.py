# python3.11 a.py
# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
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
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'}] + [
                                            {'label': s, 'value': s} for s in spacex_df['Launch Site'].unique()],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    print('DEBUG entered_site =', repr(entered_site))
    # Normalize the incoming value just in case
    site = (entered_site or '').strip()

    # ---- IF: ALL sites selected -> show total successes by site ----
    if site == 'ALL' or site == '':
        df_all = (
            spacex_df.groupby('Launch Site', as_index=False)['class']
                     .sum()  # sum of 1/0 gives success count
                     .rename(columns={'class': 'Successes'})
        )
        fig = px.pie(
            df_all,
            values='Successes',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
        return fig

    # ---- ELSE: Specific site selected -> show Success vs Failure counts ----
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == site]
        counts = (site_df['class']
          .value_counts()
          .reindex([1, 0], fill_value=0)
          .rename(index={1: 'Success', 0: 'Failure'})
          .reset_index())

# Rename properly
        counts.columns = ['Outcome', 'Count']
        fig = px.pie(
            counts,
            values='Count',
            names='Outcome',
            title=f'Success vs Failure for {site}'
        )
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter(selected_site, payload_range):
    # Defensive defaults
    if not payload_range or len(payload_range) != 2:
        payload_range = [min_payload, max_payload]
    low, high = payload_range

    # Filter by payload range first
    df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    # If a specific site is selected, filter by site
    site = (selected_site or '').strip()
    if site not in ('', 'ALL'):
        df = df[df['Launch Site'] == site]
        title = f'Payload vs. Outcome for {site}'
    else:
        title = 'Payload vs. Outcome for All Sites'

    # Build scatter: x = payload, y = class, color = Booster Version Category
    fig = px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        hover_data=['Launch Site', 'Booster Version Category'],
        title=title,
        labels={'class': 'Mission Outcome (1=Success, 0=Failure)'}
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
