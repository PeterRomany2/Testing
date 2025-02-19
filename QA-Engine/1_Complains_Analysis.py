# import streamlit as st
# import pandas as pd
# import time
# import plotly.express as px
# from woocommerce import API

# # WooCommerce API Credentials
# wcapi = API(
#     url="https://kayanek.com/", # Your store URL
#     consumer_key="ck_f12a7dbc4bee7f93a396c12fa2c94492d6ea684b", # Your consumer key
#     consumer_secret="cs_487b009cc33c5d91a90753ac16ab4860168ff3a5", # Your consumer secret
#     wp_api=True, # Enable the WP REST API integration
#     version="wc/v3",
#     timeout=30  # Set timeout globally here

# )

# EXCEL_FILE = "orders_data.xlsx"

# # Streamlit UI
# st.title("WooCommerce Live Dashboard 📊")

# # Creating a placeholder for real-time updates
# placeholder = st.empty()


# # Function to fetch new orders
# def fetch_new_orders(start_page):
#     page = start_page
#     all_data = []

#     while True:
#         try:
#             response = wcapi.get("orders",
#                                  params={"per_page": 100, "page": page, "orderby": "date", "order": "asc"}).json()
#             if not response:
#                 break  # Stop if no more data

#             all_data.extend(response)
#             print(f"Fetched page {page} with {len(response)} orders.")

#             if len(response) < 100:
#                 break  # Stop if less than 100 orders

#             page += 1
#         except TimeoutError:
#             print(f"Timeout! Retrying page {page}...")
#             time.sleep(5)
#             continue

#     return pd.DataFrame(all_data)


# # Function to append new orders to Excel
# def append_to_excel(new_data_df, existing_df):
#     last_200_existing_order_ids = set(existing_df.tail(102)['id']) if not existing_df.empty else set()
#     new_data_df = new_data_df[~new_data_df['id'].isin(last_200_existing_order_ids)]

#     if not new_data_df.empty:
#         with pd.ExcelWriter(EXCEL_FILE, mode='a', if_sheet_exists='overlay') as writer:
#             new_data_df.to_excel(writer, index=False, header=False, startrow=existing_df.shape[0] + 1)
#         print(f"Added {len(new_data_df)} new orders.")


# # Real-time loop for checking new orders and updating Streamlit
# while True:
#     print("Checking for new orders...")

#     try:
#         existing_df = pd.read_excel(EXCEL_FILE)  # Reload data
#     except FileNotFoundError:
#         existing_df = pd.DataFrame()

#     new_data_df = fetch_new_orders(620)  # Fetch from last known page

#     if not new_data_df.empty:
#         append_to_excel(new_data_df, existing_df)

#     # Merge new and existing data
#     df = pd.concat([existing_df, new_data_df], ignore_index=True)

#     # Ensure the date column is in datetime format
#     df['date_created'] = pd.to_datetime(df['date_created'], errors='coerce')

#     # Calculate KPIs
#     total_orders = len(df)
#     new_orders_today = df[df['date_created'].dt.date == pd.Timestamp.today().date()].shape[0]
#     total_revenue = df['total'].astype(float).sum()

#     # Orders over time chart
#     orders_over_time = df.groupby(df['date_created'].dt.date).size().reset_index(name='count')
#     orders_chart = px.line(orders_over_time, x='date_created', y='count', title="Orders Over Time")

#     # Revenue by Month chart
#     df['month'] = df['date_created'].dt.to_period('M').astype(str)
#     revenue_by_month = df.groupby('month')['total'].sum().reset_index()
#     revenue_chart = px.bar(revenue_by_month, x='month', y='total', title="Revenue by Month")

#     # Update Streamlit UI dynamically
#     with placeholder.container():
#         st.subheader("📌 KPIs")
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Total Orders", total_orders)
#         col2.metric("New Orders Today", new_orders_today)
#         col3.metric("Total Revenue", f"${total_revenue:,.2f}")

#         st.subheader("📈 Charts")
#         st.plotly_chart(orders_chart, use_container_width=True)
#         st.plotly_chart(revenue_chart, use_container_width=True)

#     time.sleep(10)  # Refresh every 10 seconds
