import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Refund Analysis", layout="wide")



@st.cache_data
def load_refund():
    refund = pd.read_excel('Peter Assessment.xlsx', sheet_name='Refunds')
    return refund

df = load_refund()



pd.set_option("display.max_rows", None)
pd.set_option("expand_frame_repr", False)
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("You need to log in to access this page.")
    st.stop()  # Stop further execution of the page



refund_counts = df.groupby(['The Brand name', 'Reason of Refunds']).size().reset_index(name='Refund Count')

# Calculate total refund count and total refund amount per brand
brand_totals = df.groupby('The Brand name').agg(
    TotalRefundCount=('Reason of Refunds', 'count'),
    TotalRefundAmount=('Refund Amount', 'sum')
).reset_index()

# Merge the totals with the counts dataframe
refund_counts = refund_counts.merge(brand_totals, on='The Brand name')

# Calculate percentage of refunds per reason (per brand)
refund_counts['Percentage'] = (refund_counts['Refund Count'] / refund_counts['TotalRefundCount']) * 100

# Create a text column for visualization
refund_counts['Text'] = refund_counts.apply(
    lambda row: f"{row['Refund Count']} ({row['Percentage']:.2f}%)", axis=1
)

# Add custom CSS for title and metrics
st.markdown(
    """
    <style>
    .center-title {
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 2.5em;
    }

    .metric-container {
        display: flex;
        justify-content: space-between;
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    .metric-item {
        font-size: 1.2em;
        font-weight: bold;
        color: #333;
    }

    .metric-value {
        font-size: 1.8em;
        font-weight: bold;
        color: limegreen;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use the centered title
st.markdown("<h1 class='center-title'>Refund Reasons Rate Dashboard</h1>", unsafe_allow_html=True)

st.write('---')



# Display total refunds overall
total_refunds = df['Reason of Refunds'].count()
total_refund_amount = df['Refund Amount'].sum()
st.markdown(
    f"<div style='text-align: center; font-size: 1.5em;'>Total Refunds Across All Brands: <span style='color: limegreen; font-weight: bold;'>{total_refunds}</span></div>",
    unsafe_allow_html=True
)
st.markdown(
    f"<div style='text-align: center; font-size: 1.5em;'>Total Refund Amount: <span style='color: limegreen; font-weight: bold;'>${total_refund_amount:,.2f}</span></div>",
    unsafe_allow_html=True
)

st.write('---')
refund_amount_by_brand_reason = df.groupby(['The Brand name', 'Reason of Refunds'])['Refund Amount'].sum().reset_index()

refund_amount_by_brand_reason_fig = px.bar(
    refund_amount_by_brand_reason,
    x='The Brand name',
    y='Refund Amount',
    color='Reason of Refunds',
    title="Refund Amounts by Brand and Reason",
    barmode='stack'  # or 'group' if you prefer side-by-side bars
)
st.plotly_chart(refund_amount_by_brand_reason_fig)
st.write('---')

st.subheader("Refund Reasons Analysis: Count and Percentage Breakdown")

# Create expanders for each brand
unique_brands = refund_counts['The Brand name'].unique()

for brand in unique_brands:
    with st.expander(f"Refund Data for {brand}"):

        # Filter the data for the current brand
        brand_data = refund_counts[refund_counts['The Brand name'] == brand]

        # Display metrics for the current brand
        total_count = brand_data['TotalRefundCount'].iloc[0]
        total_amount = brand_data['TotalRefundAmount'].iloc[0]

        st.write(
            f"<div style='text-align: center; font-size: 1.5em;'>Total Refunds for {brand}: <span style='color: limegreen; font-weight: bold;'>{total_count}</span></div>",
            unsafe_allow_html=True
        )

        st.write(
            f"<div style='text-align: center; font-size: 1.5em;'>Total Refund Amount : <span style='color: limegreen; font-weight: bold;'>{total_amount}</span></div>",
            unsafe_allow_html=True
        )



        # Create a bar chart for the refund reasons for the current brand
        bar_fig = px.bar(
            brand_data,
            x='Reason of Refunds',
            y='Refund Count',
            title=f"Refund Reasons for {brand}",
            text='Text',  # Display count and percentage
            color='Reason of Refunds'
        )
        bar_fig.update_traces(texttemplate='%{text}', textposition='outside')
        bar_fig.update_layout(
            yaxis_title="Refund Count",
            xaxis_title="Refund Reason",
            title_font_size=16,
            showlegend=False
        )
        st.plotly_chart(bar_fig)

st.write('---')


df_clean = df.dropna(subset=['Timestamp', 'Refund Amount', 'The Brand name'])
# Streamlit app title and description

# Use the centered title
st.markdown("<h1 class='center-title'>Refunds Analysis Over Time</h1>", unsafe_allow_html=True)
st.write('---')



refund_by_order_type = df.groupby(['The Brand name', 'Order type']).size().reset_index(name='Refund Count')

# Top refund reasons by brand (for heatmap)
heatmap_data = df.groupby(['The Brand name', 'Reason of Refunds']).size().reset_index(name='Count')

# Cumulative refund trend over time
cumulative_refund_trend = df.groupby('Timestamp')['Refund Amount'].sum().cumsum().reset_index()

# Proportion of refund amounts
refund_amounts_by_brand = df.groupby('The Brand name')['Refund Amount'].sum().reset_index()

trend_fig = px.line(
    cumulative_refund_trend,
    x='Timestamp',
    y='Refund Amount',
    title="Cumulative Refund Amount Over Time",
    markers=True
)
trend_fig.update_traces(line=dict(width=3))
st.plotly_chart(trend_fig)


# Row 1: Column for the total refund per day across all brands
col1 = st.columns(1)  # Single column for total refund across all brands

with col1[0]:
    # Group by date to calculate Total Refund Per Day across all brands
    df_clean['Date'] = df_clean['Timestamp'].dt.date
    df_daily_refund_all = df_clean.groupby('Date')['Refund Amount'].sum().reset_index()

    # Calculate delta for Total Refund Per Day across all brands
    df_daily_refund_all['Delta'] = df_daily_refund_all['Refund Amount'].diff().fillna(0)

    # Create the line chart for Total Refund Per Day across all brands
    fig_total_refund_per_day_all = px.line(df_daily_refund_all,
                                           x='Date',
                                           y='Refund Amount',
                                           title='Total Refund Per Day (All Brands)',
                                           labels={'Date': 'Date', 'Refund Amount': 'Total Refund Amount'},
                                           markers=True,
                                           template='plotly_dark')

    # Add annotations for delta values with enhanced colors
    for i in range(1, len(df_daily_refund_all)):
        delta_value = df_daily_refund_all['Delta'].iloc[i]

        # Determine the color for the delta annotation (green for positive, red for negative)
        delta_color = 'limegreen' if delta_value > 0 else 'red'

        # Adding the delta as annotations (displayed as text on the chart)
        fig_total_refund_per_day_all.add_annotation(
            x=df_daily_refund_all['Date'].iloc[i],
            y=df_daily_refund_all['Refund Amount'].iloc[i],
            text=f"Δ {delta_value:.2f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            ax=0,
            ay=-40,
            font=dict(size=16, color=delta_color),  # Change color based on delta value
            bgcolor="black",
        )

    st.plotly_chart(fig_total_refund_per_day_all, use_container_width=True)

# Row 2: Column for the selected brand's total refund per day and reason-specific charts
st.write("### 📈 Total Refund Per Day (Selected Brand) and Refunds Per Reason")

col2, col3 = st.columns([3, 2])  # Wider column for the selected brand chart, second for reason-specific charts

with col2:
    # Brand filter
    brand_filter = st.selectbox("Select a Brand", df_clean['The Brand name'].unique())

    # Filter data by selected brand
    df_filtered = df_clean[df_clean['The Brand name'] == brand_filter]

    # Group by date to calculate Total Refund Per Day for the selected brand
    df_filtered['Date'] = df_filtered['Timestamp'].dt.date
    df_daily_refund = df_filtered.groupby('Date')['Refund Amount'].sum().reset_index()

    # Calculate delta for Total Refund Per Day
    df_daily_refund['Delta'] = df_daily_refund['Refund Amount'].diff().fillna(0)

    # Create the line chart for Total Refund Per Day (for selected brand)
    fig_total_refund_per_day_brand = px.line(df_daily_refund,
                                             x='Date',
                                             y='Refund Amount',
                                             title=f'Total Refund Per Day for {brand_filter}',
                                             labels={'Date': 'Date', 'Refund Amount': 'Total Refund Amount'},
                                             markers=True,
                                             template='plotly_dark')

    # Add annotations for delta values with enhanced colors
    for i in range(1, len(df_daily_refund)):
        delta_value = df_daily_refund['Delta'].iloc[i]

        # Determine the color for the delta annotation (green for positive, red for negative)
        delta_color = 'limegreen' if delta_value > 0 else 'red'

        # Adding the delta as annotations (displayed as text on the chart)
        fig_total_refund_per_day_brand.add_annotation(
            x=df_daily_refund['Date'].iloc[i],
            y=df_daily_refund['Refund Amount'].iloc[i],
            text=f"Δ {delta_value:.2f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            ax=0,
            ay=-40,
            font=dict(size=16, color=delta_color),  # Change color based on delta value
            bgcolor="black",
        )

    st.plotly_chart(fig_total_refund_per_day_brand, use_container_width=True)

with col3:
    # Filter data by selected brand for reason-specific analysis
    df_filtered_reasons = df_clean[df_clean['The Brand name'] == brand_filter]

    # Group by date and reason to calculate the total refund per reason for the selected brand
    df_filtered_reasons['Date'] = df_filtered_reasons['Timestamp'].dt.date
    df_reason_refund = df_filtered_reasons.groupby(['Date', 'Reason of Refunds'])['Refund Amount'].sum().reset_index()
    # Get all unique refund reasons
    reasons = df_filtered_reasons['Reason of Refunds'].unique()

    # Create a separate line chart for each reason inside an expander
    for reason in reasons:
        with st.expander(f"Total Refund Per Day for Reason: {reason}"):
            # Filter data for the current reason
            df_reason_specific = df_reason_refund[df_reason_refund['Reason of Refunds'] == reason]

            # Calculate delta for Total Refund Per Day by reason
            df_reason_specific['Delta'] = df_reason_specific['Refund Amount'].diff().fillna(0)

            # Create the line chart for the specific refund reason
            fig_reason_refund_per_day = px.line(df_reason_specific,
                                                x='Date',
                                                y='Refund Amount',
                                                title=f'Total Refund Per Day for Reason: {reason} ({brand_filter})',
                                                labels={'Date': 'Date', 'Refund Amount': 'Total Refund Amount'},
                                                markers=True,
                                                template='plotly_dark')

            # Add annotations for delta values with enhanced colors
            for i in range(1, len(df_reason_specific)):
                delta_value = df_reason_specific['Delta'].iloc[i]

                # Determine the color for the delta annotation (green for positive, red for negative)
                delta_color = 'limegreen' if delta_value > 0 else 'red'

                # Adding the delta as annotations (displayed as text on the chart)
                fig_reason_refund_per_day.add_annotation(
                    x=df_reason_specific['Date'].iloc[i],
                    y=df_reason_specific['Refund Amount'].iloc[i],
                    text=f"Δ {delta_value:.2f}",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    ax=0,
                    ay=-40,
                    font=dict(size=16, color=delta_color),  # Change color based on delta value
                    bgcolor="black",
                )

            st.plotly_chart(fig_reason_refund_per_day, use_container_width=True)



# Display the raw data for both charts in one row with 3 columns (no checkbox)
col1, col2, col3 = st.columns(3)  # Create 3 columns for raw data display


with col1:
    with st.expander("Total Refund Per Day (All Brands)"):
        st.write(df_daily_refund_all)

with col2:
    with st.expander("Total Refund Per Day (Selected Brand)"):
        st.write(df_daily_refund)

with col3:
    with st.expander("Total Refund Per Day by Reason (Selected Brand)"):
        st.write(df_reason_refund)

st.write('---')


order_type_fig = px.bar(
    refund_by_order_type,
    x='The Brand name',
    y='Refund Count',
    color='Order type',
    title="Refund Rate by Order Type",
    barmode='group'
)
st.plotly_chart(order_type_fig)

