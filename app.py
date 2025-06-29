import streamlit as st
import pandas as pd
import plotly.express as px

# Missing values: It is more beneficial to try to restore missing data, as by deleting it we can lose potentially important insights. is_4wd contains a boolean type of information (yes/no). So filling missing data with 0 will allow us to keep a potentially useful feature and also convert the whole column data type as bool. You could fill paint_color with unknown or any other placeholder, as it is not possible to fill this value based on other car features. For model_year, cylinders, odometer it is possible to check the relationship between feature with missing values and other vehicle characteristics to fill it with more relevant value (Critical). You could determine the features (columns) that could relate to the column we are trying to fill. Then you could use transform() method to fill these missing values per group of relatable columns.
def load_data():
    df = pd.read_csv('vehicles_us.csv')

    df['is_4wd'] = df['is_4wd'].fillna(0).astype(bool)
    df['paint_color'] = df['paint_color'].fillna('Unknown')
    df['cylinders'] = df.groupby('type')['cylinders'].transform(lambda x: x.fillna(x.median()))
    df['model_year'] = df.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))
    # The vehicles_us.csv dataset likely contains missing values. It's a good practice to inspect and handle these. For example, the price or odometer columns might have NaN values, which could affect the plots. You could add a section to inspect and clean the data.    
    df.dropna(subset = ['price', 'odometer', 'condition'], inplace = True)

    return df
    
df = load_data()

st.header("Used Cars Dashboard")
st.write("Exploring price, mileage, and condition of used vehicles.")

# To make the dashboard more interactive, you could add widgets to filter the data. For instance, a slider for the year of the vehicle or a multi-select box for the manufacturer would allow users to explore the data more deeply.
st.sidebar.header("Filter Listings")
min_year, max_year = int(df['model_year'].min()), int(df['model_year'].max())
year_range = st.sidebar.slider('Model year range:', min_value = min_year, max_value = max_year, value=(min_year, max_year))
filtered_df = df[(df['model_year'] >= year_range[0]) & (df['model_year'] <= year_range[1])]

hist = px.histogram(filtered_df, x='odometer', nbins=50)
# While the subheader for the scatter plot is good, adding a main title to the plot itself can provide better context, especially if the user saves the plot image.
hist.update_layout(title_text="Odometer Distribution")
st.plotly_chart(hist)

# You can enhance the user experience by customizing the hover data to show more relevant information.
scatter = px.scatter(filtered_df, x='odometer', y='price', color='condition', hover_data=['model_year', 'model'])
# While the subheader for the scatter plot is good, adding a main title to the plot itself can provide better context, especially if the user saves the plot image.
scatter.update_layout(title_text="Price vs. Odometer by Vehicle Condition")
st.plotly_chart(scatter)

