import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(
    page_title="Agricultural Market Price Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
.metric-card {
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,.25);
    background: rgba(128,128,128,.06);
}
.small-note {font-size: .9rem; color: #6b7280;}
</style>
""", unsafe_allow_html=True)

STATE_MAPPING = {
    "Tamilnadu": "Tamil Nadu",
    "Chattisgarh": "Chhattisgarh",
    "Jammu & Kashmir": "Jammu and Kashmir",
    "Gao": "Goa",
    "Uttrakhand": "Uttarakhand",
}

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


# -----------------------------
# Data preparation
# -----------------------------
@st.cache_data(show_spinner=False)
def load_price_data(file_bytes):
    df = pd.read_csv(BytesIO(file_bytes))

    # Accept either the notebook's original column names or cleaned names.
    rename_map = {
        "STATE": "State",
        "District Name": "District",
        "Market Name": "Market",
        "Price Date": "Date",
    }
    df = df.rename(columns=rename_map)

    required = [
        "State", "District", "Market", "Commodity",
        "Variety", "Grade", "Min_Price", "Max_Price",
        "Modal_Price", "Date"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            "The uploaded price CSV is missing these columns: "
            + ", ".join(missing)
        )

    # Same cleaning logic used in the notebook.
    df = df.drop_duplicates().copy()

    for c in ["State","District","Market","Commodity","Variety","Grade"]:
        df[c] = (
            df[c].astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

    df["State"] = df["State"].replace(STATE_MAPPING)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    for c in ["Min_Price","Max_Price","Modal_Price"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
        df.loc[df[c] <= 0, c] = np.nan

    df = df.dropna(subset=["Date"]).copy()
    df["Week"] = df["Date"].dt.to_period("W").apply(lambda x: x.start_time)
    return df


@st.cache_data(show_spinner=False)
def make_weekly_price(df):
    weekly = (
        df.groupby(["State","District","Commodity","Week"], as_index=False)
        .agg(
            Median_Modal_Price=("Modal_Price","median"),
            Median_Min_Price=("Min_Price","median"),
            Median_Max_Price=("Max_Price","median"),
        )
        .sort_values(["State","District","Commodity","Week"])
    )
    return weekly.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_optional_csv(file_bytes):
    return pd.read_csv(BytesIO(file_bytes))


@st.cache_data(show_spinner=False)
def prepare_merged_data(merged):
    d = merged.copy()
    if "Week" in d.columns:
        d["Week"] = pd.to_datetime(d["Week"], errors="coerce")
    if "Date" in d.columns:
        d["Date"] = pd.to_datetime(d["Date"], errors="coerce")
    for c in ["Median_Modal_Price","Median_Min_Price","Median_Max_Price",
              "Total_Rainfall","Mean_Temperature","Mean_Humidity"]:
        if c in d.columns:
            d[c] = pd.to_numeric(d[c], errors="coerce")
    if "State" in d.columns:
        d["State"] = d["State"].replace(STATE_MAPPING)
    return d


# -----------------------------
# Helper functions
# -----------------------------
def money(v):
    if pd.isna(v):
        return "—"
    return f"₹{v:,.0f}"


def explain(title, text):
    st.markdown(f"**How to read this chart:** {text}")


def metric_row(items):
    cols = st.columns(len(items))
    for col, (label, value, help_text) in zip(cols, items):
        col.metric(label, value, help=help_text)


# -----------------------------
# Header
# -----------------------------
st.title("🌾 Agricultural Market Price Intelligence Dashboard")
st.caption(
    "Interactive dashboard based on the analysis workflow in App.ipynb: "
    "cleaning → weekly aggregation → EDA → seasonality → weather relationships → forecasting."
)

st.info(
    "Upload the original agriculture price CSV used by the notebook. "
    "An optional merged/feature CSV can be uploaded for the weather and forecasting sections. "
    "The dashboard does not silently replace the notebook's terminology or cleaning logic."
)

# -----------------------------
# Sidebar inputs
# -----------------------------
st.sidebar.header("Data")
price_file = st.sidebar.file_uploader(
    "1. Agriculture price CSV",
    type=["csv"],
    help="The notebook expects columns such as STATE, District Name, Market Name, Commodity, Min_Price, Max_Price, Modal_Price and Price Date."
)

merged_file = st.sidebar.file_uploader(
    "2. Optional merged/feature CSV",
    type=["csv"],
    help="Upload merged_df or agricultural_market_final_features.csv if you want weather-correlation and model/feature charts."
)

forecast7_file = st.sidebar.file_uploader("Optional 7-day forecast CSV", type=["csv"])
forecast14_file = st.sidebar.file_uploader("Optional 14-day forecast CSV", type=["csv"])
forecast30_file = st.sidebar.file_uploader("Optional 30-day forecast CSV", type=["csv"])

if price_file is None:
    st.warning("Upload the agriculture price CSV in the sidebar to start the dashboard.")
    st.stop()

try:
    price_df = load_price_data(price_file.getvalue())
    weekly_df = make_weekly_price(price_df)
except Exception as e:
    st.error(f"Could not load the price file: {e}")
    st.stop()

merged_df = None
if merged_file is not None:
    try:
        merged_df = prepare_merged_data(load_optional_csv(merged_file.getvalue()))
    except Exception as e:
        st.warning(f"Optional merged/feature file could not be loaded: {e}")

# -----------------------------
# Global filters
# -----------------------------
st.sidebar.header("Filters")

states = sorted(weekly_df["State"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect(
    "State",
    states,
    default=states,
)

filtered = weekly_df[weekly_df["State"].isin(selected_states)].copy()

commodities = sorted(filtered["Commodity"].dropna().unique().tolist())
selected_commodities = st.sidebar.multiselect(
    "Commodity",
    commodities,
    default=commodities,
)

filtered = filtered[filtered["Commodity"].isin(selected_commodities)].copy()

min_date = filtered["Week"].min().date()
max_date = filtered["Week"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[
        (filtered["Week"].dt.date >= date_range[0]) &
        (filtered["Week"].dt.date <= date_range[1])
    ].copy()

# -----------------------------
# KPI cards
# -----------------------------
st.subheader("Dataset overview")

metric_row([
    ("Price records", f"{len(price_df):,}", "Rows after duplicate removal."),
    ("Weekly observations", f"{len(weekly_df):,}", "State–district–commodity–week records."),
    ("States", f"{weekly_df['State'].nunique():,}", "Unique standardized states."),
    ("Districts", f"{weekly_df['District'].nunique():,}", "Unique districts in the price data."),
    ("Commodities", f"{weekly_df['Commodity'].nunique():,}", "Unique commodities in the price data."),
])

if len(filtered):
    st.caption(
        f"Filtered period: {filtered['Week'].min().date()} → {filtered['Week'].max().date()}"
    )

tabs = st.tabs([
    "📊 Overview",
    "📈 Price Trends",
    "🗺️ Geography",
    "🌱 Seasonality & Volatility",
    "🌦️ Weather",
    "🔮 Forecasting",
    "🧾 Data Quality",
])

# ============================================================
# OVERVIEW
# ============================================================
with tabs[0]:
    st.header("1. Overview")

    if len(filtered):
        overall = (
            filtered.groupby("Week", as_index=False)
            .agg(
                Median_Modal_Price=("Median_Modal_Price","median"),
                Median_Min_Price=("Median_Min_Price","median"),
                Median_Max_Price=("Median_Max_Price","median"),
            )
        )

        fig = px.line(
            overall,
            x="Week",
            y=["Median_Modal_Price","Median_Min_Price","Median_Max_Price"],
            title="Overall Weekly Agricultural Commodity Price Trend",
            labels={"value":"Price","Week":"Week","variable":"Measure"},
        )
        st.plotly_chart(fig, use_container_width=True)
        explain(
            "Overall trend",
            "Each point represents the median across the available "
            "state–district–commodity weekly observations. The three lines show "
            "the weekly median modal, minimum and maximum prices."
        )

        c1, c2 = st.columns(2)

        with c1:
            commodity_summary = (
                filtered.groupby("Commodity", as_index=False)
                .agg(
                    Median_Price=("Median_Modal_Price","median"),
                    Mean_Price=("Median_Modal_Price","mean"),
                    Record_Count=("Median_Modal_Price","count"),
                )
                .sort_values("Median_Price", ascending=False)
            )
            fig = px.bar(
                commodity_summary,
                x="Commodity",
                y="Median_Price",
                title="Commodity-wise Median Modal Price",
                labels={"Median_Price":"Median modal price"},
            )
            st.plotly_chart(fig, use_container_width=True)
            explain(
                "Commodity comparison",
                "Higher bars indicate commodities with a higher typical weekly "
                "modal price in the selected data."
            )

        with c2:
            state_summary = (
                filtered.groupby("State", as_index=False)
                .agg(Median_Price=("Median_Modal_Price","median"))
                .sort_values("Median_Price", ascending=False)
            )
            fig = px.bar(
                state_summary,
                x="State",
                y="Median_Price",
                title="State-wise Median Modal Price",
                labels={"Median_Price":"Median modal price"},
            )
            fig.update_layout(xaxis_tickangle=-60)
            st.plotly_chart(fig, use_container_width=True)
            explain(
                "State comparison",
                "This compares the typical weekly modal price across standardized "
                "state names. It is a descriptive comparison, not a measure of farm income or profitability."
            )
    else:
        st.warning("No observations match the current filters.")

# ============================================================
# PRICE TRENDS
# ============================================================
with tabs[1]:
    st.header("2. Price trends and market comparisons")

    if not len(filtered):
        st.warning("No observations match the current filters.")
    else:
        c1, c2 = st.columns(2)

        district_summary = (
            filtered.groupby("District", as_index=False)
            .agg(Median_Price=("Median_Modal_Price","median"))
        )

        top15 = district_summary.nlargest(15, "Median_Price").sort_values("Median_Price")
        bottom15 = district_summary.nsmallest(15, "Median_Price").sort_values("Median_Price")

        with c1:
            fig = px.bar(
                top15,
                x="Median_Price",
                y="District",
                orientation="h",
                title="Top 15 Districts by Median Modal Price",
                labels={"Median_Price":"Median modal price"},
            )
            st.plotly_chart(fig, use_container_width=True)
            explain(
                "Top districts",
                "The chart displays the 15 districts with the highest median modal price "
                "within the selected filters."
            )

        with c2:
            fig = px.bar(
                bottom15,
                x="Median_Price",
                y="District",
                orientation="h",
                title="Bottom 15 Districts by Median Modal Price",
                labels={"Median_Price":"Median modal price"},
            )
            st.plotly_chart(fig, use_container_width=True)
            explain(
                "Bottom districts",
                "The chart displays the 15 districts with the lowest median modal price "
                "within the selected filters."
            )

        st.subheader("Market-level comparison")
        market_summary = (
            price_df[
                price_df["State"].isin(selected_states) &
                price_df["Commodity"].isin(selected_commodities)
            ]
            .groupby(["State","District","Market"], as_index=False)
            .agg(
                Median_Modal_Price=("Modal_Price","median"),
                Record_Count=("Modal_Price","count"),
            )
            .dropna(subset=["Median_Modal_Price"])
        )

        if len(market_summary):
            market_summary["Location"] = (
                market_summary["Market"].astype(str)
                + " | " + market_summary["District"].astype(str)
                + " | " + market_summary["State"].astype(str)
            )
            top_market = market_summary.nlargest(20, "Median_Modal_Price").sort_values("Median_Modal_Price")
            fig = px.bar(
                top_market,
                x="Median_Modal_Price",
                y="Location",
                orientation="h",
                title="Top 20 Markets by Median Modal Price",
                labels={"Median_Modal_Price":"Median modal price"},
            )
            st.plotly_chart(fig, use_container_width=True)
            explain(
                "Market comparison",
                "Each bar represents the median modal price for a market across its available records. "
                "The market label includes market, district and state."
            )

# ============================================================
# SEASONALITY / VOLATILITY
# ============================================================
with tabs[2]:
    st.header("3. Geography")
    st.write(
        "Use the filters to investigate how the price distribution changes across "
        "states and districts. The notebook's geographic analysis is based on median modal prices."
    )

    state_geo = (
        filtered.groupby("State", as_index=False)
        .agg(
            Median_Price=("Median_Modal_Price","median"),
            Mean_Price=("Median_Modal_Price","mean"),
            Record_Count=("Median_Modal_Price","count"),
        )
        .sort_values("Median_Price", ascending=False)
    )
    st.dataframe(state_geo, use_container_width=True, hide_index=True)

    st.subheader("District detail")
    chosen_state = st.selectbox(
        "Choose a state for district analysis",
        sorted(filtered["State"].dropna().unique())
    )
    district_geo = (
        filtered[filtered["State"] == chosen_state]
        .groupby("District", as_index=False)
        .agg(
            Median_Price=("Median_Modal_Price","median"),
            Mean_Price=("Median_Modal_Price","mean"),
            Record_Count=("Median_Modal_Price","count"),
        )
        .sort_values("Median_Price", ascending=False)
    )
    fig = px.bar(
        district_geo,
        x="District",
        y="Median_Price",
        title=f"District-wise Median Modal Price — {chosen_state}",
        labels={"Median_Price":"Median modal price"},
    )
    fig.update_layout(xaxis_tickangle=-60)
    st.plotly_chart(fig, use_container_width=True)
    explain(
        "District detail",
        "This narrows the state comparison to individual districts so that local "
        "price differences can be inspected without mixing every state together."
    )

with tabs[3]:
    st.header("4. Seasonality and price volatility")

    if not len(filtered):
        st.warning("No observations match the current filters.")
    else:
        season = filtered.copy()
        season["Month"] = season["Week"].dt.month
        season["Week_Number"] = season["Week"].dt.isocalendar().week.astype(int)

        monthly = (
            season.groupby("Month", as_index=False)
            .agg(Median_Price=("Median_Modal_Price","median"))
        )
        monthly["Month_Name"] = monthly["Month"].map(
            {i: m for i, m in enumerate(MONTHS, start=1)}
        )

        fig = px.line(
            monthly,
            x="Month_Name",
            y="Median_Price",
            markers=True,
            category_orders={"Month_Name": MONTHS},
            title="Monthly Seasonal Price Pattern",
            labels={"Median_Price":"Median modal price","Month_Name":"Month"},
        )
        st.plotly_chart(fig, use_container_width=True)
        explain(
            "Monthly seasonality",
            "The line connects the median price for each calendar month. Repeated "
            "high or low levels across the year can indicate a seasonal pattern in the selected data."
        )

        weekly_pattern = (
            season.groupby("Week_Number", as_index=False)
            .agg(Median_Price=("Median_Modal_Price","median"))
        )
        fig = px.line(
            weekly_pattern,
            x="Week_Number",
            y="Median_Price",
            title="Weekly Seasonal Price Pattern",
            labels={"Week_Number":"ISO week number","Median_Price":"Median modal price"},
        )
        st.plotly_chart(fig, use_container_width=True)
        explain(
            "Weekly seasonality",
            "This shows the typical price level by week-of-year, which helps reveal "
            "recurring patterns that may be hidden in a long chronological time series."
        )

        commodity_monthly = (
            season.groupby(["Commodity","Month"], as_index=False)
            .agg(Median_Price=("Median_Modal_Price","median"))
        )
        commodity_monthly["Month_Name"] = commodity_monthly["Month"].map(
            {i: m for i, m in enumerate(MONTHS, start=1)}
        )

        fig = px.line(
            commodity_monthly,
            x="Month_Name",
            y="Median_Price",
            color="Commodity",
            markers=True,
            category_orders={"Month_Name": MONTHS},
            title="Commodity-wise Monthly Seasonal Price Pattern",
            labels={"Median_Price":"Median modal price","Month_Name":"Month"},
        )
        st.plotly_chart(fig, use_container_width=True)
        explain(
            "Commodity seasonality",
            "Each commodity gets its own monthly line. This makes it possible to "
            "see whether different commodities follow different seasonal patterns."
        )

        volatility = (
            filtered.groupby("Commodity", as_index=False)
            .agg(
                Mean_Price=("Median_Modal_Price","mean"),
                Std_Price=("Median_Modal_Price","std"),
            )
        )
        volatility["CV_Percent"] = (
            volatility["Std_Price"] / volatility["Mean_Price"] * 100
        )
        volatility = volatility.replace([np.inf,-np.inf], np.nan).dropna()
        volatility = volatility.sort_values("CV_Percent", ascending=False)

        fig = px.bar(
            volatility,
            x="Commodity",
            y="CV_Percent",
            title="Commodity-wise Price Volatility",
            labels={"CV_Percent":"Coefficient of variation (%)"},
        )
        st.plotly_chart(fig, use_container_width=True)
        explain(
            "Price volatility",
            "The coefficient of variation is standard deviation divided by mean price, "
            "expressed as a percentage. It measures relative variability rather than absolute price."
        )

# ============================================================
# WEATHER
# ============================================================
with tabs[4]:
    st.header("5. Weather–price relationships")

    if merged_df is None:
        st.warning(
            "Upload the notebook's merged/feature CSV to enable weather charts. "
            "The notebook's weather analysis uses Total_Rainfall, Mean_Temperature and Mean_Humidity."
        )
        st.code(
            "Expected weather columns:\n"
            "Total_Rainfall\n"
            "Mean_Temperature\n"
            "Mean_Humidity\n"
            "Median_Modal_Price"
        )
    elif not {"Median_Modal_Price","Total_Rainfall","Mean_Temperature","Mean_Humidity"}.issubset(merged_df.columns):
        st.error("The optional file does not contain all required weather/price columns.")
    else:
        weather = merged_df[
            ["Median_Modal_Price","Total_Rainfall","Mean_Temperature","Mean_Humidity"]
        ].corr()

        fig = go.Figure(
            data=go.Heatmap(
                z=weather.values,
                x=weather.columns,
                y=weather.columns,
                zmin=-1,
                zmax=1,
                text=np.round(weather.values, 2),
                texttemplate="%{text}",
                colorscale="RdBu",
                colorbar_title="Correlation",
            )
        )
        fig.update_layout(title="Weather–Price Correlation Matrix")
        st.plotly_chart(fig, use_container_width=True)

        explain(
            "Correlation matrix",
            "Correlation ranges from -1 to +1. Positive values indicate that the two "
            "variables move together in the observed data; negative values indicate opposite movement. "
            "Correlation alone does not establish causation."
        )

        price_corr = (
            weather["Median_Modal_Price"]
            .drop("Median_Modal_Price")
            .sort_values(ascending=False)
            .reset_index()
        )
        price_corr.columns = ["Weather_Variable","Correlation"]

        fig = px.bar(
            price_corr,
            x="Weather_Variable",
            y="Correlation",
            title="Weather Variables Correlated with Median Modal Price",
            labels={"Correlation":"Correlation with price"},
        )
        fig.update_yaxes(range=[-1,1])
        st.plotly_chart(fig, use_container_width=True)

        # Lag correlations from notebook logic.
        lag = merged_df.copy()
        group_cols = ["State","District","Commodity"]
        if all(c in lag.columns for c in group_cols):
            lag = lag.sort_values(group_cols + ["Week"])
            for c in ["Total_Rainfall","Mean_Temperature","Mean_Humidity"]:
                lag[f"{c}_Lag_1"] = lag.groupby(group_cols)[c].shift(1)
                lag[f"{c}_Lag_2"] = lag.groupby(group_cols)[c].shift(2)

            lag_cols = [
                "Total_Rainfall_Lag_1","Total_Rainfall_Lag_2",
                "Mean_Temperature_Lag_1","Mean_Temperature_Lag_2",
                "Mean_Humidity_Lag_1","Mean_Humidity_Lag_2",
            ]
            lag_corr = lag[["Median_Modal_Price"] + lag_cols].corr()["Median_Modal_Price"].drop("Median_Modal_Price")
            lag_corr = lag_corr.sort_values(ascending=False).reset_index()
            lag_corr.columns = ["Lagged_Weather_Variable","Correlation"]

            fig = px.bar(
                lag_corr,
                x="Lagged_Weather_Variable",
                y="Correlation",
                title="Weather Lag–Price Correlation",
                labels={"Correlation":"Correlation with price"},
            )
            fig.update_yaxes(range=[-1,1])
            st.plotly_chart(fig, use_container_width=True)
            explain(
                "Weather lag relationship",
                "The lag chart compares price with weather from one or two previous weekly periods, "
                "following the notebook's lag-feature approach."
            )

# ============================================================
# FORECASTING
# ============================================================
with tabs[5]:
    st.header("6. Forecasting and model outputs")

    st.markdown(
        "The notebook creates 7-day, 14-day and 30-day targets and evaluates forecasting models "
        "using MAE, RMSE and MAPE. If you upload the notebook's forecast output files, the dashboard "
        "can visualize those final predictions directly."
    )

    forecast_files = [
        ("7-Day", forecast7_file, "Forecast_7D"),
        ("14-Day", forecast14_file, "Forecast_14D"),
        ("30-Day", forecast30_file, "Forecast_30D"),
    ]

    for label, f, pred_col in forecast_files:
        if f is not None:
            try:
                fc = load_optional_csv(f.getvalue())
                required_fc = {"State","District","Commodity","Latest_Week","Latest_Price",pred_col}
                if required_fc.issubset(fc.columns):
                    st.subheader(f"{label} forecast")
                    fc["Forecast_Change"] = fc[pred_col] - fc["Latest_Price"]
                    display_fc = fc.copy()

                    c1, c2 = st.columns(2)
                    with c1:
                        fig = px.scatter(
                            display_fc.sample(min(5000, len(display_fc)), random_state=42),
                            x="Latest_Price",
                            y=pred_col,
                            hover_data=["State","District","Commodity"],
                            title=f"{label}: Latest Price vs Forecast",
                            labels={pred_col:"Forecast price","Latest_Price":"Latest price"},
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        explain(
                            f"{label} forecast scatter",
                            "Each point is a State–District–Commodity series. Points close to the diagonal "
                            "would have forecasts close to their latest observed price."
                        )

                    with c2:
                        summary = (
                            display_fc.assign(
                                Direction=np.where(
                                    display_fc["Forecast_Change"] > 0, "Increase",
                                    np.where(display_fc["Forecast_Change"] < 0, "Decrease", "No change")
                                )
                            )
                            .groupby("Direction", as_index=False)
                            .size()
                            .rename(columns={"size":"Series_Count"})
                        )
                        fig = px.bar(
                            summary,
                            x="Direction",
                            y="Series_Count",
                            title=f"{label}: Forecast Direction",
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        explain(
                            f"{label} forecast direction",
                            "This counts how many series have a forecast above, below or equal to the latest price."
                        )

                    st.dataframe(
                        display_fc.sort_values("Forecast_Change", ascending=False).head(50),
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.warning(
                        f"{label} file is missing one or more expected columns: "
                        + ", ".join(sorted(required_fc - set(fc.columns)))
                    )
            except Exception as e:
                st.warning(f"Could not read the {label} forecast file: {e}")

    if all(f is None for _, f, _ in forecast_files):
        st.info(
            "No forecast CSVs were uploaded. The dashboard still provides all EDA charts. "
            "For the notebook's final global forecasts, upload forecast_7d_all.csv, "
            "forecast_14d_all.csv and forecast_30d_all.csv."
        )

# ============================================================
# DATA QUALITY
# ============================================================
with tabs[6]:
    st.header("7. Data quality and cleaning checks")

    missing = price_df.isna().sum().sort_values(ascending=False).reset_index()
    missing.columns = ["Column","Missing_Values"]

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Missing values")
        fig = px.bar(
            missing,
            x="Column",
            y="Missing_Values",
            title="Missing Values by Column",
        )
        fig.update_layout(xaxis_tickangle=-60)
        st.plotly_chart(fig, use_container_width=True)
        explain(
            "Missing values",
            "Bars show how many records are missing in each original price-data column after the "
            "basic cleaning steps."
        )

    with c2:
        st.subheader("Price distributions")
        dist = price_df[["Min_Price","Max_Price","Modal_Price"]].melt(
            var_name="Price_Type", value_name="Price"
        ).dropna()
        # Limit only the visual sample; the underlying data remains unchanged.
        plot_dist = dist.sample(min(100000, len(dist)), random_state=42)
        fig = px.box(
            plot_dist,
            x="Price_Type",
            y="Price",
            points=False,
            title="Price Distribution",
        )
        st.plotly_chart(fig, use_container_width=True)
        explain(
            "Price distribution",
            "The box plot shows the central distribution and spread of minimum, maximum and modal prices. "
            "A sample is used only for rendering speed when the dataset is very large."
        )

    st.subheader("Cleaned data preview")
    st.dataframe(
        price_df.head(100),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Download weekly dataset")
    csv = weekly_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download weekly aggregated data",
        data=csv,
        file_name="weekly_price_data.csv",
        mime="text/csv",
    )

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption(
    "Source workflow: App.ipynb. The dashboard follows the notebook's price cleaning, "
    "state standardization, weekly aggregation, EDA, seasonality, volatility and weather-correlation terminology."
)
