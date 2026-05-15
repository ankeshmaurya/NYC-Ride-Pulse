

import os

import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="NYC Ride Pulse", page_icon=":taxi:")


# LOAD DATA ONCE
@st.cache_data
def load_data():
    path = "uber-raw-data-sep14.csv.gz"
    if not os.path.isfile(path):
        path = f"https://github.com/streamlit/demo-uber-nyc-pickups/raw/main/{path}"

    data = pd.read_csv(
        path,
        nrows=100000,  # approx. 10% of data
        names=[
            "date/time",
            "lat",
            "lon",
        ],  # specify names directly since they don't change
        skiprows=1,  # don't read header since names specified directly
        usecols=[0, 1, 2],  # doesn't load last column, constant value "B02512"
        parse_dates=[
            "date/time"
        ],  # set as datetime instead of converting after the fact
    )

    data["weekday"] = data["date/time"].dt.day_name()
    data["hour"] = data["date/time"].dt.hour
    return data


# FUNCTION FOR AIRPORT MAPS
def map(data, lat, lon, zoom):
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v10",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position=["lon", "lat"],
                    radius=100,
                    elevation_scale=3,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )


# FILTER DATA FOR A SPECIFIC HOUR, CACHE
@st.cache_data
def filterdata(df, hour_selected, weekday_selected):
    filtered = df[df["hour"] == hour_selected]
    if weekday_selected != "All days":
        filtered = filtered[filtered["weekday"] == weekday_selected]
    return filtered


# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
@st.cache_data
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))


# FILTER DATA BY HOUR
@st.cache_data
def histdata(df, hr, weekday_selected):
    filtered = df[(df["hour"] >= hr) & (df["hour"] < (hr + 1))]
    if weekday_selected != "All days":
        filtered = filtered[filtered["weekday"] == weekday_selected]

    hist = np.histogram(filtered["date/time"].dt.minute, bins=60, range=(0, 60))[0]

    return pd.DataFrame({"minute": range(60), "pickups": hist})


# STREAMLIT APP LAYOUT
data = load_data()

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((2, 3))

# SEE IF THERE'S A QUERY PARAM IN THE URL (e.g. ?pickup_hour=2)
if not st.session_state.get("url_synced", False):
    try:
        pickup_hour = int(st.query_params["pickup_hour"])
        st.session_state["pickup_hour"] = pickup_hour
        st.session_state["url_synced"] = True
    except KeyError:
        pass


# IF THE SLIDER CHANGES, UPDATE THE QUERY PARAM
def update_query_params():
    hour_selected = st.session_state["pickup_hour"]
    st.query_params["pickup_hour"] = hour_selected


with row1_1:
    st.title("NYC Ride Pulse")
    hour_selected = st.slider(
        "Pick an hour", 0, 23, key="pickup_hour", on_change=update_query_params
    )
    weekday_selected = st.selectbox(
        "Day of week",
        ["All days"] + list(data["weekday"].unique()),
    )


with row1_2:
    st.write(
        """
    ##
    Explore pickup patterns across New York City and its major airports.
    Use the controls to isolate specific hours and days, then compare how activity concentrates around key locations.
    """
    )

st.caption("Data: 100k pickup samples from September 2014.")

filtered_data = filterdata(data, hour_selected, weekday_selected)
pickup_count = int(filtered_data.shape[0])
unique_days = int(filtered_data["date/time"].dt.date.nunique())
avg_per_day = int(round(pickup_count / max(unique_days, 1), 0))

metric_1, metric_2, metric_3 = st.columns(3)
metric_1.metric("Pickups in view", f"{pickup_count:,}")
metric_2.metric("Distinct days", f"{unique_days}")
metric_3.metric("Avg pickups/day", f"{avg_per_day:,}")

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1, row2_2, row2_3, row2_4 = st.columns((2, 1, 1, 1))

# SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
la_guardia = [40.7900, -73.8700]
jfk = [40.6650, -73.7821]
newark = [40.7090, -74.1805]
zoom_level = 12
midpoint = mpoint(data["lat"], data["lon"])

with row2_1:
    st.write(
        f"""**All New York City from {hour_selected}:00 and {(hour_selected + 1) % 24}:00**"""
    )
    map(filtered_data, midpoint[0], midpoint[1], 11)

with row2_2:
    st.write("**La Guardia Airport**")
    map(filtered_data, la_guardia[0], la_guardia[1], zoom_level)

with row2_3:
    st.write("**JFK Airport**")
    map(filtered_data, jfk[0], jfk[1], zoom_level)

with row2_4:
    st.write("**Newark Airport**")
    map(filtered_data, newark[0], newark[1], zoom_level)

# CALCULATING DATA FOR THE HISTOGRAM
chart_data = histdata(filtered_data, hour_selected, weekday_selected)

# LAYING OUT THE HISTOGRAM SECTION
st.write(
    f"""**Breakdown of rides per minute between {hour_selected}:00 and {(hour_selected + 1) % 24}:00**"""
)

st.altair_chart(
    alt.Chart(chart_data)
    .mark_area(
        interpolate="step-after",
    )
    .encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=["minute", "pickups"],
    )
    .configure_mark(opacity=0.25, color="#1f77b4"),
    use_container_width=True,
)
