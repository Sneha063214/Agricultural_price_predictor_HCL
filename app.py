# import streamlit as st
# import pandas as pd


# # ============================================================
# # PAGE CONFIGURATION
# # ============================================================

# st.set_page_config(
#     page_title="Agricultural Market Price Analyzer",
#     page_icon="🌾",
#     layout="wide"
# )


# # ============================================================
# # TITLE
# # ============================================================

# st.title("🌾 Agricultural Market Price Analyzer")

# st.write(
#     "Analyze historical agricultural prices, weather patterns "
#     "and future price forecasts."
# )


# # ============================================================
# # LOAD DATA
# # ============================================================

# @st.cache_data
# def load_data():

#     features_df = pd.read_csv(
#         "agricultural_market_final_features.csv"
#     )

#     forecast_7d_df = pd.read_csv(
#         "forecast_7d_all.csv"
#     )

#     forecast_14d_df = pd.read_csv(
#         "forecast_14d_all.csv"
#     )

#     forecast_30d_df = pd.read_csv(
#         "forecast_30d_all.csv"
#     )

#     return (
#         features_df,
#         forecast_7d_df,
#         forecast_14d_df,
#         forecast_30d_df
#     )


# features_df, forecast_7d_df, forecast_14d_df, forecast_30d_df = load_data()


# # ============================================================
# # DATE CONVERSION
# # ============================================================

# features_df["Week"] = pd.to_datetime(
#     features_df["Week"],
#     errors="coerce"
# )


# # ============================================================
# # MARKET & COMMODITY SELECTION
# # ============================================================

# st.header("📍 Market & Commodity Selection")

# col1, col2, col3 = st.columns(3)


# # -------------------------
# # STATE
# # -------------------------

# with col1:

#     state_options = sorted(
#         features_df["State"]
#         .dropna()
#         .unique()
#     )

#     selected_state = st.selectbox(
#         "Select State",
#         state_options
#     )


# # -------------------------
# # DISTRICT
# # -------------------------

# district_options = sorted(
#     features_df[
#         features_df["State"] == selected_state
#     ]["District"]
#     .dropna()
#     .unique()
# )

# with col2:

#     selected_district = st.selectbox(
#         "Select District",
#         district_options
#     )


# # -------------------------
# # COMMODITY
# # -------------------------

# commodity_options = sorted(
#     features_df[
#         (features_df["State"] == selected_state) &
#         (features_df["District"] == selected_district)
#     ]["Commodity"]
#     .dropna()
#     .unique()
# )

# with col3:

#     selected_commodity = st.selectbox(
#         "Select Commodity",
#         commodity_options
#     )


# st.info(
#     f"Selected: {selected_state} → "
#     f"{selected_district} → "
#     f"{selected_commodity}"
# )


# # ============================================================
# # FILTER HISTORICAL DATA
# # ============================================================

# selected_data = features_df[
#     (features_df["State"] == selected_state) &
#     (features_df["District"] == selected_district) &
#     (features_df["Commodity"] == selected_commodity)
# ].copy()

# selected_data = selected_data.sort_values("Week")


# # ============================================================
# # HISTORICAL PRICE TREND
# # ============================================================

# st.header("📈 Historical Price Trend")

# if not selected_data.empty:

#     st.line_chart(
#         selected_data.set_index("Week")[
#             "Median_Modal_Price"
#         ]
#     )

# else:

#     st.warning(
#         "No historical price data available."
#     )


# # ============================================================
# # WEATHER ANALYSIS
# # ============================================================

# st.header("🌦️ Weather Analysis")


# if not selected_data.empty:

#     weather_col1, weather_col2, weather_col3 = st.columns(3)


#     # -------------------------
#     # TEMPERATURE
#     # -------------------------

#     avg_temperature = selected_data[
#         "Mean_Temperature"
#     ].mean()

#     with weather_col1:

#         st.metric(
#             "Average Temperature",
#             f"{avg_temperature:.2f} °C"
#         )


#     # -------------------------
#     # HUMIDITY
#     # -------------------------

#     avg_humidity = selected_data[
#         "Mean_Humidity"
#     ].mean()

#     with weather_col2:

#         st.metric(
#             "Average Humidity",
#             f"{avg_humidity:.2f} %"
#         )


#     # -------------------------
#     # RAINFALL
#     # -------------------------

#     total_rainfall = selected_data[
#         "Total_Rainfall"
#     ].sum()

#     with weather_col3:

#         st.metric(
#             "Total Rainfall",
#             f"{total_rainfall:.2f} mm"
#         )


#     # -------------------------
#     # TEMPERATURE TREND
#     # -------------------------

#     st.subheader("🌡️ Temperature Trend")

#     st.line_chart(
#         selected_data.set_index("Week")[
#             "Mean_Temperature"
#         ]
#     )


#     # -------------------------
#     # HUMIDITY TREND
#     # -------------------------

#     st.subheader("💧 Humidity Trend")

#     st.line_chart(
#         selected_data.set_index("Week")[
#             "Mean_Humidity"
#         ]
#     )


#     # -------------------------
#     # RAINFALL TREND
#     # -------------------------

#     st.subheader("🌧️ Rainfall Trend")

#     st.line_chart(
#         selected_data.set_index("Week")[
#             "Total_Rainfall"
#         ]
#     )


# # ============================================================
# # FUTURE PRICE FORECAST
# # ============================================================

# st.header("🔮 Future Price Forecast")


# # Filter 7-day forecast

# forecast_7_selected = forecast_7d_df[
#     (forecast_7d_df["State"] == selected_state) &
#     (forecast_7d_df["District"] == selected_district) &
#     (forecast_7d_df["Commodity"] == selected_commodity)
# ]


# # Filter 14-day forecast

# forecast_14_selected = forecast_14d_df[
#     (forecast_14d_df["State"] == selected_state) &
#     (forecast_14d_df["District"] == selected_district) &
#     (forecast_14d_df["Commodity"] == selected_commodity)
# ]


# # Filter 30-day forecast

# forecast_30_selected = forecast_30d_df[
#     (forecast_30d_df["State"] == selected_state) &
#     (forecast_30d_df["District"] == selected_district) &
#     (forecast_30d_df["Commodity"] == selected_commodity)
# ]


# forecast_col1, forecast_col2, forecast_col3 = st.columns(3)


# # ============================================================
# # 7-DAY FORECAST
# # ============================================================

# with forecast_col1:

#     st.subheader("📅 7-Day Forecast")

#     if not forecast_7_selected.empty:

#         price_7d = forecast_7_selected.iloc[0][
#             "Forecast_7D"
#         ]

#         st.metric(
#             "Predicted Price",
#             f"₹{price_7d:,.2f} / quintal"
#         )

#         st.caption(
#             f"≈ ₹{price_7d / 100:,.2f} per kg"
#         )

#     else:

#         st.info(
#             "Forecast not available for this selection."
#         )


# # ============================================================
# # 14-DAY FORECAST
# # ============================================================

# with forecast_col2:

#     st.subheader("📅 14-Day Forecast")

#     if not forecast_14_selected.empty:

#         price_14d = forecast_14_selected.iloc[0][
#             "Forecast_14D"
#         ]

#         st.metric(
#             "Predicted Price",
#             f"₹{price_14d:,.2f} / quintal"
#         )

#         st.caption(
#             f"≈ ₹{price_14d / 100:,.2f} per kg"
#         )

#     else:

#         st.info(
#             "Forecast not available for this selection."
#         )


# # ============================================================
# # 30-DAY FORECAST
# # ============================================================

# with forecast_col3:

#     st.subheader("📅 30-Day Forecast")

#     if not forecast_30_selected.empty:

#         price_30d = forecast_30_selected.iloc[0][
#             "Forecast_30D"
#         ]

#         st.metric(
#             "Predicted Price",
#             f"₹{price_30d:,.2f} / quintal"
#         )

#         st.caption(
#             f"≈ ₹{price_30d / 100:,.2f} per kg"
#         )

#     else:

#         st.info(
#             "Forecast not available for this selection."
#         )


# # ============================================================
# # FORECAST COMPARISON
# # ============================================================

# st.header("📊 Forecast Comparison")


# if (
#     not forecast_7_selected.empty
#     and not forecast_14_selected.empty
#     and not forecast_30_selected.empty
# ):

#     comparison_df = pd.DataFrame({
#         "Forecast Horizon": [
#             "7 Days",
#             "14 Days",
#             "30 Days"
#         ],

#         "Predicted Price": [
#             forecast_7_selected.iloc[0]["Forecast_7D"],
#             forecast_14_selected.iloc[0]["Forecast_14D"],
#             forecast_30_selected.iloc[0]["Forecast_30D"]
#         ]
#     })


#     st.bar_chart(
#         comparison_df.set_index(
#             "Forecast Horizon"
#         )
#     )


# # ============================================================
# # MODEL PERFORMANCE
# # ============================================================

# st.header("🤖 Model Performance")


# performance_df = pd.DataFrame({
#     "Forecast Horizon": [
#         "7 Days",
#         "14 Days",
#         "30 Days"
#     ],

#     "MAE": [
#         297.649862,
#         374.776872,
#         537.523449
#     ],

#     "RMSE": [
#         1579.480756,
#         1586.331959,
#         990.548881
#     ],

#     "MAPE (%)": [
#         18.455095,
#         25.272335,
#         38.426064
#     ]
# })


# st.dataframe(
#     performance_df,
#     use_container_width=True,
#     hide_index=True
# )


# # ============================================================
# # FOOTER
# # ============================================================

# st.markdown("---")

# st.caption(
#     "Agricultural Market Price Analyzer | "
#     "Historical price analysis, weather correlation "
#     "and ML-based price forecasting"
# )

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# # ============================================================
# # PAGE CONFIGURATION
# # ============================================================

# st.set_page_config(
#     page_title="Agricultural Market Price Analyzer",
#     page_icon="🌾",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )


# # ============================================================
# # CUSTOM CSS
# # ============================================================

# st.markdown("""
# <style>

#     .main {
#         background-color: #f7f9fc;
#     }

#     .block-container {
#         padding-top: 2rem;
#         padding-bottom: 3rem;
#     }

#     .hero {
#         padding: 28px;
#         border-radius: 18px;
#         background: linear-gradient(135deg, #1b5e20, #43a047);
#         color: white;
#         margin-bottom: 25px;
#     }

#     .hero h1 {
#         font-size: 38px;
#         margin-bottom: 8px;
#     }

#     .hero p {
#         font-size: 17px;
#         margin-bottom: 0;
#     }

#     .section-title {
#         font-size: 27px;
#         font-weight: 700;
#         margin-top: 25px;
#         margin-bottom: 15px;
#     }

#     .insight-box {
#         padding: 16px 20px;
#         border-radius: 12px;
#         background-color: #eef7ee;
#         border-left: 5px solid #2e7d32;
#         margin-top: 8px;
#         margin-bottom: 20px;
#         font-size: 15px;
#     }

#     .info-box {
#         padding: 16px 20px;
#         border-radius: 12px;
#         background-color: #eef4ff;
#         border-left: 5px solid #1565c0;
#         margin-top: 8px;
#         margin-bottom: 20px;
#     }

#     div[data-testid="stMetric"] {
#         background-color: white;
#         padding: 15px;
#         border-radius: 12px;
#         box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
#     }

# </style>
# """, unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

# st.markdown("""
# <div class="hero">

# <h1>🌾 Agricultural Market Price Analyzer</h1>

# <p>
# Explore agricultural commodity prices, seasonal patterns,
# weather relationships and machine-learning based price forecasts.
# </p>

# </div>
# """, unsafe_allow_html=True)


# # ============================================================
# # LOAD DATA
# # ============================================================

# @st.cache_data
# def load_data():

#     features_df = pd.read_csv(
#         "agricultural_market_final_features.csv"
#     )

#     organized_price_df = pd.read_csv(
#         "organized_price_data.csv"
#     )

#     forecast_7d_df = pd.read_csv(
#         "forecast_7d_all.csv"
#     )

#     forecast_14d_df = pd.read_csv(
#         "forecast_14d_all.csv"
#     )

#     forecast_30d_df = pd.read_csv(
#         "forecast_30d_all.csv"
#     )

#     return (
#         features_df,
#         organized_price_df,
#         forecast_7d_df,
#         forecast_14d_df,
#         forecast_30d_df
#     )


# (
#     features_df,
#     organized_price_df,
#     forecast_7d_df,
#     forecast_14d_df,
#     forecast_30d_df
# ) = load_data()


# # ============================================================
# # DATA PREPARATION
# # ============================================================

# features_df["Week"] = pd.to_datetime(
#     features_df["Week"],
#     errors="coerce"
# )

# organized_price_df["Date"] = pd.to_datetime(
#     organized_price_df["Date"],
#     errors="coerce"
# )

# organized_price_df["Modal_Price"] = pd.to_numeric(
#     organized_price_df["Modal_Price"],
#     errors="coerce"
# )


# # State name standardization used during EDA

# state_mapping = {
#     "Tamilnadu": "Tamil Nadu",
#     "Chattisgarh": "Chhattisgarh",
#     "Jammu & Kashmir": "Jammu and Kashmir",
#     "Gao": "Goa",
#     "Uttrakhand": "Uttarakhand"
# }

# features_df["State"] = features_df["State"].replace(
#     state_mapping
# )

# organized_price_df["State"] = organized_price_df["State"].replace(
#     state_mapping
# )


# # ============================================================
# # SIDEBAR
# # ============================================================

# st.sidebar.title("🌾 Dashboard Controls")

# st.sidebar.markdown(
#     "Use the filters below to explore a specific "
#     "state, district and commodity."
# )


# # ============================================================
# # MARKET & COMMODITY SELECTION
# # ============================================================

# st.markdown(
#     '<div class="section-title">📍 Market & Commodity Selection</div>',
#     unsafe_allow_html=True
# )

# col1, col2, col3 = st.columns(3)


# # -------------------------
# # STATE
# # -------------------------

# state_options = sorted(
#     features_df["State"]
#     .dropna()
#     .unique()
# )

# with col1:

#     selected_state = st.selectbox(
#         "Select State",
#         state_options
#     )


# # -------------------------
# # DISTRICT
# # -------------------------

# district_options = sorted(
#     features_df[
#         features_df["State"] == selected_state
#     ]["District"]
#     .dropna()
#     .unique()
# )

# with col2:

#     selected_district = st.selectbox(
#         "Select District",
#         district_options
#     )


# # -------------------------
# # COMMODITY
# # -------------------------

# commodity_options = sorted(
#     features_df[
#         (features_df["State"] == selected_state) &
#         (features_df["District"] == selected_district)
#     ]["Commodity"]
#     .dropna()
#     .unique()
# )

# with col3:

#     selected_commodity = st.selectbox(
#         "Select Commodity",
#         commodity_options
#     )


# st.markdown(
#     f"""
#     <div class="info-box">
#     <b>Selected:</b>
#     {selected_state} → {selected_district} → {selected_commodity}
#     </div>
#     """,
#     unsafe_allow_html=True
# )


# # ============================================================
# # FILTER SELECTED SERIES
# # ============================================================

# selected_data = features_df[
#     (features_df["State"] == selected_state) &
#     (features_df["District"] == selected_district) &
#     (features_df["Commodity"] == selected_commodity)
# ].copy()

# selected_data = selected_data.sort_values("Week")


# # ============================================================
# # OVERVIEW METRICS
# # ============================================================

# st.markdown(
#     '<div class="section-title">📊 Selected Series Overview</div>',
#     unsafe_allow_html=True
# )

# if not selected_data.empty:

#     avg_price = selected_data[
#         "Median_Modal_Price"
#     ].mean()

#     min_price = selected_data[
#         "Median_Modal_Price"
#     ].min()

#     max_price = selected_data[
#         "Median_Modal_Price"
#     ].max()

#     price_std = selected_data[
#         "Median_Modal_Price"
#     ].std()

#     c1, c2, c3, c4 = st.columns(4)

#     with c1:
#         st.metric(
#             "Average Price",
#             f"₹{avg_price:,.2f}"
#         )

#     with c2:
#         st.metric(
#             "Minimum Price",
#             f"₹{min_price:,.2f}"
#         )

#     with c3:
#         st.metric(
#             "Maximum Price",
#             f"₹{max_price:,.2f}"
#         )

#     with c4:
#         st.metric(
#             "Price Std. Dev.",
#             f"₹{price_std:,.2f}"
#         )


# # ============================================================
# # TABS
# # ============================================================

# tab1, tab2, tab3, tab4, tab5 = st.tabs(
#     [
#         "📈 Price Analysis",
#         "🌦️ Weather Analysis",
#         "🔗 Weather Relationships",
#         "🔮 Forecasts",
#         "🤖 Model Performance"
#     ]
# )


# # ============================================================
# # TAB 1 — PRICE ANALYSIS
# # ============================================================

# with tab1:

#     # --------------------------------------------------------
#     # HISTORICAL PRICE TREND
#     # --------------------------------------------------------

#     st.markdown(
#         '<div class="section-title">📈 Historical Price Trend</div>',
#         unsafe_allow_html=True
#     )

#     if not selected_data.empty:

#         fig = px.line(
#             selected_data,
#             x="Week",
#             y="Median_Modal_Price",
#             markers=True,
#             title=(
#                 f"{selected_commodity} Price Trend — "
#                 f"{selected_district}"
#             ),
#             labels={
#                 "Week": "Week",
#                 "Median_Modal_Price": "Median Modal Price (₹/quintal)"
#             }
#         )

#         fig.update_layout(
#             hovermode="x unified",
#             height=450
#         )

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#         first_price = selected_data.iloc[0][
#             "Median_Modal_Price"
#         ]

#         last_price = selected_data.iloc[-1][
#             "Median_Modal_Price"
#         ]

#         if last_price > first_price:

#             direction = "increased"

#         elif last_price < first_price:

#             direction = "decreased"

#         else:

#             direction = "remained broadly stable"

#         st.markdown(
#             f"""
#             <div class="insight-box">
#             <b>💡 Inference:</b>
#             The historical median modal price has {direction}
#             over the available period for
#             <b>{selected_commodity}</b> in
#             <b>{selected_district}</b>.
#             The graph shows the actual weekly movement of the commodity price.
#             </div>
#             """,
#             unsafe_allow_html=True
#         )


#     # --------------------------------------------------------
#     # MONTHLY PRICE PATTERN
#     # --------------------------------------------------------

#     st.markdown(
#         '<div class="section-title">📅 Monthly Price Pattern</div>',
#         unsafe_allow_html=True
#     )

#     monthly_df = features_df.copy()

#     monthly_df["Month_Name"] = (
#         monthly_df["Week"]
#         .dt.month_name()
#     )

#     monthly_order = [
#         "January",
#         "February",
#         "March",
#         "April",
#         "May",
#         "June",
#         "July",
#         "August",
#         "September",
#         "October",
#         "November",
#         "December"
#     ]

#     monthly_pattern = (
#         monthly_df
#         .groupby(
#             ["Month", "Month_Name"],
#             as_index=False
#         )["Median_Modal_Price"]
#         .median()
#         .sort_values("Month")
#     )

#     fig = px.line(
#         monthly_pattern,
#         x="Month_Name",
#         y="Median_Modal_Price",
#         markers=True,
#         category_orders={
#             "Month_Name": monthly_order
#         },
#         title="Overall Monthly Median Modal Price",
#         labels={
#             "Month_Name": "Month",
#             "Median_Modal_Price": "Median Price (₹/quintal)"
#         }
#     )

#     fig.update_layout(height=430)

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     highest_month = monthly_pattern.loc[
#         monthly_pattern["Median_Modal_Price"].idxmax(),
#         "Month_Name"
#     ]

#     lowest_month = monthly_pattern.loc[
#         monthly_pattern["Median_Modal_Price"].idxmin(),
#         "Month_Name"
#     ]

#     st.markdown(
#         f"""
#         <div class="insight-box">
#         <b>💡 Inference:</b>
#         The monthly pattern indicates that agricultural prices
#         vary across the year. In the analyzed dataset,
#         <b>{highest_month}</b> has the highest median price,
#         while <b>{lowest_month}</b> has the lowest median price.
#         This indicates the presence of seasonal price variation.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


#     # --------------------------------------------------------
#     # WEEKLY PRICE PATTERN
#     # --------------------------------------------------------

#     st.markdown(
#         '<div class="section-title">🗓️ Weekly Seasonal Pattern</div>',
#         unsafe_allow_html=True
#     )

#     weekly_pattern = (
#         features_df
#         .assign(
#             Week_Number=features_df["Week"].dt.isocalendar().week.astype(int)
#         )
#         .groupby("Week_Number", as_index=False)
#         ["Median_Modal_Price"]
#         .median()
#     )

#     fig = px.line(
#         weekly_pattern,
#         x="Week_Number",
#         y="Median_Modal_Price",
#         markers=True,
#         title="Median Price by Week of Year",
#         labels={
#             "Week_Number": "Week Number",
#             "Median_Modal_Price": "Median Price (₹/quintal)"
#         }
#     )

#     fig.update_layout(height=430)

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     st.markdown(
#         """
#         <div class="insight-box">
#         <b>💡 Inference:</b>
#         Prices do not remain constant throughout the year.
#         The weekly pattern shows periods of relatively lower
#         and higher prices, indicating recurring seasonal behavior
#         in the agricultural market.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


#     # --------------------------------------------------------
#     # SEASONAL PATTERN
#     # --------------------------------------------------------

#     st.markdown(
#         '<div class="section-title">🌱 Seasonal Price Pattern</div>',
#         unsafe_allow_html=True
#     )

#     season_order = [
#         "Winter",
#         "Summer",
#         "Monsoon",
#         "Post-Monsoon"
#     ]

#     seasonal_df = (
#         features_df
#         .groupby("Season", as_index=False)
#         ["Median_Modal_Price"]
#         .median()
#     )

#     seasonal_df["Season"] = pd.Categorical(
#         seasonal_df["Season"],
#         categories=season_order,
#         ordered=True
#     )

#     seasonal_df = seasonal_df.sort_values("Season")

#     fig = px.bar(
#         seasonal_df,
#         x="Season",
#         y="Median_Modal_Price",
#         title="Median Price Across Seasons",
#         labels={
#             "Median_Modal_Price": "Median Price (₹/quintal)"
#         },
#         text_auto=".0f"
#     )

#     fig.update_layout(height=400)

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     highest_season = seasonal_df.loc[
#         seasonal_df["Median_Modal_Price"].idxmax(),
#         "Season"
#     ]

#     lowest_season = seasonal_df.loc[
#         seasonal_df["Median_Modal_Price"].idxmin(),
#         "Season"
#     ]

#     st.markdown(
#         f"""
#         <div class="insight-box">
#         <b>💡 Inference:</b>
#         Among the defined seasons, <b>{highest_season}</b>
#         has the highest overall median price and
#         <b>{lowest_season}</b> has the lowest.
#         This suggests that seasonal conditions are associated
#         with changes in market prices.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


#     # --------------------------------------------------------
#     # STATE COMPARISON
#     # --------------------------------------------------------

#     st.markdown(
#         '<div class="section-title">🗺️ State-wise Price Comparison</div>',
#         unsafe_allow_html=True
#     )

#     state_comparison = (
#         features_df
#         .groupby("State", as_index=False)
#         ["Median_Modal_Price"]
#         .median()
#         .sort_values(
#             "Median_Modal_Price",
#             ascending=False
#         )
#     )

#     fig = px.bar(
#         state_comparison,
#         x="State",
#         y="Median_Modal_Price",
#         title="Median Modal Price by State",
#         labels={
#             "Median_Modal_Price": "Median Price (₹/quintal)"
#         }
#     )

#     fig.update_layout(
#         height=500,
#         xaxis_tickangle=-45
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     st.markdown(
#         """
#         <div class="insight-box">
#         <b>💡 Inference:</b>
#         Median commodity prices differ considerably across states.
#         This reflects geographical differences in agricultural
#         production, markets, supply conditions and commodity mix.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


#     # --------------------------------------------------------
#     # COMMODITY COMPARISON
#     # --------------------------------------------------------

#     st.markdown(
#         '<div class="section-title">🥕 Commodity-wise Price Comparison</div>',
#         unsafe_allow_html=True
#     )

#     commodity_comparison = (
#         features_df
#         .groupby("Commodity", as_index=False)
#         ["Median_Modal_Price"]
#         .median()
#         .sort_values(
#             "Median_Modal_Price",
#             ascending=False
#         )
#     )

#     fig = px.bar(
#         commodity_comparison,
#         x="Commodity",
#         y="Median_Modal_Price",
#         title="Median Price by Commodity",
#         labels={
#             "Median_Modal_Price": "Median Price (₹/quintal)"
#         },
#         text_auto=".0f"
#     )

#     fig.update_layout(height=430)

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     st.markdown(
#         """
#         <div class="insight-box">
#         <b>💡 Inference:</b>
#         Different commodities have substantially different
#         price levels. Therefore, price forecasting needs to
#         preserve the commodity-specific time series rather than
#         mixing all commodities into a single sequence.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


#     # --------------------------------------------------------
#     # MARKET COMPARISON
#     # --------------------------------------------------------

#     st.markdown(
#         '<div class="section-title">🏪 Market-wise Price Comparison</div>',
#         unsafe_allow_html=True
#     )

#     market_comparison = (
#         organized_price_df
#         .groupby(
#             ["State", "District", "Market"],
#             as_index=False
#         )
#         .agg(
#             Median_Modal_Price=(
#                 "Modal_Price",
#                 "median"
#             ),
#             Record_Count=(
#                 "Modal_Price",
#                 "count"
#             )
#         )
#     )

#     market_comparison = market_comparison.dropna(
#         subset=["Median_Modal_Price"]
#     )

#     top_markets = (
#         market_comparison
#         .sort_values(
#             "Median_Modal_Price",
#             ascending=False
#         )
#         .head(15)
#         .copy()
#     )

#     top_markets["Market_Label"] = (
#         top_markets["Market"] +
#         " (" +
#         top_markets["District"] +
#         ")"
#     )

#     fig = px.bar(
#         top_markets.sort_values("Median_Modal_Price"),
#         x="Median_Modal_Price",
#         y="Market_Label",
#         orientation="h",
#         title="Top 15 Markets by Median Modal Price",
#         labels={
#             "Median_Modal_Price": "Median Price (₹/quintal)",
#             "Market_Label": "Market"
#         }
#     )

#     fig.update_layout(height=600)

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     st.markdown(
#         """
#         <div class="insight-box">
#         <b>💡 Inference:</b>
#         Market-level prices show substantial variation.
#         This demonstrates that location at the market/district
#         level can be important when interpreting agricultural
#         commodity prices.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


#     # --------------------------------------------------------
#     # PRICE VOLATILITY
#     # --------------------------------------------------------

#     st.markdown(
#         '<div class="section-title">📦 Price Volatility</div>',
#         unsafe_allow_html=True
#     )

#     volatility_df = features_df[
#         [
#             "Commodity",
#             "Median_Modal_Price"
#         ]
#     ].dropna()

#     fig = px.box(
#         volatility_df,
#         x="Commodity",
#         y="Median_Modal_Price",
#         points=False,
#         title="Price Distribution and Volatility by Commodity",
#         labels={
#             "Median_Modal_Price": "Median Modal Price (₹/quintal)"
#         }
#     )

#     fig.update_layout(height=500)

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     st.markdown(
#         """
#         <div class="insight-box">
#         <b>💡 Inference:</b>
#         The box plot shows the spread and variability of prices
#         for each commodity. A wider distribution indicates greater
#         variation in observed prices across locations and periods.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


# # ============================================================
# # TAB 2 — WEATHER ANALYSIS
# # ============================================================

# with tab2:

#     st.markdown(
#         '<div class="section-title">🌦️ Weather Analysis</div>',
#         unsafe_allow_html=True
#     )

#     if not selected_data.empty:

#         weather_col1, weather_col2, weather_col3 = st.columns(3)

#         avg_temperature = selected_data[
#             "Mean_Temperature"
#         ].mean()

#         avg_humidity = selected_data[
#             "Mean_Humidity"
#         ].mean()

#         total_rainfall = selected_data[
#             "Total_Rainfall"
#         ].sum()

#         with weather_col1:

#             st.metric(
#                 "Average Temperature",
#                 f"{avg_temperature:.2f} °C"
#             )

#         with weather_col2:

#             st.metric(
#                 "Average Humidity",
#                 f"{avg_humidity:.2f} %"
#             )

#         with weather_col3:

#             st.metric(
#                 "Total Rainfall",
#                 f"{total_rainfall:.2f} mm"
#             )


#         # ----------------------------------------------------
#         # TEMPERATURE
#         # ----------------------------------------------------

#         st.subheader("🌡️ Temperature Trend")

#         fig = px.line(
#             selected_data,
#             x="Week",
#             y="Mean_Temperature",
#             markers=True,
#             title="Weekly Mean Temperature"
#         )

#         fig.update_layout(height=400)

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#         st.markdown(
#             """
#             <div class="insight-box">
#             <b>💡 Inference:</b>
#             Temperature varies over time according to seasonal
#             weather conditions. The trend can be compared with
#             the corresponding commodity price movement.
#             </div>
#             """,
#             unsafe_allow_html=True
#         )


#         # ----------------------------------------------------
#         # HUMIDITY
#         # ----------------------------------------------------

#         st.subheader("💧 Humidity Trend")

#         fig = px.line(
#             selected_data,
#             x="Week",
#             y="Mean_Humidity",
#             markers=True,
#             title="Weekly Mean Humidity"
#         )

#         fig.update_layout(height=400)

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#         st.markdown(
#             """
#             <div class="insight-box">
#             <b>💡 Inference:</b>
#             Humidity changes across the agricultural season.
#             Humidity was also one of the weather variables showing
#             a measurable relationship with price in the EDA.
#             </div>
#             """,
#             unsafe_allow_html=True
#         )


#         # ----------------------------------------------------
#         # RAINFALL
#         # ----------------------------------------------------

#         st.subheader("🌧️ Rainfall Trend")

#         fig = px.bar(
#             selected_data,
#             x="Week",
#             y="Total_Rainfall",
#             title="Weekly Total Rainfall"
#         )

#         fig.update_layout(height=400)

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#         st.markdown(
#             """
#             <div class="insight-box">
#             <b>💡 Inference:</b>
#             Rainfall is highly time-dependent and can vary
#             significantly between weeks. This makes rainfall
#             useful as a time-varying external factor for
#             agricultural price analysis.
#             </div>
#             """,
#             unsafe_allow_html=True
#         )


# # ============================================================
# # TAB 3 — WEATHER RELATIONSHIPS
# # ============================================================

# with tab3:

#     st.markdown(
#         '<div class="section-title">🔗 Price–Weather Relationships</div>',
#         unsafe_allow_html=True
#     )

#     # --------------------------------------------------------
#     # CORRELATION VALUES
#     # --------------------------------------------------------

#     corr_cols = [
#         "Median_Modal_Price",
#         "Total_Rainfall",
#         "Mean_Temperature",
#         "Mean_Humidity"
#     ]

#     corr_df = features_df[corr_cols].corr()

#     price_rainfall_corr = corr_df.loc[
#         "Median_Modal_Price",
#         "Total_Rainfall"
#     ]

#     price_temperature_corr = corr_df.loc[
#         "Median_Modal_Price",
#         "Mean_Temperature"
#     ]

#     price_humidity_corr = corr_df.loc[
#         "Median_Modal_Price",
#         "Mean_Humidity"
#     ]

#     c1, c2, c3 = st.columns(3)

#     with c1:

#         st.metric(
#             "Price ↔ Rainfall",
#             f"{price_rainfall_corr:.3f}"
#         )

#     with c2:

#         st.metric(
#             "Price ↔ Temperature",
#             f"{price_temperature_corr:.3f}"
#         )

#     with c3:

#         st.metric(
#             "Price ↔ Humidity",
#             f"{price_humidity_corr:.3f}"
#         )


#     # --------------------------------------------------------
#     # PRICE VS RAINFALL
#     # --------------------------------------------------------

#     st.subheader("🌧️ Price vs Rainfall")

#     fig = px.scatter(
#         features_df,
#         x="Total_Rainfall",
#         y="Median_Modal_Price",
#         opacity=0.45,
#         trendline="ols",
#         title="Commodity Price vs Total Rainfall",
#         labels={
#             "Total_Rainfall": "Total Rainfall (mm)",
#             "Median_Modal_Price": "Median Price (₹/quintal)"
#         }
#     )

#     fig.update_layout(height=450)

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     st.markdown(
#         f"""
#         <div class="insight-box">
#         <b>💡 Inference:</b>
#         The correlation between price and rainfall in the analyzed
#         dataset is <b>{price_rainfall_corr:.3f}</b>.
#         This indicates a positive association, although correlation
#         alone does not establish causation.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


#     # --------------------------------------------------------
#     # PRICE VS TEMPERATURE
#     # --------------------------------------------------------

#     st.subheader("🌡️ Price vs Temperature")

#     fig = px.scatter(
#         features_df,
#         x="Mean_Temperature",
#         y="Median_Modal_Price",
#         opacity=0.45,
#         trendline="ols",
#         title="Commodity Price vs Mean Temperature",
#         labels={
#             "Mean_Temperature": "Mean Temperature (°C)",
#             "Median_Modal_Price": "Median Price (₹/quintal)"
#         }
#     )

#     fig.update_layout(height=450)

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     st.markdown(
#         f"""
#         <div class="insight-box">
#         <b>💡 Inference:</b>
#         The correlation between price and temperature is
#         <b>{price_temperature_corr:.3f}</b>.
#         This is close to zero in the overall dataset, indicating
#         little linear association between these two variables
#         at the aggregated level.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


#     # --------------------------------------------------------
#     # PRICE VS HUMIDITY
#     # --------------------------------------------------------

#     st.subheader("💧 Price vs Humidity")

#     fig = px.scatter(
#         features_df,
#         x="Mean_Humidity",
#         y="Median_Modal_Price",
#         opacity=0.45,
#         trendline="ols",
#         title="Commodity Price vs Mean Humidity",
#         labels={
#             "Mean_Humidity": "Mean Humidity (%)",
#             "Median_Modal_Price": "Median Price (₹/quintal)"
#         }
#     )

#     fig.update_layout(height=450)

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     st.markdown(
#         f"""
#         <div class="insight-box">
#         <b>💡 Inference:</b>
#         The price-humidity correlation is
#         <b>{price_humidity_corr:.3f}</b>.
#         This represents a positive linear association in the
#         analyzed dataset. Humidity therefore provides useful
#         information for the forecasting feature set.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


#     # --------------------------------------------------------
#     # CORRELATION HEATMAP
#     # --------------------------------------------------------

#     st.subheader("🔥 Weather Correlation Matrix")

#     heatmap_data = features_df[
#         [
#             "Median_Modal_Price",
#             "Total_Rainfall",
#             "Mean_Temperature",
#             "Mean_Humidity"
#         ]
#     ].corr()

#     fig = px.imshow(
#         heatmap_data,
#         text_auto=".3f",
#         aspect="auto",
#         title="Correlation Matrix"
#     )

#     fig.update_layout(height=500)

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     st.markdown(
#         """
#         <div class="insight-box">
#         <b>💡 Inference:</b>
#         The correlation matrix summarizes the linear relationships
#         among price and the three weather variables. It also shows
#         that rainfall and humidity themselves have a relationship,
#         so weather variables should be considered together rather
#         than interpreted independently.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


#     # --------------------------------------------------------
#     # WEATHER LAG ANALYSIS
#     # --------------------------------------------------------

#     st.subheader("⏮️ Weather Lag Analysis")

#     lag_correlations = {}

#     lag_columns = [
#         "Rainfall_Lag_1",
#         "Rainfall_Lag_2",
#         "Temperature_Lag_1",
#         "Temperature_Lag_2",
#         "Humidity_Lag_1",
#         "Humidity_Lag_2"
#     ]

#     for col in lag_columns:

#         if col in features_df.columns:

#             lag_correlations[col] = (
#                 features_df[
#                     [
#                         "Median_Modal_Price",
#                         col
#                     ]
#                 ]
#                 .corr()
#                 .iloc[0, 1]
#             )

#     lag_df = pd.DataFrame(
#         list(lag_correlations.items()),
#         columns=[
#             "Weather Feature",
#             "Correlation"
#         ]
#     )

#     lag_df = lag_df.sort_values(
#         "Correlation",
#         ascending=False
#     )

#     fig = px.bar(
#         lag_df,
#         x="Weather Feature",
#         y="Correlation",
#         title="Price Correlation with Previous Weather Conditions",
#         labels={
#             "Correlation": "Correlation with Price"
#         },
#         text_auto=".3f"
#     )

#     fig.update_layout(height=450)

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

#     strongest_lag = lag_df.iloc[0]

#     st.markdown(
#         f"""
#         <div class="insight-box">
#         <b>💡 Inference:</b>
#         Among the tested lagged weather variables,
#         <b>{strongest_lag["Weather Feature"]}</b> has the highest
#         observed correlation with price at approximately
#         <b>{strongest_lag["Correlation"]:.3f}</b>.
#         This supports including lagged weather variables as
#         forecasting features.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


# # ============================================================
# # TAB 4 — FORECASTS
# # ============================================================

# with tab4:

#     st.markdown(
#         '<div class="section-title">🔮 Future Price Forecast</div>',
#         unsafe_allow_html=True
#     )

#     forecast_7_selected = forecast_7d_df[
#         (forecast_7d_df["State"] == selected_state) &
#         (forecast_7d_df["District"] == selected_district) &
#         (forecast_7d_df["Commodity"] == selected_commodity)
#     ]

#     forecast_14_selected = forecast_14d_df[
#         (forecast_14d_df["State"] == selected_state) &
#         (forecast_14d_df["District"] == selected_district) &
#         (forecast_14d_df["Commodity"] == selected_commodity)
#     ]

#     forecast_30_selected = forecast_30d_df[
#         (forecast_30d_df["State"] == selected_state) &
#         (forecast_30d_df["District"] == selected_district) &
#         (forecast_30d_df["Commodity"] == selected_commodity)
#     ]


#     forecast_col1, forecast_col2, forecast_col3 = st.columns(3)


#     # --------------------------------------------------------
#     # 7 DAY
#     # --------------------------------------------------------

#     with forecast_col1:

#         st.subheader("📅 7-Day Forecast")

#         if not forecast_7_selected.empty:

#             price_7d = forecast_7_selected.iloc[0][
#                 "Forecast_7D"
#             ]

#             st.metric(
#                 "Predicted Price",
#                 f"₹{price_7d:,.2f} / quintal"
#             )

#             st.caption(
#                 f"≈ ₹{price_7d / 100:,.2f} per kg"
#             )

#         else:

#             st.info(
#                 "Forecast not available."
#             )


#     # --------------------------------------------------------
#     # 14 DAY
#     # --------------------------------------------------------

#     with forecast_col2:

#         st.subheader("📅 14-Day Forecast")

#         if not forecast_14_selected.empty:

#             price_14d = forecast_14_selected.iloc[0][
#                 "Forecast_14D"
#             ]

#             st.metric(
#                 "Predicted Price",
#                 f"₹{price_14d:,.2f} / quintal"
#             )

#             st.caption(
#                 f"≈ ₹{price_14d / 100:,.2f} per kg"
#             )

#         else:

#             st.info(
#                 "Forecast not available."
#             )


#     # --------------------------------------------------------
#     # 30 DAY
#     # --------------------------------------------------------

#     with forecast_col3:

#         st.subheader("📅 30-Day Forecast")

#         if not forecast_30_selected.empty:

#             price_30d = forecast_30_selected.iloc[0][
#                 "Forecast_30D"
#             ]

#             st.metric(
#                 "Predicted Price",
#                 f"₹{price_30d:,.2f} / quintal"
#             )

#             st.caption(
#                 f"≈ ₹{price_30d / 100:,.2f} per kg"
#             )

#         else:

#             st.info(
#                 "Forecast not available."
#             )


#     # --------------------------------------------------------
#     # FORECAST COMPARISON
#     # --------------------------------------------------------

#     st.markdown(
#         '<div class="section-title">📊 Forecast Horizon Comparison</div>',
#         unsafe_allow_html=True
#     )

#     if (
#         not forecast_7_selected.empty
#         and not forecast_14_selected.empty
#         and not forecast_30_selected.empty
#     ):

#         comparison_df = pd.DataFrame({

#             "Forecast Horizon": [
#                 "7 Days",
#                 "14 Days",
#                 "30 Days"
#             ],

#             "Predicted Price": [
#                 forecast_7_selected.iloc[0]["Forecast_7D"],
#                 forecast_14_selected.iloc[0]["Forecast_14D"],
#                 forecast_30_selected.iloc[0]["Forecast_30D"]
#             ]
#         })

#         fig = px.bar(
#             comparison_df,
#             x="Forecast Horizon",
#             y="Predicted Price",
#             text_auto=".2f",
#             title="Predicted Price Across Forecast Horizons",
#             labels={
#                 "Predicted Price": "Predicted Price (₹/quintal)"
#             }
#         )

#         fig.update_layout(height=430)

#         st.plotly_chart(
#             fig,
#             use_container_width=True
#         )

#         st.markdown(
#             """
#             <div class="insight-box">
#             <b>💡 Inference:</b>
#             The chart compares the model's predicted price across
#             7-day, 14-day and 30-day forecasting horizons.
#             Longer horizons naturally contain more uncertainty,
#             so predictions should be interpreted as model estimates
#             rather than guaranteed market prices.
#             </div>
#             """,
#             unsafe_allow_html=True
#         )


# # ============================================================
# # TAB 5 — MODEL PERFORMANCE
# # ============================================================

# with tab5:

#     st.markdown(
#         '<div class="section-title">🤖 Model Performance</div>',
#         unsafe_allow_html=True
#     )

#     performance_df = pd.DataFrame({

#         "Forecast Horizon": [
#             "7 Days",
#             "14 Days",
#             "30 Days"
#         ],

#         "MAE": [
#             297.649862,
#             374.776872,
#             537.523449
#         ],

#         "RMSE": [
#             1579.480756,
#             1586.331959,
#             990.548881
#         ],

#         "MAPE (%)": [
#             18.455095,
#             25.272335,
#             38.426064
#         ]
#     })


#     st.dataframe(
#         performance_df,
#         use_container_width=True,
#         hide_index=True
#     )


#     # --------------------------------------------------------
#     # MAPE GRAPH
#     # --------------------------------------------------------

#     fig = px.bar(
#         performance_df,
#         x="Forecast Horizon",
#         y="MAPE (%)",
#         text_auto=".2f",
#         title="MAPE by Forecast Horizon",
#         labels={
#             "MAPE (%)": "MAPE (%)"
#         }
#     )

#     fig.update_layout(height=400)

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )


#     st.markdown(
#         """
#         <div class="insight-box">
#         <b>💡 Inference:</b>
#         The model performance metrics quantify forecasting error
#         at each prediction horizon. MAE represents average absolute
#         error, RMSE gives greater weight to larger errors, and MAPE
#         expresses the error relative to the actual price.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


# # ============================================================
# # FOOTER
# # ============================================================

# st.markdown("---")

# st.caption(
#     "🌾 Agricultural Market Price Analyzer | "
#     "Historical Price Analysis • Weather Correlation • "
#     "Seasonality • Machine Learning Forecasting"
# )



import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Agricultural Market Price Analyzer",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   MAIN APP
   ========================================================= */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    padding: 28px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        #1b5e20,
        #43a047
    );
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white !important;
    font-size: 38px;
    margin-bottom: 8px;
}

.hero p {
    color: white !important;
    font-size: 17px;
    margin-bottom: 0;
}


/* =========================================================
   SECTION HEADINGS
   ========================================================= */

.section-title {
    font-size: 27px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}


/* =========================================================
   INSIGHT BOX
   ========================================================= */

.insight-box {
    padding: 16px 20px;
    border-radius: 12px;

    background-color: #e8f5e9;

    border-left: 5px solid #2e7d32;

    margin-top: 8px;
    margin-bottom: 20px;

    color: #1b1b1b !important;

    font-size: 15px;
    line-height: 1.6;
}

.insight-box b {
    color: #1b5e20 !important;
}


/* =========================================================
   INFO BOX
   ========================================================= */

.info-box {
    padding: 16px 20px;
    border-radius: 12px;

    background-color: #e3f2fd;

    border-left: 5px solid #1565c0;

    margin-top: 8px;
    margin-bottom: 20px;

    color: #123 !important;

    font-size: 15px;
}


/* =========================================================
   METRIC CARDS
   ========================================================= */

div[data-testid="stMetric"] {
    background-color: white !important;

    padding: 18px;

    border-radius: 14px;

    border: 1px solid #e0e0e0;

    box-shadow:
        0px 3px 10px rgba(0,0,0,0.08);
}

div[data-testid="stMetric"] label {
    color: #555555 !important;
}

div[data-testid="stMetric"] div {
    color: #111111 !important;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background-color: #f1f8f2 !important;
}

section[data-testid="stSidebar"] * {
    color: #1b1b1b;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #1b5e20 !important;
}


/* =========================================================
   SELECTBOX
   ========================================================= */

div[data-baseweb="select"] > div {
    background-color: white !important;

    border-radius: 8px;

    border: 1px solid #cfd8dc;
}

div[data-baseweb="select"] span {
    color: #222 !important;
}


/* =========================================================
   TABS
   ========================================================= */

button[data-baseweb="tab"] {
    font-weight: 600;
}


/* =========================================================
   DATAFRAME
   ========================================================= */

div[data-testid="stDataFrame"] {
    border-radius: 12px;
}


/* =========================================================
   CAPTION
   ========================================================= */

.stCaption {
    color: #555 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<h1>🌾 Agricultural Market Price Analyzer</h1>

<p>
Explore agricultural commodity prices, seasonal patterns,
weather relationships and machine-learning based price forecasts.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    features_df = pd.read_csv(
        "agricultural_market_final_features.csv"
    )

    organized_price_df = pd.read_csv(
        "organized_price_data.csv"
    )

    forecast_7d_df = pd.read_csv(
        "forecast_7d_all.csv"
    )

    forecast_14d_df = pd.read_csv(
        "forecast_14d_all.csv"
    )

    forecast_30d_df = pd.read_csv(
        "forecast_30d_all.csv"
    )

    return (
        features_df,
        organized_price_df,
        forecast_7d_df,
        forecast_14d_df,
        forecast_30d_df
    )


(
    features_df,
    organized_price_df,
    forecast_7d_df,
    forecast_14d_df,
    forecast_30d_df
) = load_data()


# ============================================================
# DATA PREPARATION
# ============================================================

features_df["Week"] = pd.to_datetime(
    features_df["Week"],
    errors="coerce"
)

organized_price_df["Date"] = pd.to_datetime(
    organized_price_df["Date"],
    errors="coerce"
)

organized_price_df["Modal_Price"] = pd.to_numeric(
    organized_price_df["Modal_Price"],
    errors="coerce"
)


# ============================================================
# STATE NAME STANDARDIZATION
# ============================================================

state_mapping = {
    "Tamilnadu": "Tamil Nadu",
    "Chattisgarh": "Chhattisgarh",
    "Jammu & Kashmir": "Jammu and Kashmir",
    "Gao": "Goa",
    "Uttrakhand": "Uttarakhand"
}

features_df["State"] = features_df["State"].replace(
    state_mapping
)

organized_price_df["State"] = organized_price_df["State"].replace(
    state_mapping
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🌾 Dashboard Controls")

st.sidebar.markdown(
    "Select the location and commodity "
    "you want to analyze."
)


# ============================================================
# STATE SELECTION
# ============================================================

state_options = sorted(
    features_df["State"]
    .dropna()
    .unique()
)

selected_state = st.sidebar.selectbox(
    "📍 Select State",
    state_options
)


# ============================================================
# DISTRICT SELECTION
# ============================================================

district_options = sorted(
    features_df[
        features_df["State"] == selected_state
    ]["District"]
    .dropna()
    .unique()
)

selected_district = st.sidebar.selectbox(
    "🏙️ Select District",
    district_options
)


# ============================================================
# COMMODITY SELECTION
# ============================================================

commodity_options = sorted(
    features_df[
        (features_df["State"] == selected_state) &
        (features_df["District"] == selected_district)
    ]["Commodity"]
    .dropna()
    .unique()
)

selected_commodity = st.sidebar.selectbox(
    "🥕 Select Commodity",
    commodity_options
)


# ============================================================
# SIDEBAR SELECTION SUMMARY
# ============================================================

st.sidebar.markdown("---")

st.sidebar.markdown(
    f"""
    **Current Selection**

    📍 **State:** {selected_state}

    🏙️ **District:** {selected_district}

    🥕 **Commodity:** {selected_commodity}
    """
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Use the tabs on the main dashboard "
    "to explore prices, weather, relationships "
    "and forecasts."
)


# ============================================================
# FILTER SELECTED SERIES
# ============================================================

selected_data = features_df[
    (features_df["State"] == selected_state) &
    (features_df["District"] == selected_district) &
    (features_df["Commodity"] == selected_commodity)
].copy()

selected_data = selected_data.sort_values(
    "Week"
)


# ============================================================
# SELECTED SERIES OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">📊 Selected Series Overview</div>',
    unsafe_allow_html=True
)

if not selected_data.empty:

    avg_price = selected_data[
        "Median_Modal_Price"
    ].mean()

    min_price = selected_data[
        "Median_Modal_Price"
    ].min()

    max_price = selected_data[
        "Median_Modal_Price"
    ].max()

    price_std = selected_data[
        "Median_Modal_Price"
    ].std()

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Average Price",
            f"₹{avg_price:,.2f}"
        )

    with c2:

        st.metric(
            "Minimum Price",
            f"₹{min_price:,.2f}"
        )

    with c3:

        st.metric(
            "Maximum Price",
            f"₹{max_price:,.2f}"
        )

    with c4:

        st.metric(
            "Price Std. Dev.",
            f"₹{price_std:,.2f}"
        )


# ============================================================
# MAIN TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📈 Price Analysis",
        "🌦️ Weather Analysis",
        "🔗 Weather Relationships",
        "🔮 Forecasts",
        "🤖 Model Performance"
    ]
)


# ============================================================
# TAB 1 — PRICE ANALYSIS
# ============================================================

with tab1:

    # ========================================================
    # HISTORICAL PRICE TREND
    # ========================================================

    st.markdown(
        '<div class="section-title">📈 Historical Price Trend</div>',
        unsafe_allow_html=True
    )

    if not selected_data.empty:

        fig = px.line(
            selected_data,
            x="Week",
            y="Median_Modal_Price",
            markers=True,
            title=(
                f"{selected_commodity} Price Trend — "
                f"{selected_district}"
            ),
            labels={
                "Week": "Week",
                "Median_Modal_Price":
                    "Median Modal Price (₹/quintal)"
            }
        )

        fig.update_layout(
            hovermode="x unified",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        first_price = selected_data.iloc[0][
            "Median_Modal_Price"
        ]

        last_price = selected_data.iloc[-1][
            "Median_Modal_Price"
        ]

        if last_price > first_price:

            direction = "increased"

        elif last_price < first_price:

            direction = "decreased"

        else:

            direction = "remained broadly stable"

        st.markdown(
            f"""
            <div class="insight-box">
            <b>💡 Inference:</b>
            The historical median modal price has {direction}
            over the available period for
            <b>{selected_commodity}</b> in
            <b>{selected_district}</b>.
            The graph shows the actual weekly movement
            of the commodity price.
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # MONTHLY PRICE PATTERN
    # ========================================================

    st.markdown(
        '<div class="section-title">📅 Monthly Price Pattern</div>',
        unsafe_allow_html=True
    )

    monthly_df = features_df.copy()

    monthly_df["Month_Name"] = (
        monthly_df["Week"]
        .dt.month_name()
    )

    monthly_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    monthly_pattern = (
        monthly_df
        .groupby(
            ["Month", "Month_Name"],
            as_index=False
        )["Median_Modal_Price"]
        .median()
        .sort_values("Month")
    )

    fig = px.line(
        monthly_pattern,
        x="Month_Name",
        y="Median_Modal_Price",
        markers=True,
        category_orders={
            "Month_Name": monthly_order
        },
        title="Overall Monthly Median Modal Price",
        labels={
            "Month_Name": "Month",
            "Median_Modal_Price":
                "Median Price (₹/quintal)"
        }
    )

    fig.update_layout(
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    highest_month = monthly_pattern.loc[
        monthly_pattern["Median_Modal_Price"].idxmax(),
        "Month_Name"
    ]

    lowest_month = monthly_pattern.loc[
        monthly_pattern["Median_Modal_Price"].idxmin(),
        "Month_Name"
    ]

    st.markdown(
        f"""
        <div class="insight-box">
        <b>💡 Inference:</b>
        The monthly pattern indicates that agricultural prices
        vary across the year. In the analyzed dataset,
        <b>{highest_month}</b> has the highest median price,
        while <b>{lowest_month}</b> has the lowest median price.
        This indicates the presence of seasonal price variation.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # WEEKLY PRICE PATTERN
    # ========================================================

    st.markdown(
        '<div class="section-title">🗓️ Weekly Seasonal Pattern</div>',
        unsafe_allow_html=True
    )

    weekly_pattern = (
        features_df
        .assign(
            Week_Number=
            features_df["Week"]
            .dt.isocalendar()
            .week
            .astype(int)
        )
        .groupby(
            "Week_Number",
            as_index=False
        )["Median_Modal_Price"]
        .median()
    )

    fig = px.line(
        weekly_pattern,
        x="Week_Number",
        y="Median_Modal_Price",
        markers=True,
        title="Median Price by Week of Year",
        labels={
            "Week_Number": "Week Number",
            "Median_Modal_Price":
                "Median Price (₹/quintal)"
        }
    )

    fig.update_layout(
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        """
        <div class="insight-box">
        <b>💡 Inference:</b>
        Prices do not remain constant throughout the year.
        The weekly pattern shows periods of relatively lower
        and higher prices, indicating recurring seasonal behavior
        in the agricultural market.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # SEASONAL PATTERN
    # ========================================================

    st.markdown(
        '<div class="section-title">🌱 Seasonal Price Pattern</div>',
        unsafe_allow_html=True
    )

    season_order = [
        "Winter",
        "Summer",
        "Monsoon",
        "Post-Monsoon"
    ]

    seasonal_df = (
        features_df
        .groupby(
            "Season",
            as_index=False
        )["Median_Modal_Price"]
        .median()
    )

    seasonal_df["Season"] = pd.Categorical(
        seasonal_df["Season"],
        categories=season_order,
        ordered=True
    )

    seasonal_df = seasonal_df.sort_values(
        "Season"
    )

    fig = px.bar(
        seasonal_df,
        x="Season",
        y="Median_Modal_Price",
        title="Median Price Across Seasons",
        labels={
            "Median_Modal_Price":
                "Median Price (₹/quintal)"
        },
        text_auto=".0f"
    )

    fig.update_layout(
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    highest_season = seasonal_df.loc[
        seasonal_df["Median_Modal_Price"].idxmax(),
        "Season"
    ]

    lowest_season = seasonal_df.loc[
        seasonal_df["Median_Modal_Price"].idxmin(),
        "Season"
    ]

    st.markdown(
        f"""
        <div class="insight-box">
        <b>💡 Inference:</b>
        Among the defined seasons,
        <b>{highest_season}</b> has the highest overall
        median price and
        <b>{lowest_season}</b> has the lowest.
        This suggests that seasonal conditions are associated
        with changes in market prices.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # STATE COMPARISON
    # ========================================================

    st.markdown(
        '<div class="section-title">🗺️ State-wise Price Comparison</div>',
        unsafe_allow_html=True
    )

    state_comparison = (
        features_df
        .groupby(
            "State",
            as_index=False
        )["Median_Modal_Price"]
        .median()
        .sort_values(
            "Median_Modal_Price",
            ascending=False
        )
    )

    fig = px.bar(
        state_comparison,
        x="State",
        y="Median_Modal_Price",
        title="Median Modal Price by State",
        labels={
            "Median_Modal_Price":
                "Median Price (₹/quintal)"
        }
    )

    fig.update_layout(
        height=500,
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        """
        <div class="insight-box">
        <b>💡 Inference:</b>
        Median commodity prices differ considerably across states.
        This reflects geographical differences in agricultural
        production, markets, supply conditions and commodity mix.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # COMMODITY COMPARISON
    # ========================================================

    st.markdown(
        '<div class="section-title">🥕 Commodity-wise Price Comparison</div>',
        unsafe_allow_html=True
    )

    commodity_comparison = (
        features_df
        .groupby(
            "Commodity",
            as_index=False
        )["Median_Modal_Price"]
        .median()
        .sort_values(
            "Median_Modal_Price",
            ascending=False
        )
    )

    fig = px.bar(
        commodity_comparison,
        x="Commodity",
        y="Median_Modal_Price",
        title="Median Price by Commodity",
        labels={
            "Median_Modal_Price":
                "Median Price (₹/quintal)"
        },
        text_auto=".0f"
    )

    fig.update_layout(
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        """
        <div class="insight-box">
        <b>💡 Inference:</b>
        Different commodities have substantially different
        price levels. Therefore, price forecasting needs to
        preserve commodity-specific time-series behavior
        rather than treating all commodities as one sequence.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # MARKET COMPARISON
    # ========================================================

    st.markdown(
        '<div class="section-title">🏪 Market-wise Price Comparison</div>',
        unsafe_allow_html=True
    )

    market_comparison = (
        organized_price_df
        .groupby(
            [
                "State",
                "District",
                "Market"
            ],
            as_index=False
        )
        .agg(
            Median_Modal_Price=(
                "Modal_Price",
                "median"
            ),
            Record_Count=(
                "Modal_Price",
                "count"
            )
        )
    )

    market_comparison = market_comparison.dropna(
        subset=["Median_Modal_Price"]
    )

    top_markets = (
        market_comparison
        .sort_values(
            "Median_Modal_Price",
            ascending=False
        )
        .head(15)
        .copy()
    )

    top_markets["Market_Label"] = (
        top_markets["Market"] +
        " (" +
        top_markets["District"] +
        ")"
    )

    fig = px.bar(
        top_markets.sort_values(
            "Median_Modal_Price"
        ),
        x="Median_Modal_Price",
        y="Market_Label",
        orientation="h",
        title="Top 15 Markets by Median Modal Price",
        labels={
            "Median_Modal_Price":
                "Median Price (₹/quintal)",
            "Market_Label":
                "Market"
        }
    )

    fig.update_layout(
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        """
        <div class="insight-box">
        <b>💡 Inference:</b>
        Market-level prices show substantial variation.
        This demonstrates that geographical location at the
        market and district level can be important when
        interpreting agricultural commodity prices.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # PRICE VOLATILITY
    # ========================================================

    st.markdown(
        '<div class="section-title">📦 Price Volatility</div>',
        unsafe_allow_html=True
    )

    volatility_df = features_df[
        [
            "Commodity",
            "Median_Modal_Price"
        ]
    ].dropna()

    fig = px.box(
        volatility_df,
        x="Commodity",
        y="Median_Modal_Price",
        points=False,
        title="Price Distribution and Volatility by Commodity",
        labels={
            "Median_Modal_Price":
                "Median Modal Price (₹/quintal)"
        }
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        """
        <div class="insight-box">
        <b>💡 Inference:</b>
        The box plot shows the spread and variability of prices
        for each commodity. A wider distribution indicates
        greater variation in observed prices across locations
        and periods.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TAB 2 — WEATHER ANALYSIS
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-title">🌦️ Weather Analysis</div>',
        unsafe_allow_html=True
    )

    if not selected_data.empty:

        weather_col1, weather_col2, weather_col3 = st.columns(3)

        avg_temperature = selected_data[
            "Mean_Temperature"
        ].mean()

        avg_humidity = selected_data[
            "Mean_Humidity"
        ].mean()

        total_rainfall = selected_data[
            "Total_Rainfall"
        ].sum()

        with weather_col1:

            st.metric(
                "Average Temperature",
                f"{avg_temperature:.2f} °C"
            )

        with weather_col2:

            st.metric(
                "Average Humidity",
                f"{avg_humidity:.2f} %"
            )

        with weather_col3:

            st.metric(
                "Total Rainfall",
                f"{total_rainfall:.2f} mm"
            )


        # ====================================================
        # TEMPERATURE TREND
        # ====================================================

        st.subheader("🌡️ Temperature Trend")

        fig = px.line(
            selected_data,
            x="Week",
            y="Mean_Temperature",
            markers=True,
            title="Weekly Mean Temperature",
            labels={
                "Mean_Temperature":
                    "Mean Temperature (°C)"
            }
        )

        fig.update_layout(
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown(
            """
            <div class="insight-box">
            <b>💡 Inference:</b>
            Temperature varies over time according to seasonal
            weather conditions. The trend can be compared with
            the corresponding commodity price movement.
            </div>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # HUMIDITY TREND
        # ====================================================

        st.subheader("💧 Humidity Trend")

        fig = px.line(
            selected_data,
            x="Week",
            y="Mean_Humidity",
            markers=True,
            title="Weekly Mean Humidity",
            labels={
                "Mean_Humidity":
                    "Mean Humidity (%)"
            }
        )

        fig.update_layout(
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown(
            """
            <div class="insight-box">
            <b>💡 Inference:</b>
            Humidity changes across the agricultural season.
            Humidity also showed a measurable relationship with
            price in the overall EDA, making it useful as a
            forecasting feature.
            </div>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # RAINFALL TREND
        # ====================================================

        st.subheader("🌧️ Rainfall Trend")

        fig = px.bar(
            selected_data,
            x="Week",
            y="Total_Rainfall",
            title="Weekly Total Rainfall",
            labels={
                "Total_Rainfall":
                    "Total Rainfall (mm)"
            }
        )

        fig.update_layout(
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown(
            """
            <div class="insight-box">
            <b>💡 Inference:</b>
            Rainfall is time-dependent and varies considerably
            between weeks. This makes rainfall a useful external
            variable for agricultural price analysis and forecasting.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# TAB 3 — WEATHER RELATIONSHIPS
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-title">🔗 Price–Weather Relationships</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # CORRELATION MATRIX
    # ========================================================

    corr_cols = [
        "Median_Modal_Price",
        "Total_Rainfall",
        "Mean_Temperature",
        "Mean_Humidity"
    ]

    corr_df = features_df[
        corr_cols
    ].corr()

    price_rainfall_corr = corr_df.loc[
        "Median_Modal_Price",
        "Total_Rainfall"
    ]

    price_temperature_corr = corr_df.loc[
        "Median_Modal_Price",
        "Mean_Temperature"
    ]

    price_humidity_corr = corr_df.loc[
        "Median_Modal_Price",
        "Mean_Humidity"
    ]


    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Price ↔ Rainfall",
            f"{price_rainfall_corr:.3f}"
        )

    with c2:

        st.metric(
            "Price ↔ Temperature",
            f"{price_temperature_corr:.3f}"
        )

    with c3:

        st.metric(
            "Price ↔ Humidity",
            f"{price_humidity_corr:.3f}"
        )


    # ========================================================
    # PRICE VS RAINFALL
    # ========================================================

    st.subheader("🌧️ Price vs Rainfall")

    fig = px.scatter(
        features_df,
        x="Total_Rainfall",
        y="Median_Modal_Price",
        opacity=0.45,
        title="Commodity Price vs Total Rainfall",
        labels={
            "Total_Rainfall":
                "Total Rainfall (mm)",
            "Median_Modal_Price":
                "Median Price (₹/quintal)"
        }
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        f"""
        <div class="insight-box">
        <b>💡 Inference:</b>
        The correlation between price and rainfall in the
        analyzed dataset is <b>{price_rainfall_corr:.3f}</b>.
        This indicates a positive linear association,
        although correlation alone does not establish causation.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # PRICE VS TEMPERATURE
    # ========================================================

    st.subheader("🌡️ Price vs Temperature")

    fig = px.scatter(
        features_df,
        x="Mean_Temperature",
        y="Median_Modal_Price",
        opacity=0.45,
        title="Commodity Price vs Mean Temperature",
        labels={
            "Mean_Temperature":
                "Mean Temperature (°C)",
            "Median_Modal_Price":
                "Median Price (₹/quintal)"
        }
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        f"""
        <div class="insight-box">
        <b>💡 Inference:</b>
        The correlation between price and temperature is
        <b>{price_temperature_corr:.3f}</b>.
        This is close to zero in the overall dataset,
        indicating little linear association between these
        two variables at the aggregated level.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # PRICE VS HUMIDITY
    # ========================================================

    st.subheader("💧 Price vs Humidity")

    fig = px.scatter(
        features_df,
        x="Mean_Humidity",
        y="Median_Modal_Price",
        opacity=0.45,
        title="Commodity Price vs Mean Humidity",
        labels={
            "Mean_Humidity":
                "Mean Humidity (%)",
            "Median_Modal_Price":
                "Median Price (₹/quintal)"
        }
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        f"""
        <div class="insight-box">
        <b>💡 Inference:</b>
        The price-humidity correlation is
        <b>{price_humidity_corr:.3f}</b>.
        This represents a positive linear association in the
        analyzed dataset. Humidity therefore provides useful
        information for the forecasting feature set.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CORRELATION HEATMAP
    # ========================================================

    st.subheader("🔥 Weather Correlation Matrix")

    heatmap_data = features_df[
        [
            "Median_Modal_Price",
            "Total_Rainfall",
            "Mean_Temperature",
            "Mean_Humidity"
        ]
    ].corr()

    fig = px.imshow(
        heatmap_data,
        text_auto=".3f",
        aspect="auto",
        title="Correlation Matrix"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        """
        <div class="insight-box">
        <b>💡 Inference:</b>
        The correlation matrix summarizes the linear relationships
        among price and the three weather variables. It also shows
        the relationship between rainfall and humidity, so weather
        variables should be interpreted together rather than
        independently.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # WEATHER LAG ANALYSIS
    # ========================================================

    st.subheader("⏮️ Weather Lag Analysis")

    lag_correlations = {}

    lag_columns = [
        "Rainfall_Lag_1",
        "Rainfall_Lag_2",
        "Temperature_Lag_1",
        "Temperature_Lag_2",
        "Humidity_Lag_1",
        "Humidity_Lag_2"
    ]

    for col in lag_columns:

        if col in features_df.columns:

            temp = features_df[
                [
                    "Median_Modal_Price",
                    col
                ]
            ].dropna()

            if len(temp) > 1:

                lag_correlations[col] = (
                    temp[
                        "Median_Modal_Price"
                    ].corr(
                        temp[col]
                    )
                )


    lag_df = pd.DataFrame(
        list(
            lag_correlations.items()
        ),
        columns=[
            "Weather Feature",
            "Correlation"
        ]
    )

    lag_df = lag_df.sort_values(
        "Correlation",
        ascending=False
    )

    fig = px.bar(
        lag_df,
        x="Weather Feature",
        y="Correlation",
        title="Price Correlation with Previous Weather Conditions",
        labels={
            "Correlation":
                "Correlation with Price"
        },
        text_auto=".3f"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if not lag_df.empty:

        strongest_lag = lag_df.iloc[0]

        st.markdown(
            f"""
            <div class="insight-box">
            <b>💡 Inference:</b>
            Among the tested lagged weather variables,
            <b>{strongest_lag["Weather Feature"]}</b>
            has the highest observed correlation with price
            at approximately
            <b>{strongest_lag["Correlation"]:.3f}</b>.
            This supports including lagged weather variables
            as forecasting features.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# TAB 4 — FORECASTS
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-title">🔮 Future Price Forecast</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # FILTER FORECASTS
    # ========================================================

    forecast_7_selected = forecast_7d_df[
        (forecast_7d_df["State"] == selected_state) &
        (forecast_7d_df["District"] == selected_district) &
        (forecast_7d_df["Commodity"] == selected_commodity)
    ]

    forecast_14_selected = forecast_14d_df[
        (forecast_14d_df["State"] == selected_state) &
        (forecast_14d_df["District"] == selected_district) &
        (forecast_14d_df["Commodity"] == selected_commodity)
    ]

    forecast_30_selected = forecast_30d_df[
        (forecast_30d_df["State"] == selected_state) &
        (forecast_30d_df["District"] == selected_district) &
        (forecast_30d_df["Commodity"] == selected_commodity)
    ]


    forecast_col1, forecast_col2, forecast_col3 = st.columns(3)


    # ========================================================
    # 7 DAY FORECAST
    # ========================================================

    with forecast_col1:

        st.subheader("📅 7-Day Forecast")

        if not forecast_7_selected.empty:

            price_7d = forecast_7_selected.iloc[0][
                "Forecast_7D"
            ]

            st.metric(
                "Predicted Price",
                f"₹{price_7d:,.2f} / quintal"
            )

            st.caption(
                f"≈ ₹{price_7d / 100:,.2f} per kg"
            )

        else:

            st.info(
                "Forecast not available."
            )


    # ========================================================
    # 14 DAY FORECAST
    # ========================================================

    with forecast_col2:

        st.subheader("📅 14-Day Forecast")

        if not forecast_14_selected.empty:

            price_14d = forecast_14_selected.iloc[0][
                "Forecast_14D"
            ]

            st.metric(
                "Predicted Price",
                f"₹{price_14d:,.2f} / quintal"
            )

            st.caption(
                f"≈ ₹{price_14d / 100:,.2f} per kg"
            )

        else:

            st.info(
                "Forecast not available."
            )


    # ========================================================
    # 30 DAY FORECAST
    # ========================================================

    with forecast_col3:

        st.subheader("📅 30-Day Forecast")

        if not forecast_30_selected.empty:

            price_30d = forecast_30_selected.iloc[0][
                "Forecast_30D"
            ]

            st.metric(
                "Predicted Price",
                f"₹{price_30d:,.2f} / quintal"
            )

            st.caption(
                f"≈ ₹{price_30d / 100:,.2f} per kg"
            )

        else:

            st.info(
                "Forecast not available."
            )


    # ========================================================
    # FORECAST COMPARISON
    # ========================================================

    st.markdown(
        '<div class="section-title">📊 Forecast Horizon Comparison</div>',
        unsafe_allow_html=True
    )

    if (
        not forecast_7_selected.empty
        and not forecast_14_selected.empty
        and not forecast_30_selected.empty
    ):

        comparison_df = pd.DataFrame({

            "Forecast Horizon": [
                "7 Days",
                "14 Days",
                "30 Days"
            ],

            "Predicted Price": [
                forecast_7_selected.iloc[0][
                    "Forecast_7D"
                ],

                forecast_14_selected.iloc[0][
                    "Forecast_14D"
                ],

                forecast_30_selected.iloc[0][
                    "Forecast_30D"
                ]
            ]
        })


        fig = px.bar(
            comparison_df,
            x="Forecast Horizon",
            y="Predicted Price",
            text_auto=".2f",
            title="Predicted Price Across Forecast Horizons",
            labels={
                "Predicted Price":
                    "Predicted Price (₹/quintal)"
            }
        )

        fig.update_layout(
            height=430
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown(
            """
            <div class="insight-box">
            <b>💡 Inference:</b>
            The chart compares the model's predicted price
            across the 7-day, 14-day and 30-day forecasting
            horizons. Longer forecasting horizons generally
            involve greater uncertainty, so these values should
            be interpreted as model estimates rather than
            guaranteed market prices.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# TAB 5 — MODEL PERFORMANCE
# ============================================================

with tab5:

    st.markdown(
        '<div class="section-title">🤖 Model Performance</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # PERFORMANCE DATA
    # ========================================================

    performance_df = pd.DataFrame({

        "Forecast Horizon": [
            "7 Days",
            "14 Days",
            "30 Days"
        ],

        "MAE": [
            297.649862,
            374.776872,
            537.523449
        ],

        "RMSE": [
            1579.480756,
            1586.331959,
            990.548881
        ],

        "MAPE (%)": [
            18.455095,
            25.272335,
            38.426064
        ]
    })


    # ========================================================
    # PERFORMANCE TABLE
    # ========================================================

    st.dataframe(
        performance_df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # MAPE GRAPH
    # ========================================================

    fig = px.bar(
        performance_df,
        x="Forecast Horizon",
        y="MAPE (%)",
        text_auto=".2f",
        title="MAPE by Forecast Horizon",
        labels={
            "MAPE (%)":
                "MAPE (%)"
        }
    )

    fig.update_layout(
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # PERFORMANCE EXPLANATION
    # ========================================================

    st.markdown(
        """
        <div class="insight-box">
        <b>💡 Interpretation:</b>

        <br><br>

        <b>MAE:</b>
        Mean Absolute Error represents the average absolute
        difference between predicted and actual prices.

        <br><br>

        <b>RMSE:</b>
        Root Mean Squared Error gives greater weight to larger
        prediction errors.

        <br><br>

        <b>MAPE:</b>
        Mean Absolute Percentage Error expresses prediction
        error relative to the actual price.

        <br><br>

        These metrics are calculated from the global Random
        Forest forecasting models evaluated on the corresponding
        forecast horizons.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🌾 Agricultural Market Price Analyzer | "
    "Historical Price Analysis • Weather Correlation • "
    "Seasonality • Machine Learning Forecasting"
)