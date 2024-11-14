################################################ CitiBike DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'CitiBike Strategy Dashboard', layout='wide')
st.title("CitiBike Ride Usage Strategy Dashboard")
st.markdown("The dashboard will help with the analysis and understanding of user behavior of CitiBike ride stations to assess bike distribution in New York.")
st.markdown("Since the Covid-19 pandemic, New York residents have increased their usage in bike sharing resulting in an increase in demand. CitiBike faces a distribution issue where riders are seeing fewer bikes at popular bike stations or stations full of docked bikes causing returns difficult for riders, which has caused an increase in customer complaints. This dashboard will help to uncover insight to combat these issues and aid in creating an optimal distribution strategy.")

########################## Import data ###########################################################################################

df = pd.read_csv(r"C:\Users\Drew\New_York_CitiBike\reduced_data_main_columns.csv")
df_random = pd.read_csv(r"C:\Users\Drew\New_York_CitiBike\reduced_data_random_set.csv")
top20_stations = pd.read_csv(r"C:\Users\Drew\New_York_CitiBike\top20_stations.csv")
df_member = pd.read_csv(r"C:\Users\Drew\New_York_CitiBike\member_usage_pie_plot.csv")
df_season = pd.read_csv(r"C:\Users\Drew\New_York_CitiBike\season_bar_chart.csv")
df_bike_type = pd.read_csv(r"C:\Users\Drew\New_York_CitiBike\bike_type_usage_pie.csv")
df_sample = pd.read_csv(r"C:\Users\Drew\New_York_CitiBike\bike_trips_avgTemp_line_plot.csv")

########################################## DEFINE THE CHARTS #####################################################################

## Bar chart

### Top 20 Stations

colorscale = [
    [0.0, '#004B87'],  # Darker shade of blue
    [0.5, '#0067B1'],  # CitiBike blue
    [1.0, '#66C5E9']   # Lighter blue, more saturated
]

fig_top20 = go.Figure(go.Bar(x = top20_stations['start_station_name'], y=top20_stations['value'], marker=dict(color=top20_stations['value'],colorscale=colorscale)))
fig_top20.update_layout(xaxis_tickangle=20)

fig_top20.update_layout(
    title = 'Top 20 Most Popular CitiBike Stations in New York',
    xaxis_title = 'Start Stations',
    yaxis_title = 'Number of Times Stations Used by Riders',
    width = 900, height = 600)
st.plotly_chart(fig_top20, use_container_width = True)

### Season Bike Usage 

colorscale = [
    [0.0, '#004B87'],  # Darker shade of blue
    [0.5, '#0067B1'],  # CitiBike blue
    [1.0, '#66C5E9']   # Lighter blue, more saturated
]

fig_season = go.Figure(go.Bar(x = df_season['season'], y=df_season['value'], marker=dict(color=df_season['value'],colorscale=colorscale)))
fig_season.update_layout()

fig_season.update_layout(
    title = 'Seasonal Bike Usage',
    xaxis_title = 'Season',
    yaxis_title = 'Number of Rides by Season',
    width = 900, height = 600)
st.plotly_chart(fig_season, use_container_width = True)

## Pie Chart

### Member Usage Comparison

colors = ['#004B87', '#0067B1']

fig_member = go.Figure(go.Pie(labels=df_member['member_casual'],values=df_member['value'],marker=dict(colors=colors),textinfo='percent+label'))

fig_member.update_layout(
    title='CitiBike Member Usage in New York',
    xaxis_title='Type of Rider',
    yaxis_title='Number of Trips by Riders',
    width=900, height=600)
st.plotly_chart(fig_member, use_container_width = True)

### Bike Type Usage Comparison

colors = ['#004B87', '#0067B1']

fig_bike_type = go.Figure(go.Pie(labels=df_bike_type['rideable_type'],values=df_bike_type['value'],marker=dict(colors=colors),textinfo='percent+label'))

fig_bike_type.update_layout(
    title='Comparison of Bike Type Used by Riders in New York',
    xaxis_title='Type of Bike',
    yaxis_title='Number of Trips by Riders',
    width=900, height=600)
st.plotly_chart(fig_bike_type, use_container_width = True)

## Line Chart

### Daily Bike Trips vs Average Temperature

fig_trip_temp = make_subplots(specs=[[{"secondary_y": True}]])

fig_trip_temp.add_trace(
    go.Scatter(
        x=df_sample['date'],
        y=df_sample['number_of_rides'],
        name='Daily Bike Rides',
        mode='lines',  # Only plot lines, not markers
        line=dict(color='blue'),
    ),
    secondary_y=False
)

fig_trip_temp.add_trace(
    go.Scatter(
        x=df_sample['date'],
        y=df_sample['avgTemp'],
        name='Daily Temperature',
        mode='lines',  # Only plot lines, not markers
        line=dict(color='red'),
    ),
    secondary_y=True
)

fig_trip_temp.update_layout(
    title='Daily Bike Trips vs Average Temperature in New York',
    width=900,
    height=600,
    xaxis_title="Date",
    yaxis_title="Number of daily bike rides",
    yaxis2_title="Average temperatures (°F)"
)

st.plotly_chart(fig_trip_temp, use_container_width = True)

## Add Kepler Map of Most Commonly Taken Station Trips

path_to_html = "CitiBike Bike Trips Aggregated Map.html"

# Read file and keep in variable of map
with open(path_to_html, 'r') as f:
    html_data = f.read()
    
## Show in web page
st.header("CitiBike Most Common Rides in New York")
st.components.v1.html(html_data,height=1000)