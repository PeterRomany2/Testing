import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
pd.set_option("display.max_rows", None)
pd.set_option("expand_frame_repr", False)
st.set_page_config(page_title="Delivery Complains", layout="wide")

# Load Escalation Sheet data
@st.cache_data
def load_escalation_data():
    escalation_sheet = pd.read_excel('Peter Assessment.xlsx', sheet_name='Escalation Sheet')
    return escalation_sheet

escalation_sheet = load_escalation_data()


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("You need to log in to access this page.")
    st.stop()  # Stop further execution of the page












# Handle missing data and incorrect entries
escalation_sheet = escalation_sheet.dropna(subset=['Total Order Amount'])
escalation_sheet.drop(escalation_sheet[escalation_sheet['Total Order Amount'] == "visa"].index, inplace=True)
escalation_sheet['Total Order Amount'] = escalation_sheet['Total Order Amount'].astype(int)

# Filter relevant columns
escalation_data = escalation_sheet[['Timestamp', 'The Brand name', 'Complaint Type', 'Priorty']]

# Brands of interest (these are the brands receiving deliveries from Flextock)
brands_of_interest = ['Dermatique', 'Blankie', 'Cleo']
escalation_data = escalation_data[escalation_data['The Brand name'].isin(brands_of_interest)]

# Delivery-related complaints
delivery_issues = [
    'Wrong Item (Gift the customer with picture)',
    'Missing Item (Gift the customer without picture)',
    'Damaged-Broken  (Gift the customer & ask for picture before 48 h after receiving the order to open a ticket in the shipping company)'
]
escalation_data = escalation_data[escalation_data['Complaint Type'].isin(delivery_issues)]

# Parse date for time-based analysis
escalation_data['Date'] = pd.to_datetime(escalation_data['Timestamp']).dt.date

# Convert 'Month' to datetime to avoid the "Period" error in Plotly
escalation_data['Month'] = pd.to_datetime(escalation_data['Timestamp']).dt.to_period('M').dt.to_timestamp()

# Filter data to include only the first 15 days of the month
escalation_data['Day'] = pd.to_datetime(escalation_data['Timestamp']).dt.day
escalation_data_first_half = escalation_data[escalation_data['Day'] <= 15]

# Group complaints by brand and complaint reason
complaints_by_brand_and_reason = escalation_data.groupby(['The Brand name', 'Complaint Type']).size().reset_index(name='Count')

# Dashboard Title and Intro
st.markdown(
    """
    <div style='text-align: center; font-size: 2em; font-weight: bold;'>
        Flextock Delivery Company Complaints Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

# Section 2: Complaint Reason Breakdown (Overall, not filtered by brand)
reason_breakdown = escalation_data['Complaint Type'].value_counts().reset_index()
reason_breakdown.columns = ['Complaint Type', 'Count']

# Calculate the total number of complaints across all brands
total_complaints_all_brands = complaints_by_brand_and_reason['Count'].sum()

# Display total complaints across all brands
st.write(
    f"<div style='text-align: center; font-size: 1.5em;'>Total Complaints Overall: <span style='color: limegreen; font-weight: bold;'>{len(escalation_sheet)}</span></div>",
    unsafe_allow_html=True
)


st.write(
    f"<div style='text-align: center; font-size: 1.5em;'>Total Complaints Related to Flextock: <span style='color: limegreen; font-weight: bold;'>{total_complaints_all_brands}</span></div>",
    unsafe_allow_html=True
)
# Create a pie chart to show the breakdown of complaints by reason
pie_chart = px.pie(
    reason_breakdown,
    names='Complaint Type',
    values='Count',
    title="Count & Percentage of Complaint Reasons Related to Flextock"
)
st.plotly_chart(pie_chart)

complaint_type_rename = {
    'Wrong Item (Gift the customer with picture)': 'Wrong Item',
    'Missing Item (Gift the customer without picture)': 'Missing Item',
    'Damaged-Broken  (Gift the customer & ask for picture before 48 h after receiving the order to open a ticket in the shipping company)': 'Damaged-Broken'
}

# Rename complaint types using the dictionary
escalation_data['Complaint Type'] = escalation_data['Complaint Type'].map(complaint_type_rename)

# Group complaints by Complaint Type (Reason) and Brand
complaints_by_reason_and_brand = escalation_data.groupby(['Complaint Type', 'The Brand name']).size().reset_index(name='Complaint Count')

# Calculate the percentage for each complaint type within each brand
complaints_by_reason_and_brand['Percentage'] = complaints_by_reason_and_brand.groupby('The Brand name')['Complaint Count'].transform(lambda x: (x / x.sum()) * 100)

# Create the 'Text' column for labels that combine count and percentage
complaints_by_reason_and_brand['Text'] = complaints_by_reason_and_brand['Complaint Count'].astype(str) + ' (' + complaints_by_reason_and_brand['Percentage'].round(1).astype(str) + '%)'


# Create a bar chart to visualize complaints categorized by reason (on x-axis) and brand (color)
bar_fig = px.bar(
    complaints_by_reason_and_brand,
    x='Complaint Type',
    y='Complaint Count',
    color='The Brand name',
    title="Complaint Reasons Categorized by Brand",
    labels={"Complaint Type": "Complaint Reason", "Complaint Count": "Number of Complaints"},
    barmode="stack",
    text='Text',  # Display combined count and percentage
)

# Update the text display on the bars
bar_fig.update_traces(texttemplate='%{text}', textposition='outside')

# Update layout for better readability
bar_fig.update_layout(
    yaxis_title="Number of Complaints",
    xaxis_title="Complaint Reason",
    title_font_size=16,
    showlegend=True,
    xaxis=dict(
        tickangle=45,  # Rotate x-axis labels
        tickfont=dict(size=10),  # Adjust the font size for x-axis labels
    )
)

st.write('---')
complaints_by_brand_and_reason['Complaint Type'] = complaints_by_brand_and_reason['Complaint Type'].replace(complaint_type_rename)
total_complaints_per_type = complaints_by_brand_and_reason.groupby('Complaint Type')['Count'].sum().reset_index()
complaint_type_metrics = total_complaints_per_type.set_index('Complaint Type')['Count'].to_dict()

st.markdown(
    """
    <div style='display: flex; justify-content: center; flex-wrap: wrap;'>
        <div style='text-align: center; margin: 10px;'>
            <h3 style='color: limegreen;'>Wrong Item</h3>
            <p style='font-size: 1.2em;'>Complaints: {}</p>
        </div>
        <div style='text-align: center; margin: 10px;'>
            <h3 style='color: orange;'>Missing Item</h3>
            <p style='font-size: 1.2em;'>Complaints: {}</p>
        </div>
        <div style='text-align: center; margin: 10px;'>
            <h3 style='color: blue;'>Damaged-Broken</h3>
            <p style='font-size: 1.2em;'>Complaints: {}</p>
        </div>
    </div>
    """.format(
        complaint_type_metrics.get('Wrong Item', 0),
        complaint_type_metrics.get('Missing Item', 0),
        complaint_type_metrics.get('Damaged-Broken', 0)
    ),
    unsafe_allow_html=True
)

# st.plotly_chart(bar_fig)



# Group complaints by Complaint Type and Brand (same as before)
complaints_by_reason_and_brand = escalation_data.groupby(['Complaint Type', 'The Brand name']).size().reset_index(name='Complaint Count')

# Calculate the percentage for each complaint type within each brand
complaints_by_reason_and_brand['Percentage'] = complaints_by_reason_and_brand.groupby('The Brand name')['Complaint Count'].transform(lambda x: (x / x.sum()) * 100)

# Create the 'Text' column for labels that combine count and percentage
complaints_by_reason_and_brand['Text'] = complaints_by_reason_and_brand['Complaint Count'].astype(str) + ' (' + complaints_by_reason_and_brand['Percentage'].round(1).astype(str) + '%)'

# Create a grouped bar chart to visualize complaints by Complaint Type and Brand
grouped_bar_fig = px.bar(
    complaints_by_reason_and_brand,
    x='Complaint Type',  # x-axis for complaint type
    y='Complaint Count',
    color='The Brand name',  # Group bars by brand (colors represent the brands)
    title="Complaints Reasons Related to Flextock Clustered by Brand",
    labels={"Complaint Type": "Complaint Reason", "Complaint Count": "Number of Complaints"},
    barmode="group",  # Group bars side by side for each complaint type
    text='Text',  # Display combined count and percentage
)

# Update the text display on the bars
grouped_bar_fig.update_traces(texttemplate='%{text}', textposition='outside')

# Update layout for better readability
grouped_bar_fig.update_layout(
    yaxis_title="Number of Complaints",
    xaxis_title="Complaint Type",
    title_font_size=16,
    showlegend=True,
    xaxis=dict(
        tickangle=45,  # Rotate x-axis labels for better readability
        tickfont=dict(size=10),  # Adjust font size for x-axis labels
    )
)

# Display the grouped bar chart
st.plotly_chart(grouped_bar_fig)








st.write('---')




# Provided data for late orders and Flextock responsibility
late_order_metrics = {
    'Cleo': {'Total Late Orders': 808, 'Flextock Responsible': 808},
    'Blankie': {'Total Late Orders': 745, 'Flextock Responsible': 745},
    'Dermatique': {'Total Late Orders': 531, 'Flextock Responsible': 531},
    'Skinside': {'Total Late Orders': 616, 'Flextock Responsible': 0},  # Flextock is not responsible for this brand
    'Cleo (StudioSkin)': {'Total Late Orders': 323, 'Flextock Responsible': 0},  # Flextock is not responsible for this brand
    'Kayanek': {'Total Late Orders': 271, 'Flextock Responsible': 0}  # Flextock is not responsible for this brand
}

# Title of the dashboard
st.markdown("<h1 style='text-align: center;'>Late Orders Inquiries & Flextock Responsibility</h1>", unsafe_allow_html=True)
st.write(
    f"<div style='text-align: center; font-size: 1.5em;'>Total Late Order Inquiries: <span style='color: limegreen; font-weight: bold;'>3294 Orders</span></div>",
    unsafe_allow_html=True
)

# Calculate total late orders and Flextock responsibility
total_late_orders = sum([metrics['Total Late Orders'] for metrics in late_order_metrics.values()])
total_flextock_responsible = sum([metrics['Flextock Responsible'] for metrics in late_order_metrics.values()])

# Function to create circular metric (progress bar) with smaller circle
def create_circular_metric(value, max_value, label):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': label},
        gauge={'axis': {'range': [0, max_value]},
               'bar': {'color': "limegreen"},
               'steps': [{'range': [0, max_value], 'color': "lightgray"}]},
        domain={'x': [0.1, 0.9], 'y': [0.1, 0.9]}  # Adjust the domain to make the circle smaller
    ))
    return fig

# Create two columns for side-by-side display
col1, col2 = st.columns(2)

# First column: Total Late Orders
with col1:
    fig2 = create_circular_metric(total_flextock_responsible, 2084, "Flextock Responsibility")
    st.plotly_chart(fig2, use_container_width=True)


# Second column: Total Flextock Responsibility
with col2:
    brand_metrics = {
        'Cleo': 808,
        'Blankie': 745,
        'Dermatique': 531,
        'Skinside': 0,  # Flextock is not responsible for this brand
        'Cleo (StudioSkin)': 0,  # Flextock is not responsible for this brand
        'Kayanek': 0  # Flextock is not responsible for this brand
    }

    # Display brand responsibility metrics in a similar way as the complaint types
    st.markdown(
        """
        <div style='display: flex; justify-content: center; flex-wrap: wrap;'>
            <div style='text-align: center; margin: 10px;'>
                <h3 style='color: limegreen;'>Cleo</h3>
                <p style='font-size: 1.2em;'>Flextock Responsible For: {} Orders</p>
            </div>
            <div style='text-align: center; margin: 10px;'>
                <h3 style='color: orange;'>Blankie</h3>
                <p style='font-size: 1.2em;'>Flextock Responsible For: {} Orders</p>
            </div>
            <div style='text-align: center; margin: 10px;'>
                <h3 style='color: blue;'>Dermatique</h3>
                <p style='font-size: 1.2em;'>Flextock Responsible For: {} Orders</p>
            </div>
        </div>
        """.format(
            brand_metrics.get('Cleo', 0),
            brand_metrics.get('Blankie', 0),
            brand_metrics.get('Dermatique', 0)
        ),
        unsafe_allow_html=True
    )





lottie_html = """


<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">

<script src="https://unpkg.com/@lottiefiles/lottie-player@2.0.8/dist/lottie-player.js"></script><lottie-player src="https://lottie.host/12b7ed42-a5ed-4279-b74f-2f005d9dead3/CQa6sLq1Bl.json" background="##ffffff" speed="1" style="width: 300px; height: 300px" loop controls autoplay direction="1" mode="normal"></lottie-player>
</div>


"""
components.html(lottie_html, height=200)


# Display a good goodbye message
st.markdown(
    """
    <div style='text-align: center; font-size: 2em; font-weight: bold; color: #4CAF50;'>
                    Thank you for using Cleo Website, Mr. Omar! <br>
            Have a wonderful day! 😊
    </div>
    """, unsafe_allow_html=True
)
