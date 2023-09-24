import streamlit as st
import pandas as pd
from main import get_recommendations_with_details

# Load the CSV dataset
@st.cache_data    # Caching for faster reloading
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
    selected_category = st.selectbox('Select a category:', sorted(data['category'].unique()))
    filtered_data = data[data['category'] == selected_category]

    st.title("Product Recommendations App")

    # Create an input field for the user to enter the product ID
    
    product_id = st.number_input("Enter Product ID", min_value=0)

    
    # Add a dropdown for selecting a product by name
    # selected_product_name = st.selectbox('Select a product:', sorted(filtered_data['product_name'].values))

    # # Get the product ID for the selected product name
    # product_id = filtered_data[filtered_data['product_name'] == selected_product_name]['product_id'].values[0]

    # Create a button to trigger the recommendations
    if st.button("Get Recommendations"):
        # Call the recommendation function with default parameter values
        recommendations = get_recommendations_with_details(product_id=product_id)

        # Display recommendations in the Streamlit app
        st.header(f"Recommendations")
        num_columns = 3  # Number of columns in the grid layout
        num_recommendations = len(recommendations)
        num_rows = (num_recommendations - 1) // num_columns + 1

        columns = st.columns(num_columns)

        recommendation_index = 0
        for row in range(num_rows):
            for col in range(num_columns):
                if recommendation_index >= num_recommendations:
                    break

                with columns[col]:
                    recommendation = recommendations[recommendation_index]
                    st.subheader(f"Recommendation {recommendation_index + 1}")
                    st.write(f"Product ID: {recommendation['product_id']}")
                    st.write(f"Product Name: {recommendation['product_name']}")
                    st.write(f"Category: {recommendation['category']}")
                    st.write(f"Rating: {recommendation['rating']} ({recommendation['rating_count']})")
                    st.image(recommendation['img_link'], use_column_width=True)
                    st.write(f"Product Link: [Link]({recommendation['product_link']})")
                    recommendation_index += 1

if __name__ == '__main__':
    main()
