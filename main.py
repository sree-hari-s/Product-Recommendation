# %%
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors

# %%
full_data = pd.read_csv('amazon.csv')
full_data.head()

# %%
full_data.shape

# %%
columns_to_drop = [
    'product_name', 'category', 'discounted_price', 'actual_price',
    'discount_percentage', 'about_product', 'user_name', 'review_id',
    'review_title', 'review_content', 'img_link', 'product_link',
    'rating_count'
]

data = full_data.drop(columns=columns_to_drop)
data.head()

# %%
data.shape

# %% [markdown]
# # Check the distribution of the rating

# %%
plt.figure(figsize=(15, 8))
sns.countplot(data=data.sort_values(by='rating'), x='rating')
plt.show()

# %%
data = data.dropna()
data = data[data.rating != '|']

# %%
product_id_encoder = LabelEncoder()
user_id_encoder = LabelEncoder()

# %%
data.product_id = product_id_encoder.fit_transform(data.product_id)
data.user_id = user_id_encoder.fit_transform(data.user_id)

# %%
data

# %% [markdown]
# # Splitting the dataset
#

# %%
Train, Test = train_test_split(data, test_size=0.2, random_state=42)

# %%
Train.head()

# %%
Test.head()

# %% [markdown]
# # Model
#

# %%
model = NearestNeighbors(metric='cosine', algorithm='brute')

# %%
model.fit(Train)

# %%
distances, indices = model.kneighbors(Train)

# %%
distances

# %%
indices

# %% [markdown]
# # Prediction

# %%


def get_recommendations_for_product(model, data, product_id, n_recommendations):
    # Find the index of the product_id in the data
    product_index = data.index[data['product_id'] == product_id].tolist()[0]

    # Compute recommendations for the specified product
    distances, indices = model.kneighbors(
        data.iloc[product_index].values.reshape(1, -1))

    # Print recommendations for the specified product
    print("Recommendations for product:", product_id)
    for j in range(1, n_recommendations + 1):
        try:
            recommended_product_id = data.iloc[indices[0][j], 0]
            distance = distances[0][j]
            print(f"{j}: {recommended_product_id}, with distance of {distance}")
        except IndexError:
            print("No more recommendations")
            break
    print("\n")


# %%
get_recommendations_for_product(model, data, 236, 5)

# %%


def get_recommendations_for_product2(model, data, n_recommendations, product_id):
    # Inverse transform the label-encoded product_id to get the original product_id
    original_product_id = product_id_encoder.inverse_transform([product_id])[0]

    # Find the index of the original product_id in the data DataFrame
    product_index = full_data[full_data['product_id']
                              == original_product_id].index[0]

    # Compute recommendations for the specified product
    distances, indices = model.kneighbors(
        data.iloc[product_index].values.reshape(1, -1))

    # Print details of recommended products
    print(
        f"Recommendations for product with original ID {original_product_id}:")
    original = full_data.loc[full_data['product_id']
                             == original_product_id].iloc[0]
    print(f"   Product Name: {original['product_name']}")
    print(f"   Category: {original['category']}")
    print("\n")
    for j in range(1, n_recommendations + 1):
        try:
            recommended_index = indices[0][j]
            recommended_original_id = product_id_encoder.inverse_transform(
                [recommended_index])[0]
            distance = distances[0][j]
            # Retrieve details of the recommended product from the full_data DataFrame
            recommended_product_details = full_data[full_data['product_id']
                                                    == recommended_original_id].iloc[0]
            print(f"{j}: Product ID: {recommended_original_id}, Distance: {distance}")
            # You can also print additional details of the recommended product
            print(
                f"   Product Name: {recommended_product_details['product_name']}")
            print(f"   Category: {recommended_product_details['category']}")
            # Add more details as needed
        except:
            print(f"No more recommendations")
            continue
        print("\n")


# %%
# Example usage:
get_recommendations_for_product2(model, data, 5, 21)

# %%

# %%
pickle.dump(model, open('model.pkl', 'wb'))

# %%
data.to_csv('Test_data.csv')

# %%
model = pickle.load(open('model.pkl', 'rb'))

# %%


def get_recommendations_with_details(model=model, data=data, n_recommendations=5, product_id=0):
    # Inverse transform the label-encoded product_id to get the original product_id
    original_product_id = product_id_encoder.inverse_transform([product_id])[0]

    # Find the index of the original product_id in the data DataFrame
    product_index = full_data[full_data['product_id']
                              == original_product_id].index[0]

    # Compute recommendations for the specified product
    distances, indices = model.kneighbors(
        data.iloc[product_index].values.reshape(1, -1))

    recommendations = []

    for j in range(1, n_recommendations + 1):
        try:
            recommended_index = indices[0][j]
            recommended_original_id = product_id_encoder.inverse_transform(
                [recommended_index])[0]
            distance = distances[0][j]

            # Retrieve details of the recommended product from the full_data DataFrame
            recommended_product_details = full_data[full_data['product_id']
                                                    == recommended_original_id].iloc[0]

            recommendation_info = {
                'product_id': recommended_original_id,
                'product_name': recommended_product_details['product_name'],
                'category': recommended_product_details['category'],
                'rating': recommended_product_details['rating'],
                'rating_count': recommended_product_details['rating_count'],
                'img_link': recommended_product_details['img_link'],
                'product_link': recommended_product_details['product_link'],
                'distance': distance
            }

            recommendations.append(recommendation_info)

        except:
            print(f"No more recommendations")
            continue

    return recommendations
