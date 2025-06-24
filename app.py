import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    df = pd.read_csv('vehicles_us.csv')

    df['is_4wd'] = df['is_4wd'].fillna(0).astype(bool)
    df['paint_color'] = df['paint_color'].fillna('Unknown')
    df['cylinders'] = df.groupby('type')['cylinders'].transform(lambda x: x.fillna(x.median()))
    df['model_year'] = df.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))
    df.dropna(subset = ['price', 'odometer', 'condition'], inplace = True)

    return df
    
df = load_data()

st.header("Used Cars Dashboard")
st.write("Exploring price, mileage, and condition of used vehicles.")

st.sidebar.header("Filter Listings")
year_range = st.sidebar.slider('Model year range:', int(df['model_year'].min()), int(df['model_year'].max()), (2010, 2020))

manufacturers = st.sidebar.multiselect('Select Manufacturers:', options = sorted(df['model'].dropna().unique()), default = sorted(df['model'].dropna().unique()))

filtered_df = df[(df['model_year'] >= year_range[0]) & (df['model_year'] <= year_range[1]) & (df['model'].isin(model))]

st.title("Used Vehicle Dashboard")
st.markdown("Explore listings of used cars in the U.S. with interactive filters and visualizations.")

st.subheader("Distribution of Odometer Readings")
hist = px.histogram(filtered_df, x='odometer', nbins=50)
hist.update_layout(title_text="Odometer Distribution")
st.plotly_chart(hist)

st.subheader("Price vs. Odometer")
scatter = px.scatter(filtered_df, x='odometer', y='price', color='condition', hover_data=['model_year', 'model', 'type'])
scatter.update_layout(title_text="Price vs. Odometer by Vehicle Condition")
st.plotly_chart(scatter)

if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(filtered_df)

