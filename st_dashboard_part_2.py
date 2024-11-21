################################################ CitiBike DASHABOARD #####################################################

# Import Libraries

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image


########################### Initial settings for the dashboard ##################################################################

# Set the page configuration & title for the dashboard.
st.set_page_config(page_title = 'CitiBike Strategy Dashboard', layout='wide')
st.title('CitiBike Ride Usage Strategy Dashboard')

# # Create a sidebar with a title and a dropdown menu that allows users to select different aspects of the analysis to view on the dashboard

st.sidebar.title('Aspect Selector')
page = st.sidebar.selectbox('Select an aspect of the analysis',
                            ['Intro Page', 'Top 20 Most Popular Stations', 'Bike Type Usage Comparison', 'Seasonal Bike Usage', 'Daily Bike Trips vs Average Temperature in New York', 'Map of Most Commonly Taken Station Trips', 'Conclusion and Recommendations'])


########################## Import data ###########################################################################################

df = pd.read_csv("reduced_data_random_set.csv")
top20_stations = pd.read_csv("top20_stations.csv")
df_season = pd.read_csv("season_bar_chart.csv")
df_bike_type = pd.read_csv("bike_type_usage_pie.csv")
df_line = pd.read_csv("bike_trips_avgTemp_line_plot.csv")

########################################## DEFINE THE PAGES #####################################################################

### Intro Page

if page == 'Intro Page':
    st.markdown('The dashboard will help with the analysis and understanding of user behavior of CitiBike ride stations to assess bike distribution in New York.')
    st.markdown('Since the Covid-19 pandemic, New York residents have increased their usage in bike sharing resulting in an increase in demand. CitiBike faces a distribution issue where riders are seeing fewer bikes at popular bike stations or stations full of docked bikes causing returns difficult for riders, which has caused an increase in customer complaints. This dashboard will help to uncover insight to combat these issues and aid in creating an optimal distribution strategy.')
    st.markdown('The dashboard studies a sample portion of the data into the following:\n'
                '- Top 20 Most Popular Stations\n'
                '- Bike Type Usage\n'
                '- Seasonal Bike Usage\n'
                '- Daily Bike Trips vs Average Temperature in New York\n'
                '- Mapping the Most Commonly Taken Station Trips')
    
    rideshare = Image.open('CitiBike Picture.jpg') # Source: https://biketoworkday.us/how-to-use-citi-bike/
    st.image(rideshare, width = 900)
    st.markdown('Source: https://biketoworkday.us/how-to-use-citi-bike/')            

### Top 20 Most Popular Stations

# Check if the selected page is 'Top 20 Most Popular Stations'
elif page == 'Top 20 Most Popular Stations':

    # Create season filter in the sidebar to select which seasons to analyze
    with st.sidebar:
        season_filter = st.multiselect(label = 'Select the Season', options = df['season'].unique(),
        default = df['season'].unique())

     # Filter the DataFrame based on the selected seasons
    df1 = df.query('season == @season_filter')

    # Calculate total number of rides and display it using a metric
    total_rides = float(df1['number_of_rides'].count())
    st.metric(label = 'Total Bike Rides', value = numerize(total_rides))

    ## Bar chart creation

     # Add 'value' column to the DataFrame for counting occurrences, then group by station name to get ride counts
    df1['value'] = 1
    df_groupby_bar = df1.groupby('start_station_name', as_index=False).agg({'value':'sum'})
    top20_stations = df_groupby_bar.nlargest(20,'value')

    # Define color scale for the bar chart
    colorscale = [
    [0.0, '#004B87'],  # Darker shade of blue
    [0.5, '#0067B1'],  # CitiBike blue
    [1.0, '#66C5E9']   # Lighter blue, more saturated
    ]

    # Create a bar chart of the top 20 stations
    fig_top20 = go.Figure(go.Bar(x = top20_stations['start_station_name'], y=top20_stations['value'], marker=dict(color=top20_stations['value'],colorscale=colorscale)))
    fig_top20.update_layout(xaxis_tickangle=20)

    fig_top20.update_layout(
    title = 'Top 20 Most Popular CitiBike Stations in New York',
    xaxis_title = 'Start Stations',
    yaxis_title = 'Number of Times Stations Used by Riders',
    width = 900, height = 600)
    st.plotly_chart(fig_top20, use_container_width = True)
   
    # Markdown text section with analysis and insights
    st.markdown('### Overall Seasonal Analysis of Stations:\n'
                '- **Leading Station**: West 21st St & 6th Ave consistently has the highest number of rides over the seasons, showing its importance as a central hub.\n'
                '-  Stations along Broadway and 6th Ave are some of the most frequented, indicating their role as central points for both commuter and tourist riders.\n'
                '- **Inventory Management Insight**: To address high demand, consider expanding the bike inventory and docking capacity at these key stations to help alleviate issues of unavailability during peak times and minimize customer complaints.\n')
    st.markdown('### Winter Season Analysis of Stations:\n'
                '- **Leading Station**: West 21st St & 6th Ave remains the highest grossing number of rides among users.\n'
                '- **Inventory Management Insight**:  During winter, consider slightly reducing bike inventory to maintain bike condition for unneeded inventory over winter, while ensuring enough availability for consistent winter riders.\n'
                '- **Safety Insight**: Introduce winter tires for bikes at popular stations like West 21st St & 6th Ave. Monitor rider activity to see if additional winter-optimized bikes might be needed.\n')
    st.markdown('### Spring Season Analysis of Stations:\n'
                '- **Leading Stations**: Chambers St & West St station becomes the highest-ranked, likely due to its proximity to parks, attracting more riders during spring.\n'
                '- **Inventory Management Insight**: Focus on keeping bike inventory available near popular parks, such as Central Park, during springtime to support increased recreational use.\n'
                '- **Operational Insight**: Consider running promotional campaigns to boost rider engagment during this season.')
    st.markdown('### Summer Season Analysis of Stations:\n'
                '- **Leading Stations**: Chambers St & West St station is the busiest, driven by both recreational and commuter use.\n'
                '- **Inventory Management Insight**: During peak summer months, ensure sufficient bike availability at popular recreational and commuter stations.\n'
                '- **Operational Insight**: Real-time rebalancing and frequent checks on bike inventory will be necessary to ensure availability and reduce customer dissatisfaction during high demand periods.')
    st.markdown('### Fall Season Analysis of Stations:\n'
                '- **Leading Stations**: West 21st & 6th Ave holds the top spot, while Broadway & West 58th St has moved to second place. University stations are showing moderate activity, likely due to student riders in the fall semester.\n'
                '- **Inventory Management Insight**: Increase bike inventory at stations near universities to meet the needs of students returning for the semester.\n'
                '- **Operational Insight**: Provide student commuters with discounts to encourage ride  growth and market student engagement activities to encourage more activity from younger generation.')
                
                  
## Pie Chart Creations
                
### Bike Type Usage Comparison

# Check if the selected page is 'Bike Type Usage Comparison'
elif page == 'Bike Type Usage Comparison':

    # Create user filter in the sidebar to select which user type (member/casual) to analyze
    with st.sidebar:
        user_filter = st.multiselect(label = 'Select the User', options = df['member_casual'].unique(),
        default = df['member_casual'].unique())

    # Filter the DataFrame based on the selected user type    
    df3 = df.query('member_casual == @user_filter')

    # Calculate and display the total number of rides using a metric
    total_rides = float(df3['number_of_rides'].count())
    st.metric(label = 'Total Bike Rides', value = numerize(total_rides))

    # Add 'value' column for counting occurrences, then group by bike type and user type to get ride counts
    df3['value'] = 1
    df_bike_type = df3.groupby(['rideable_type','member_casual'], as_index=False).agg({'value':'sum'})
    
    # Define colors for the pie chart
    colors = ['#004B87', '#0067B1']

    # Create a pie chart to visualize bike type   
    fig_bike_type = go.Figure(go.Pie(labels=df_bike_type['rideable_type'],values=df_bike_type['value'],marker=dict(colors=colors),textinfo='percent+label'))
    fig_bike_type.update_layout(
    title='Comparison of Bike Type Used by Riders in New York',
    xaxis_title='Type of Bike',
    yaxis_title='Number of Trips by Riders',
    width=1000, height=700)
    st.plotly_chart(fig_bike_type, use_container_width = True)
    
    # Markdown text section with analysis and insights
    st.markdown('### Overall Bike Type Usage Analysis.\n'
                '- Classic bikes are the preferred choice for users, accounting for **61%** of total rides, which is almost **1.5** times the usage of electric bikes at **39%**.\n'
                '- **Inventory Management Insight**: To meet the high demand for classic bikes, increase their inventory, especially during high-demand periods, to alleviate user complaints about bike availability.\n'
                '- **Operational Insight**: Although electric bikes are less frequently used, their consistent usage at **39%** indicates that maintaining or slightly increasing their availability during peak seasons and at popular stations could encourage more casual and commuter riders.\n'
                '- **Member Usage**: Member riders account for the majority of bike trips compared to casual riders. This indicates that members are more significantly impacted by inventory shortages, particularly during high demand periods.')
    st.markdown('### Member Usage Analysis.\n'
                '- Members clearly prefer classic bikes over electric bikes by a margin of around **20%**. This preference could be influenced by factors such as cost and riding comfort.\n'
                '- **Inventory Management Insight**: Focus on ensuring enough classic bikes are available in areas frequented by members during commuting hours to match their higher preference rate.\n'
                '- **Inventory Managment Insigh**: Consider allocating additional electric bikes in areas where convenience is prioritized, such as near transit hubs, to potentially attract members seeking faster options.')
    st.markdown('### Casual User Analysis.\n'
                '- Casual riders also show a significant preference for classic bikes, with around **62%** of rides compared to the **38%** for electric bikes.\n'
                '- **Operational Insight**: Since casual riders lean more toward classic bikes, consider focusing marketing and inventory availability strategies on making classic bikes easily accessible in tourist areas, especially during weekends and peak tourist seasons.\n'
                '- **Conversion Insight**: Given the steady usage of electric bikes, promote the benefits of electric bikes, such as less effort and longer range, through targeted campaigns to potentially increase their usage among casual riders.')

    
### Season Bike Usage

# Check if the selected page is 'Seasonal Bike Usage'
elif page == 'Seasonal Bike Usage':

    # Create user filter in the sidebar to select which user type (member/casual) to analyze
    with st.sidebar:
        user_filter = st.multiselect(label = 'Select the User', options = df['member_casual'].unique(),
        default = df['member_casual'].unique())

     # Filter DataFrame based on the selected user type    
    df2 = df.query('member_casual == @user_filter')

    # Calculate and display the total number of rides using a metric
    total_rides = float(df2['number_of_rides'].count())
    st.metric(label = 'Total Bike Rides', value = numerize(total_rides))

    # Add a value column for counting occurrences, then group by season and user type to get ride counts
    df2['value'] = 1
    df_season = df2.groupby(['season','member_casual'], as_index=False).agg({'value':'sum'})

    # Define colors for different user types
    colors = {
    'member': '#004B87',  # Dark blue for members
    'casual': '#66C5E9'   # Light blue for casual users
    }

    # Create a bar chart
    fig_season = go.Figure()
    
    # Loop through each type of user to create separate bars
    for user_type in df_season['member_casual'].unique():
        user_data = df_season[df_season['member_casual'] == user_type]
        fig_season.add_trace(go.Bar(
        x=user_data['season'],
        y=user_data['value'],
        name=user_type,  # Add legend label for the user type
        marker_color=colors[user_type]
        ))

    fig_season.update_layout(
        title = 'Seasonal Bike Usage',
        xaxis_title = 'Season',
        yaxis_title = 'Number of Rides by Season',
        width = 900, height = 600)
        
    st.plotly_chart(fig_season, use_container_width = True)
    
    # Markdown text section with analysis and insights
    st.markdown('### Overall Seasonal Bike Usage Analysis.\n'
            '- The graph shows a clear variation amongst rides during the seasons.\n'
            '- **Summer**: Accounts for roughly **46%** of total rides and is the clear dominant peak time of the seasons, likely due to warm weather allowing riders increased leisure and commuting opportunities.\n'
            '- **Winter**: Accounts for around **27%** of total rides, making it the second-highest for number of rides among the seasons. This shows that dedicated riders are still active despite the cold and snowy weather.\n'
            '- **Spring**: Shows the least amount of rides, accounting for around 10% of total rides. This may be due to unpredictable weather changes, such as rain and fluctuating temperatures, which could discourage bike riding. Additionally, some potential riders might prefer to enjoy springtime by foot before summer hits.')
    st.markdown('### Seasonal Bike Usage for Casual Riders Analysis.\n'
            '- **Summer**: Casual riders are most active during the summer, with around 49% of casual rides occurring in this period, likely driven by tourists and outdoor activities.\n'
            '- **Winter & Fall**: Winter accounts for **23%** of casual rides, while Fall accounts for **15%**. Casual riders are likely taking advantage of bike availability for weekend or leisure activities even during colder months.\n'
            '- **Spring**: Accounts for only **13%** of rides among casual riders, indicating an opportunity for engagement campaigns during this period.')
    st.markdown('### Seasonal Bike Usage for Member Riders Analysis.\n'
            '- **Summer**: Members show peak activity in the summer, accounting for 45% of rides, highlighting high demand for commuting and outdoor activities.\n'
            '- **Winter & Fall**: Winter usage is consistent at 28%, while Fall contributes 19%, indicating loyalty among members even during colder periods.\n'
            '- **Spring**: Accounts for around 9% of member rides, suggesting a need for engagement campaigns during this period to increase usage.')
    st.markdown('**Operational Insight**: To ensure availability during peak season, increase inventory in summer to meet high demand. Consider rebalancing bike distribution to focus more on areas with high leisure or tourism activity during summer.')
    st.markdown('**Engagement Boost Insight**: Focus promotional events or seasonal discounts during the fall, winter, and spring periods to gain rider engagement during non-peak seasons to encourage more rides.')

                

### Daily Bike Trips vs Average Temperature

# Check if the selected page is 'Daily Bike Trips vs Average Temperature in New York'
elif page == 'Daily Bike Trips vs Average Temperature in New York':

    ## Line Chart Creation
    
    # Create a subplot with secondary y-axis for temperature and bike trips
    fig_trip_temp = make_subplots(specs=[[{"secondary_y": True}]])

    # Add line trace for daily bike rides (primary y-axis)
    fig_trip_temp.add_trace(
    go.Scatter(
        x=df_line['date'],
        y=df_line['number_of_rides'],
        name='Daily Bike Rides',
        mode='lines',  # Only plot lines, not markers
        line=dict(color='blue'),
    ),
    secondary_y=False
    )

    # Add line trace for average daily temperature (secondary y-axis)
    fig_trip_temp.add_trace(
    go.Scatter(
        x=df_line['date'],
        y=df_line['avgTemp'],
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
    xaxis_title='Date',
    yaxis_title='Number of daily bike rides',
    yaxis2_title='Average temperatures (°F)'
    )

    st.plotly_chart(fig_trip_temp, use_container_width = True)
    
    # Markdown text section with analysis and insights
    st.markdown('### Correlation of Average Temperature and Bike Trips Analysis\n'
                '- There is a clear and strong correlation between average temperature and the number of bike trips. As temperatures rise, the number of bike trips begin to increase, peaking during the summer months. While as the temperature gets colder, there is a decline in rides. Despite the decline in rides, usage was found to remain surprisingly higher than expected, highlighting consistent demand among dedicated riders.')
    st.markdown('### Seasonal Peaks and Declines Analysis.\n'
                '- **Peak Periods**: The highest peaks in bike usage are observed during the summer months, from June to August, when average temperatures are at their warmest. During these months, average daily trips frequently exceed 80,000 rides.\n'
                '- **Increasing Rides**: A gradual increase in bike usage starts from March, as temperatures warm up, showing a steady rise towards summer.\n'
                '- **Decline in Usage**: A decline begins in November as temperatures cool, with the coldest months, December to February, showing lower daily rides compared to summer, though winter still ranks second among all seasons.')
    st.markdown('**Inventory Management for Peak Periods**: During peak months, such as June to August, increase bike availability to meet high demand by reallocating inventory to high-traffic areas, including stations around central park, coastline stations, and university zones.')
    st.markdown('**Inventory Management for Colder Periods**: During the colder period months of November to April, ensure sufficient inventory for winter demand but optimize costs by reducing excess supply by around **38%** where feasible, such as from least popular station areas.\n')
    st.markdown('**Engagement Boost Insight**: During colder periods, develop incentive programs for bike usage through promotional discounts or targeted marketing campaigns to encourage riding during colder periods to help encourage even more engagement during the colder period.')
    
### Add Kepler Map of Most Commonly Taken Station Trips

elif page == 'Map of Most Commonly Taken Station Trips':
    
    path_to_html = 'CitiBike Bike Trips Aggregated Map.html'

    # Read file and keep in variable of map
    with open(path_to_html, 'r') as f:
        html_data = f.read()
    
    ## Show in web page random sample data size due to size of file 
    st.header('CitiBike Most Common Rides in New York')
    st.components.v1.html(html_data,height=850)
    
    # Markdown text section with analysis and insights
    st.markdown('The map shows that the most common bike trips revolve around the central Manhattan area.') 
    st.markdown('Frequent routes are found around New York University and Columbia University, likely due to proximity to universities, commercial centers, and public transit.')
    st.markdown('The map also shows many trips along the Manhattan coastline, coinciding with the Hudson River Greenway.') 
    st.markdown('These coastline routes provide both recreational and commuter riders with scenic access to various parts of the city, serving as a major thoroughfare.')
    st.markdown('Central Park sees frequent activity along its perimeter, particularly connecting between the park and Columbus Circle.') 
    st.markdown('Central Park acts as a key connecting hub for bikers traveling between Upper Manhattan and Midtown, aiding work commutes, school trips, and social gatherings.')

### Conclusion and Recommendations Page

elif page == 'Conclusion and Recommendations':
    
    st.header('Conclusion and Recommendations')
    st.markdown('### Key Conclusions:\n'
                '- **Leading Stations**: West 21st St & 6th Ave consistently has the highest number of rides, indicating its strategic importance as a central commuter or tourist hub. While, stations along Broadway and 6th Ave have frequented locations that also suggest their role as commuter hubs.\n'
                '- **Member Usage**: Member riders dominate usage at around **72%**, emphasizing the need to ensure bike availability to maintain loyalty. Casual riders make up around **28%** of rides, indicating possible conversion opportunities to increase loyalty members.\n'
                '- **Seasonal and Temperature Rides**: There was found to be a clear correlation between temperature and bike trips. It was found that summer had the highest number of rides between both member and casual riders. While, the number of rides began to drop during winter periods, there was still a frequent dedicated number of riders during the winter periods.\n'
                '- **Geographical Insight**: Central Manhattan areas, such as near New York University, Columbia University, Hudson River Greenway, and Central Park, saw high activity levels and showed great importance as major hubs for commuters, students, and recreational riders.')
    st.markdown('### Recommendations:\n'
                '**Inventory Management**:\n'
                '- Increase inventory during summer peak periods to counter the high-demands. Real-time rebalancing and proactive inventory checks should be performed to best avoid shortages.\n'
                '- Prioritize inventory availability in high-demand areas, such as leisure/tourist zones during summer and university areas during the fall.\n' 
                '- Reduce inventory in off-peak seasons, such as winter and spring, to maintain bike conditions and ensure consistent docking availability.\n'
                '- Expand the number of classic bikes, given their higher demand, to address customer complaints regarding availability.')
    st.markdown('**Operational and Safety Initiatives**:\n'
                '- Implement a safety initiative that includes adding winter tires on bikes during the winter season to enhance usability and attract more rides in colder weather')
    st.markdown('**Marketing Opportunities**:\n'
                '- Develop promotional efforts to convert casual riders into members, such as discounted memberships highlighting the benefits of being a member.\n'
                '- Launch marketing campaigns and seasonal discounts during off-peak periods, such as fall and winter, to maintain rider engagement during quieter times.\n'
                '- Promote recreational activities around parks and river routes in spring and summer to attract more casual and tourist riders.\n')
    st.markdown('**Community Engagement Opportunities**:\n'
                '- Offer discounts or special promotions to university students during fall and spring semesters to boost engagement among younger riders.')
                
