import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')

st.header("Used Cars Dashboard")
st.write("Exploring price, mileage, and condition of used vehicles.")

if st.checkbox("Show Price Histogram"):
    fig = px.histogram(df, x = 'price')
    st.plotly_chart(fig)

st.subheader("Price vs. Odometer Scatter Plot")
fig2 = px.scatter(df, x = 'odometer', y = 'price', color = 'condition')
st.plotly_chart(fig2)
