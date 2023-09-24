import streamlit as st
import pandas as pd
from main import get_recommendations_with_details
# Load the CSV dataset
@st.cache_data   # Caching for faster reloading
def load_data():
    data = pd.read_csv('amazon.csv')
    return data

# Create a Streamlit app
def main():
    st.title('Ecommerce Demo')

    # Load the dataset
    data = load_data()

    st.title('Filters')
    # Filter products by category
    selected_category = st.selectbox('Select a category:', data['category'].unique())
    filtered_data = data[data['category'] == selected_category]
    #product_filters(filtered_data)
    st.title("Product Recommendations App")

    # Create an input field for the user to enter the product ID
    product_id = st.number_input("Enter Product ID", min_value=0)

    # Create a button to trigger the recommendations
    if st.button("Get Recommendations"):
        # Call the recommendation function with default parameter values
        recommendations = get_recommendations_with_details(product_id=product_id)

        # Display recommendations in the Streamlit app
        st.header("Recommendations")
        for i, rec in enumerate(recommendations, start=1):
            st.subheader(f"Recommendation {i}")
            st.write(f"Product ID: {rec['product_id']}")
            st.write(f"Product Name: {rec['product_name']}")
            st.write(f"Category: {rec['category']}")
            st.write(f"Rating: {rec['rating']}")
            st.write(f"Rating Count: {rec['rating_count']}")
            st.write(f"Image Link: {rec['img_link']}")
            st.write(f"Product Link: {rec['product_link']}")
            st.write(f"Distance: {rec['distance']}")

def product_filters(filtered_data):
    st.title('Products Display')
    # Display products in a grid layout
    num_columns = 3  # Number of columns in the grid
    num_products = len(filtered_data)
    num_rows = (num_products - 1) // num_columns + 1

    columns = st.columns(num_columns)

    product_index = 0
    for row in range(num_rows):
        for col in range(num_columns):
            if product_index >= num_products:
                break

            with columns[col]:
                product = filtered_data.iloc[product_index]
                st.write(f"**Product Name:** {product['product_name']}")
                #st.write(f"**Category:** {product['category']}")
                st.write(f"**Rating:** {product['rating']}({product['rating_count']})")
                st.image(product['img_link'], use_column_width=True)
                st.write(f"**Product Link:** [Link]({product['product_link']})")
                product_index += 1

if __name__ == '__main__':
    main()
