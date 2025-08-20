import streamlit as st
import langchain_helper

st.title("Restaurant Name Generator") 

cuisine = st.sidebar.selectbox("Pick a Cuisine", ["Italian", "Chinese", "Mexican", "Indian"])

if cuisine:
    try:
        response = langchain_helper.generate_restaurant_name_and_items(cuisine)

        st.header(response['restaurant_name'].strip())
        menu_items = [i.strip() for i in response.get("menu_items", "").split(",") if i.strip()]

        st.write("**Menu Items**")
        for item in menu_items:
            st.write("-", item)
    except Exception as e:
        st.error(f"Failed to generate results: {e}")
