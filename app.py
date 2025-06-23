import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    df = pd.read_csv('vehicles_us.csv')

    df['is_4wd'] = df['is_4wd'].fillna(0).astype(bool)
    df['paint_color'] = df['paint_color'].fillna('Unknown')
    df['cylinders'] = df.groupby('type')['cylinders'].transform(lambda x: x.fillna(x.median()))
    df['model_year'] = df.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))
    df['model_year'] = df.groupby('manufacturer')['model_year'].transform(lambda x: x.fillna(x.median()))
    df['odometer'] = df.groupby('model_year')['odometer'].transform(lambda x: x.fillna(x.median()))
    df['odometer'] = df.groupby('type')['odometer'].transform(lambda x: x.fillna(x.median()))
    df.dropna(subset = ['price', 'odometer', 'condition'], inplace = True)

    return df

st.header("Used Cars Dashboard")
st.write("Exploring price, mileage, and condition of used vehicles.")

def plot_pricedistribution(data):
    fig = px.histogram(df, x = 'price')
    fig.update_layout(title_text = "Distribution of Used Car Prices")
    st.plotly_chart(fig)

def plot_price_vs_odometer(data):
    fig2 = px.scatter(df, x = 'odometer', y = 'price', color = 'condition', hover_data = ['model_year', 'model'])
    fig2.update_layout(title_text = "Price vs. Odometer by Vehicle Condition")
    st.plotly_chart(fig2)

def main():
    st.set_page_config(page_title="Car Listings Dashboard", layout="wide")
    st.header("Used Car Listings Dashboard")
    st.write("Explore a dataset of used cars sold in the US. Filter and visualize vehicle pricing, mileage, and more.")

    df = load_data()

    st.sidebar.header("Filter Data")

    min_year = int(df['model_year'].min())
    max_year = int(df['model_year'].max())
    year_range = st.sidebar.slider("Model Year Range", min_year, max_year, (min_year, max_year))
    df = df[(df['model_year'] >= year_range[0]) & (df['model_year'] <= year_range[1])]

    manufacturers = sorted(df['manufacturer'].dropna().unique())
    selected_manufacturers = st.sidebar.multiselect("Select Manufacturers", manufacturers, default=manufacturers)
    df = df[df['manufacturer'].isin(selected_manufacturers)]

if __name__ == "__main__":
    main()
