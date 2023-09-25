import streamlit as st
import pandas as pd
from main import get_recommendations_with_details
from sklearn.preprocessing import LabelEncoder
import pickle


# --- GENERAL SETTINGS ---
PAGE_TITLE = "Ecommerce Demo"
PAGE_ICON = ":wave:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)
# Load the model using pickle
model = pickle.load(open('model.pkl', 'rb'))
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

    st.title('Filter Category')
    # Filter products by category
    selected_category = st.selectbox('Select a category:', sorted(data['category'].unique()))
    filtered_data = data[data['category'] == selected_category]

    st.title("Product Recommendations")

    # Create an input field for the user to enter the product ID    
    #product_id = st.number_input("Enter Product ID", min_value=0)
    
    # Add a dropdown for selecting a product by name
    product_id_encoder = LabelEncoder()
    selected_product_name = st.selectbox('Select a product:', sorted(filtered_data['product_name'].values))

    # Get the product ID for the selected product name
    selected_product_id = filtered_data[filtered_data['product_name'] == selected_product_name]['product_id'].values[0]
    product_id_encoder.fit(data['product_id'])
    product_id = product_id_encoder.transform([selected_product_id])[0]

    selected_product_details = filtered_data[filtered_data['product_id'] == selected_product_id].iloc[0]

    # Use st.columns to create two columns for details and image
    details_col, image_col = st.columns(2)

    # Display product details in the left column
    with details_col:
        st.header("Selected Product Details")
        st.write(f"Product ID: {selected_product_details['product_id']}")
        st.write(f"Product Name: {selected_product_details['product_name']}")
        st.write(f"Category: {selected_product_details['category']}")
        st.write(f"Rating: {selected_product_details['rating']} ({selected_product_details['rating_count']})")

    # Display product image and link in the right column
    with image_col:
        st.image(selected_product_details['img_link'], use_column_width=True)
        st.write(f"Product Link: [Link]({selected_product_details['product_link']})")
    
    # button to trigger the recommendations
    if st.button("Get Recommendations"):
        # Call the recommendation function with default parameter values
        recommendations = get_recommendations_with_details(product_id=product_id)

        # Display recommendations in the Streamlit app
        st.header(f"Recommendations")
        num_columns = 2  # Number of columns in the grid layout
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
                    st.image(recommendation['img_link'], use_column_width=False)
                    st.write(f"Product Link: [Link]({recommendation['product_link']})")
                    recommendation_index += 1

if __name__ == '__main__':
    main()
