import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load data (remote URL is fine for deployment)
spacex_df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
)

max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

app = dash.Dash(__name__)
server = app.server  # IMPORTANT for gunicorn

app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),

        dcc.Dropdown(
            id="site-dropdown",
            options=[{"label": "All Sites", "value": "ALL"}]
            + [{"label": s, "value": s} for s in spacex_df["Launch Site"].unique()],
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True,
            clearable=False,
        ),
        html.Br(),

        dcc.Graph(id="success-pie-chart"),
        html.Br(),

        html.P("Payload range (Kg):"),
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            value=[min_payload, max_payload],
            marks={0: "0", 2500: "2500", 5000: "5000", 7500: "7500", 10000: "10000"},
        ),

        html.Br(),
        dcc.Graph(id="success-payload-scatter-chart"),
    ]
)

@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value"),
)
def get_pie_chart(entered_site):
    site = (entered_site or "").strip()

    if site == "ALL" or site == "":
        df_all = (
            spacex_df.groupby("Launch Site", as_index=False)["class"]
            .sum()
            .rename(columns={"class": "Successes"})
        )
        return px.pie(
            df_all,
            values="Successes",
            names="Launch Site",
            title="Total Successful Launches by Site",
        )

    site_df = spacex_df[spacex_df["Launch Site"] == site]
    counts = (
        site_df["class"]
        .value_counts()
        .reindex([1, 0], fill_value=0)
        .rename(index={1: "Success", 0: "Failure"})
        .reset_index()
    )
    counts.columns = ["Outcome", "Count"]
    return px.pie(
        counts,
        values="Count",
        names="Outcome",
        title=f"Success vs Failure for {site}",
    )

@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [Input("site-dropdown", "value"), Input("payload-slider", "value")],
)
def update_scatter(selected_site, payload_range):
    if not payload_range or len(payload_range) != 2:
        payload_range = [min_payload, max_payload]
    low, high = payload_range

    df = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= low)
        & (spacex_df["Payload Mass (kg)"] <= high)
    ]

    site = (selected_site or "").strip()
    if site not in ("", "ALL"):
        df = df[df["Launch Site"] == site]
        title = f"Payload vs. Outcome for {site}"
    else:
        title = "Payload vs. Outcome for All Sites"

    return px.scatter(
        df,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        hover_data=["Launch Site", "Booster Version Category"],
        title=title,
        labels={"class": "Mission Outcome (1=Success, 0=Failure)"},
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
