import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Bird Dashboard", layout="wide")

st.title("🐦 Bird Species Observation Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("../data/cleaned_bird_data_new.csv")

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("🔍 Filters")

location = st.sidebar.multiselect(
    "Habitat Type",
    df['Location_Type'].unique(),
    default=df['Location_Type'].unique()
)

year = st.sidebar.multiselect(
    "Year",
    df['Year'].unique(),
    default=df['Year'].unique()
)

species = st.sidebar.multiselect(
    "Species",
    df['Common_Name'].unique()
)

# -------------------------------
# APPLY FILTERS
# -------------------------------
filtered_df = df[
    (df['Location_Type'].isin(location)) &
    (df['Year'].isin(year))
]

if species:
    filtered_df = filtered_df[filtered_df['Common_Name'].isin(species)]

# -------------------------------
# KPI CARDS
# -------------------------------
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Observations", len(filtered_df))
col2.metric("Total Species", filtered_df['Common_Name'].nunique())
col3.metric("Locations", filtered_df['Admin_Unit_Code'].nunique())

# -------------------------------
# ROW 1: HABITAT + SEX
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌿 Habitat Distribution")
    fig1 = px.bar(filtered_df, x='Location_Type', color='Location_Type')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("⚧️ Sex Distribution")
    sex_data = filtered_df['Sex'].value_counts().reset_index()
    sex_data.columns = ['Sex', 'Count']
    fig2 = px.pie(sex_data, names='Sex', values='Count')
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# ROW 2: TOP SPECIES + LOCATION
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🐦 Top 10 Bird Species")
    top_species = filtered_df['Common_Name'].value_counts().head(10).reset_index()
    top_species.columns = ['Common_Name', 'Count']
    fig3 = px.bar(top_species, x='Common_Name', y='Count', color='Common_Name')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("📍 Location Analysis")
    loc_data = filtered_df['Admin_Unit_Code'].value_counts().reset_index()
    loc_data.columns = ['Location', 'Count']
    fig4 = px.bar(loc_data, x='Location', y='Count', color='Location')
    st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# ROW 3: TIME + WEATHER
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Year-wise Trend")
    year_data = filtered_df['Year'].value_counts().sort_index()
    fig5 = px.line(x=year_data.index, y=year_data.values,
                   labels={'x': 'Year', 'y': 'Observations'})
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.subheader("🌦️ Weather Impact")
    weather_data = filtered_df['Sky'].value_counts().reset_index()
    weather_data.columns = ['Sky', 'Count']
    fig6 = px.bar(weather_data, x='Sky', y='Count', color='Sky')
    st.plotly_chart(fig6, use_container_width=True)

# -------------------------------
# SCATTER PLOT (ADVANCED)
# -------------------------------
st.subheader("🌡️ Temperature vs Humidity")

fig7 = px.scatter(filtered_df,
                  x='Temperature',
                  y='Humidity',
                  color='Location_Type')

st.plotly_chart(fig7, use_container_width=True)

# -------------------------------
# DATA PREVIEW
# -------------------------------
st.subheader("📄 Data Preview")
st.dataframe(filtered_df.head(50))