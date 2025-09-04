# Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col

# App title and instructions
st.title("🥤 Customize Your Smoothie!")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for name on the smoothie
name_on_order = st.text_input("Name on Smoothie:")
if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake", type="snowflake")
session = cnx.session()

# Fetch fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
pd_df = my_dataframe.to_pandas()
fruit_names = pd_df["FRUIT_NAME"].tolist()

# Multiselect for ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_names,
    max_selections=5
)

# If ingredients are selected
if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)

    # Display the SQL insert statement (for debugging)
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """
    st.write("SQL Statement to be executed:")
    st.code(my_insert_stmt, language="sql")

    # Submit button
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered! ✅")
