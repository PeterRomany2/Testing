import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Tracking System", layout="wide")




@st.cache_data
def load_daily():
    daily = pd.read_excel('Peter Assessment.xlsx', sheet_name='Daily Log')
    return daily

df = load_daily()



pd.set_option("display.max_rows", None)
pd.set_option("expand_frame_repr", False)

# Set the page config for a wide layout

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("You need to log in to access this page.")
    st.stop()  # Stop further execution of the page

lottie_html = """
<div style="position: fixed; top: 0; right: 0;">
<script src="https://unpkg.com/@lottiefiles/lottie-player@2.0.8/dist/lottie-player.js"></script><lottie-player src="https://lottie.host/360e8b4f-c02d-44db-ae3e-a65804e51260/wS4DxEonNm.json" background="##FFFFFF" speed="1" style="width: 150px; height: 100px;" loop controls autoplay direction="1" mode="normal"></lottie-player>

</div>

<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 400px; height: 100px;">
<h1 style="width: 400px; height: 100px;color:white;">Cleo Tracking System</h1>

</div>

<div style="position: fixed; top: 0; left: 0;">
<script src="https://unpkg.com/@lottiefiles/lottie-player@2.0.8/dist/lottie-player.js"></script><lottie-player src="https://lottie.host/360e8b4f-c02d-44db-ae3e-a65804e51260/wS4DxEonNm.json" background="##FFFFFF" speed="1" style="width: 150px; height: 100px;" loop controls autoplay direction="1" mode="normal"></lottie-player>

</div>

"""
components.html(lottie_html, height=60)


# Extract the date from the Timestamp column
df['Date'] = pd.to_datetime(df['Timestamp']).dt.date

# Calculate the count of interactions (inquiries) submitted by each agent per day
agent_productivity = df.groupby(['Name', 'Date']).size().reset_index(name='Interactions Count')

# Calculate additional metrics
total_interactions = df.shape[0]
total_agents = df['Name'].nunique()  # Using 'Name' instead of 'Email Address'
total_days = df['Date'].nunique()
max_interactions_agent = agent_productivity.groupby('Name')['Interactions Count'].sum().idxmax()  # Using 'Name'
max_interactions = agent_productivity.groupby('Name')['Interactions Count'].sum().max()



# Create three columns: left, middle (main content), and right
left_column, middle_column, right_column = st.columns([1, 6, 1])  # [left width, middle width, right width]

# Enhance the appearance of the metrics in the left column
with left_column:

    st.markdown(
        f"<div style='background-color: #fff3cd; border-radius: 10px; text-align: center; height: 120px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); "
        f"display: flex; flex-direction: column; justify-content: flex-start; align-items: center;'>"
        f"<h4 style='color: #e0a800; margin: 0; padding: 0;'>💬 Total Inquiries</h4>"
        f"<h3 style='color: #333; font-size: 36px; font-weight: bold; margin: 0; padding: 0;'>{total_interactions}</h3>"
        f"</div>",
        unsafe_allow_html=True
    )
    st.write('---')
    st.markdown(
        f"<div style='background-color: #fff3cd; border-radius: 10px; text-align: center; height: 120px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); "
        f"display: flex; flex-direction: column; justify-content: flex-start; align-items: center;'>"
        f"<h4 style='color: #e0a800; margin: 0; padding: 0;'>👥 Total Agents</h4>"
        f"<h3 style='color: #333; font-size: 36px; font-weight: bold; margin: 0; padding: 0;'>{total_agents}</h3>"
        f"</div>",
        unsafe_allow_html=True
    )
    st.write('---')
    st.markdown(
        f"<div style='background-color: #fff3cd; border-radius: 10px; text-align: center; height: 120px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); "
        f"display: flex; flex-direction: column; justify-content: flex-start; align-items: center;'>"
        f"<h4 style='color: #e0a800; margin: 0; padding: 0;'>📅 Total Days</h4>"
        f"<h3 style='color: #333; font-size: 36px; font-weight: bold; margin: 0; padding: 0;'>{total_days}</h3>"
        f"</div>",
        unsafe_allow_html=True
    )


# Enhance the appearance of the metrics in the right column
with right_column:
    st.markdown(
        f"<div style='background-color: #fff3cd; border-radius: 10px; text-align: center; height: 210px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); "
        f"display: flex; flex-direction: column; justify-content: center; align-items: center;'>"
        f"<h4 style='color: #e0a800; margin: 0; padding: 0;'>👑 Top Agent</h4>"
        f"<h3 style='color: #333; font-size: 36px; font-weight: bold; margin: 0; padding: 0;'>{max_interactions_agent}</h3>"
        f"</div>",
        unsafe_allow_html=True
    )
    st.write('---')
    # Agent with Max Interactions Metric
    st.markdown(
        f"<div style='background-color: #fff3cd; border-radius: 10px; text-align: center; height: 210px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); "
        f"display: flex; flex-direction: column; justify-content: center; align-items: center;'>"
        f"<h4 style='color: #e0a800; margin: 0; padding: 0;'>👑 Top Score</h4>"
        f"<h3 style='color: #333; font-size: 36px; font-weight: bold; margin: 0; padding: 0;'>{max_interactions}</h3>"
        f"</div>",
        unsafe_allow_html=True
    )

# Date Filter in Middle Column
with middle_column:
    unique_dates = sorted(df['Date'].unique())  # Get unique dates from the DataFrame
    selected_date = st.selectbox("Select a Date", unique_dates, format_func=lambda x: x.strftime('%Y-%m-%d'))

# Filter the data based on the selected date
filtered_data = agent_productivity[agent_productivity['Date'] == selected_date]

# Filtered Chart in the Middle Column
with middle_column:
    fig_filtered = px.bar(filtered_data,
                          x='Name',
                          y='Interactions Count',
                          title=f'Agent Productivity: Interactions on {selected_date.strftime("%Y-%m-%d")}',
                          labels={'Name': 'Agent', 'Interactions Count': 'Number of Interactions'},
                          color='Name',
                          barmode='stack')
    fig_filtered.update_traces(text=filtered_data['Interactions Count'],
                               textposition='outside',  # Positioning the text above the bars
                               texttemplate='%{y}')
    st.plotly_chart(fig_filtered, use_container_width=True)
    st.markdown("<hr>", unsafe_allow_html=True)



# Compute the agent summary (total interactions per agent)
agent_summary = agent_productivity.groupby('Name')['Interactions Count'].sum().reset_index()
agent_summary = agent_summary.sort_values(by='Interactions Count', ascending=False)

# Create two columns for the filtered data and agent summary side by side
left_column, right_column = st.columns([1, 1])

# Filtered Data Display with expander
with left_column:
    with st.expander(f"📅 Interactions on {selected_date.strftime('%Y-%m-%d')}", expanded=False):
        # Add some styling to the dataframe

        st.dataframe(filtered_data)

# Agent Summary Table Display with expander
with right_column:
    with st.expander("👩‍💻 Total Interactions per Agent", expanded=False):
        # Display the summary with enhanced styling
        st.dataframe(agent_summary)



st.write('---')

st.write("### 📈 Agent Performance Tracking Over Time")

col1, col2 = st.columns(2)

with col1:


    # Ensure 'Date' is in datetime format
    agent_productivity['Date'] = pd.to_datetime(agent_productivity['Date'])

    # Sort by Name and Date, and calculate the delta for each agent
    agent_productivity = agent_productivity.sort_values(by=['Name', 'Date'])
    agent_productivity['Delta'] = agent_productivity.groupby('Name')['Interactions Count'].diff().fillna(0)

    # Agent selection for delta visualization
    selected_agent = st.selectbox("Select an Agent", agent_productivity['Name'].unique())

    # Filter the data for the selected agent
    selected_agent_data = agent_productivity[agent_productivity['Name'] == selected_agent]

    # Create the line chart for the selected agent
    fig_line_agent = px.line(selected_agent_data,
                             x='Date',
                             y='Interactions Count',
                             title=f"Progress of {selected_agent} Over Time",
                             labels={'Date': 'Date', 'Interactions Count': 'Number of Interactions'},
                             markers=True)

    # Add annotations for delta values with enhanced colors
    for i in range(1, len(selected_agent_data)):
        delta_value = selected_agent_data['Delta'].iloc[i]

        # Determine the color for the delta annotation (green for positive, red for negative)
        delta_color = 'limegreen' if delta_value > 0 else 'red'

        # Adding the delta as annotations (displayed as text on the chart)
        fig_line_agent.add_annotation(
            x=selected_agent_data['Date'].iloc[i],
            y=selected_agent_data['Interactions Count'].iloc[i],
            text=f"Δ {delta_value:.0f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            ax=0,
            ay=-40,
            font=dict(size=16, color=delta_color),  # Change color based on delta value
            bgcolor="black",
        )

    # Display the chart for the selected agent
    st.plotly_chart(fig_line_agent, use_container_width=True)







with col2:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    default_agent = agent_productivity.groupby('Name')['Interactions Count'].sum().idxmax()

    fig_line_all = px.line(agent_productivity,
                           x='Date',
                           y='Interactions Count',
                           color='Name',
                           title="Progress of All Agents Over Time",
                           labels={'Date': 'Date', 'Interactions Count': 'Number of Interactions', 'Name': 'Agent'},
                           markers=True)

    for trace in fig_line_all.data:
        if trace.name != default_agent:
            trace.visible = 'legendonly'  # Hide the trace but keep it in the legend

    st.plotly_chart(fig_line_all, use_container_width=True)



st.write('---')
# New Chart: Stacked Bar Chart for Progress of All Agents
st.write("### 📊 Progress of All Agents Over Time (Bar Chart)")

fig_bar_all = px.bar(
    agent_productivity,
    x='Date',
    y='Interactions Count',
    color='Name',
    title="Progress of All Agents Over Time",
    labels={'Date': 'Date', 'Interactions Count': 'Number of Interactions', 'Name': 'Agent'},
    text_auto=True,  # Adds value labels to the bars
    barmode='stack',  # Stack bars for better comparison
)

st.plotly_chart(fig_bar_all, use_container_width=True)


st.write('---')



# print()








# Aggregate data for analysis
brand_counts = df['Brand'].value_counts().reset_index()
brand_counts.columns = ['Brand', 'Inquiry Count']
brand_counts['Percentage'] = (brand_counts['Inquiry Count'] / brand_counts['Inquiry Count'].sum()) * 100

brand_counts['Text'] = brand_counts.apply(
    lambda row: f"{row['Inquiry Count']} ({row['Percentage']:.2f}%)", axis=1
)


# Trends over time
brand_trends = df.groupby(['Date', 'Brand']).size().reset_index(name='Count')

# Channel distribution
channel_counts = df['Channel'].value_counts().reset_index()
channel_counts.columns = ['Channel', 'Count']




# Add custom CSS
st.markdown(
    """
    <style>
    .center-title {
        text-align: center;
        color: white; /* Optional: Customize text color */
        font-weight: bold;
        font-size: 2.5em; /* Optional: Adjust font size */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use the centered title
st.markdown("<h1 class='center-title'>Brand Inquiry Analysis</h1>", unsafe_allow_html=True)

st.write('---')



# Calculate the total inquiries across all brands
total_inquiries_all_brands = brand_counts['Inquiry Count'].sum()

st.write(
    f"<div style='text-align: center; font-size: 1.5em;'>Total Inquiries Across All Brands: <span style='color: limegreen; font-weight: bold;'>{total_inquiries_all_brands}</span></div>",
    unsafe_allow_html=True
)
# Contact Rates
bar_fig = px.bar(
    brand_counts,
    x='Brand',
    y='Inquiry Count',
    title="inquiry rate across various brands",
    text='Text',  # Display combined count and percentage
    color='Brand',
)
bar_fig.update_traces(texttemplate='%{text}', textposition='outside')
bar_fig.update_layout(
    yaxis_title="Inquiry Count",
    xaxis_title="Brand",
    title_font_size=16,
    showlegend=False
)
st.plotly_chart(bar_fig)
st.write('---')






# Grouping by Brand and Inquiry type to count inquiries of each type per brand
brand_inquiry_counts = df.groupby(['Brand', 'Inquiry']).size().reset_index(name='Inquiry Count')

# Calculate the total inquiries per brand (to calculate percentage)
brand_total_inquiries = brand_inquiry_counts.groupby('Brand')['Inquiry Count'].transform('sum')

# Calculate the percentage for each inquiry type based on the specific brand's total inquiries
brand_inquiry_counts['Percentage'] = (brand_inquiry_counts['Inquiry Count'] / brand_total_inquiries) * 100

# Create a text column to display the inquiry count and percentage
brand_inquiry_counts['Text'] = brand_inquiry_counts.apply(
    lambda row: f"{row['Inquiry Count']} ({row['Percentage']:.2f}%)", axis=1
)

# Sort the dataframe by 'Brand' first, and then by 'Inquiry Count' for each brand (descending order)
brand_inquiry_counts = brand_inquiry_counts.sort_values(by=['Brand', 'Inquiry Count'], ascending=[True, False])


st.subheader("Brand Inquiry Analysis: Count and Percentage Breakdown")

# Create an expander for the chart and the dataframe, showing one brand at a time
unique_brands = brand_inquiry_counts['Brand'].unique()

for brand in unique_brands:
    with st.expander(f"View Inquiry Count & Percentage for {brand}"):
        # Filter the data for the current brand
        brand_data = brand_inquiry_counts[brand_inquiry_counts['Brand'] == brand]

        # Total inquiries for the current brand
        total_inquiries_brand = brand_data['Inquiry Count'].sum()
        st.write(
            f"<div style='text-align: center; font-size: 1.5em;'>Total Inquiries for {brand}: <span style='color: limegreen; font-weight: bold;'>{total_inquiries_brand}</span></div>",
            unsafe_allow_html=True
        )

        # Inquiry count and percentage for the current brand
        bar_fig = px.bar(
            brand_data,
            x='Inquiry',
            y='Inquiry Count',
            title=f"Inquiry Count for {brand}",
            text='Text',  # Display combined count and percentage
            color='Inquiry',  # Different colors for each inquiry type
        )

        # Update layout and display options
        bar_fig.update_traces(texttemplate='%{text}', textposition='outside')
        bar_fig.update_layout(
            yaxis_title="Inquiry Count",
            xaxis_title="Inquiry Type",
            title_font_size=16,
            showlegend=False
        )

        # Display the chart
        st.plotly_chart(bar_fig)

st.write('---')























# Display the chart for the selected brand
col1, col2 = st.columns(2)
with col1:

    # Allow the user to select a brand
    selected_brand = st.selectbox("Select a Brand to Track", brand_trends['Brand'].unique())

    # Filter data for the selected brand
    selected_brand_data = brand_trends[brand_trends['Brand'] == selected_brand]

    # Calculate the delta values (change in inquiry count compared to the previous day)
    selected_brand_data['Delta'] = selected_brand_data['Count'].diff().fillna(0)

    # Inquiry Trends Over Time for the selected brand
    line_fig = px.line(
        selected_brand_data,
        x='Date',
        y='Count',
        title=f"Inquiry Trends for {selected_brand} Over Time",
        labels={'Date': 'Date', 'Count': 'Number of Inquiries'},
        markers=True
    )

    # Add annotations for the delta values with color-coding
    for _, row in selected_brand_data.iterrows():
        if row['Delta'] != 0:  # Only add delta annotations for non-zero delta
            delta_color = 'limegreen' if row['Delta'] > 0 else 'red'
            line_fig.add_annotation(
                x=row['Date'],
                y=row['Count'],
                text=f"Δ {int(row['Delta'])}",  # Delta text (rounded)
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                ax=0,
                ay=-40,
                font=dict(size=16, color=delta_color),  # Color based on delta value
                bgcolor="black",
            )

    st.plotly_chart(line_fig)


with col2:

    selected_brand = st.selectbox("Select a Brand to Track", brand_trends['Brand'].unique(),key="brand_selectbox2")
    selected_brand_data = df[df['Brand'] == selected_brand]

    brand_channel_trends = selected_brand_data.groupby(['Date', 'Channel']).size().reset_index(name='Count')

    # Inquiry Trends Over Time for the selected brand with Channel breakdown
    stacked_bar_fig = px.bar(
        brand_channel_trends,
        x='Date',
        y='Count',
        color='Channel',  # Different colors for each channel
        title=f"Inquiry Trends Over Time for {selected_brand} Clustered by Contact",
        labels={'Date': 'Date', 'Count': 'Number of Inquiries'},
    )

    # Update layout for better appearance
    stacked_bar_fig.update_layout(
        barmode='stack',  # Stacked bars to show contribution of each channel
        xaxis_title="Date",
        yaxis_title="Number of Inquiries",
        title=dict(font=dict(size=16))  # Adjust title font size
    )

    st.plotly_chart(stacked_bar_fig)

st.write('---')




# Add custom CSS
st.markdown(
    """
    <style>
    .center-title {
        text-align: center;
        color: white; /* Optional: Customize text color */
        font-weight: bold;
        font-size: 2.5em; /* Optional: Adjust font size */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use the centered title
st.markdown("<h1 class='center-title'>Brand Contact Rate Dashboard</h1>", unsafe_allow_html=True)

st.write('---')




# Channel Contact Rate Dashboard
channel_counts = df['Channel'].value_counts().reset_index()
channel_counts.columns = ['Channel', 'Inquiry Count']

# Calculate the contact rate (percentage) for each channel
total_inquiries = channel_counts['Inquiry Count'].sum()
channel_counts['Contact Rate (%)'] = (channel_counts['Inquiry Count'] / total_inquiries) * 100

# Add a column with the display text (Inquiry Count and Contact Rate)
channel_counts['Text'] = channel_counts.apply(
    lambda row: f"{row['Inquiry Count']} ({row['Contact Rate (%)']:.2f}%)", axis=1
)

# Create two columns for the charts
col1, col2 = st.columns(2)

# Column 1: Visualize the Contact Rate by Channel
with col1:
    bar_fig = px.bar(
        channel_counts,
        x='Channel',
        y='Inquiry Count',
        title="Contact Rate for All Brands",
        text='Text',  # Display Inquiry Count and Contact Rate
        color='Channel',  # Color bars by Channel
    )

    # Show the inquiry count and contact rate outside the bar
    bar_fig.update_traces(
        texttemplate='%{text}',
        textposition='outside'
    )

    # Update layout for better appearance
    bar_fig.update_layout(
        xaxis_title="Channel",
        yaxis_title="Inquiry Count",
        title=dict(font=dict(size=16)),  # Adjust title font size
        showlegend=False
    )

    # Display the plot
    st.plotly_chart(bar_fig)

# Column 2: Contact Rate by Channel and Brand
with col2:

    channel_brand_counts = df.groupby(['Channel', 'Brand']).size().reset_index(name='Inquiry Count')

    # Calculate the total inquiries for each channel
    channel_totals = channel_brand_counts.groupby('Channel')['Inquiry Count'].sum().reset_index()
    channel_totals.columns = ['Channel', 'Total Inquiries']

    # Merge the total inquiries with the individual counts
    channel_brand_counts = pd.merge(channel_brand_counts, channel_totals, on='Channel')
    channel_brand_counts['Contact Rate (%)'] = (channel_brand_counts['Inquiry Count'] / channel_brand_counts[
        'Total Inquiries']) * 100

    stacked_bar_fig = px.bar(
        channel_brand_counts,
        x='Channel',
        y='Inquiry Count',
        color='Brand',  # Different colors for different Brands
        title="Contact Rate for All Brands Clustered by Brand",
        labels={'Inquiry Count': 'Inquiry Count'},
    )

    # Update layout for better appearance
    stacked_bar_fig.update_layout(
        xaxis_title="Channel",
        yaxis_title="Inquiry Count",
        title=dict(font=dict(size=16)),  # Adjust title font size
        barmode='stack',  # Stack the bars to show multiple brands per channel
        showlegend=True  # Show legend for brands
    )

    # Display the plot
    st.plotly_chart(stacked_bar_fig)

st.write('---')





channel_brand_day_counts = df.groupby(['Date', 'Channel', 'Brand']).size().reset_index(name='Inquiry Count')


# Create two columns for the charts
col1, col2 = st.columns(2)

# Column 1: Visualize the Contact Rate by Channel Over Time (Filtered by Brand)
with col1:
    # Filter by Brand
    brands = df['Brand'].unique()  # Get list of unique brands
    selected_brand = st.selectbox("Select a Brand", brands)

    # Filter the data based on selected Brand
    filtered_data = channel_brand_day_counts[channel_brand_day_counts['Brand'] == selected_brand]

    # Visualize the Contact Rate by Channel Over Time (Filtered by Brand)
    stacked_bar_fig = px.bar(
        filtered_data,
        x='Date',
        y='Inquiry Count',
        color='Channel',  # Different colors for different Channels
        title=f"Contact Rate for {selected_brand} Over Time",
        labels={'Inquiry Count': 'Inquiry Count'},
    )

    # Update layout for better appearance
    stacked_bar_fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Inquiry Count",
        title=dict(font=dict(size=16)),  # Adjust title font size
        barmode='stack',  # Stack the bars to show inquiries per channel
        showlegend=True,  # Show legend for channels
        xaxis_tickangle=45,  # Rotate x-axis labels for better readability
    )

    # Display the plot
    st.plotly_chart(stacked_bar_fig)

# Column 2: Contact Rate by Channel Over Time (All Brands)
with col2:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    stacked_bar_all_brands_fig = px.bar(
        channel_brand_day_counts,
        x='Date',
        y='Inquiry Count',
        color='Channel',  # Different colors for different Channels
        title="Contact Rate for All Brands Over Time",
        labels={'Inquiry Count': 'Inquiry Count'},
    )

    # Update layout for better appearance
    stacked_bar_all_brands_fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Inquiry Count",
        title=dict(font=dict(size=16)),  # Adjust title font size
        barmode='stack',  # Stack the bars to show inquiries per channel
        showlegend=True,  # Show legend for channels
        xaxis_tickangle=45,  # Rotate x-axis labels for better readability
    )

    # Display the plot
    st.plotly_chart(stacked_bar_all_brands_fig)

st.write('---')



# print()


