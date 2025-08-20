# langchain_helper.py
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
import os

def _get_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("OPENAI_API_KEY", "")
        except Exception:
            api_key = ""
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Set it as an environment variable or in Streamlit secrets.")
    return api_key

def _create_llm():
    api_key = _get_openai_api_key()
    # Updated model to gpt-3.5-turbo
    return OpenAI(model_name="gpt-3.5-turbo", temperature=0.7, openai_api_key=api_key)

def generate_restaurant_name_and_items(cuisine):
    llm = _create_llm()

    prompt_template_name = PromptTemplate(
        input_variables=["cuisine"],
        template="I want to open a restaurant for {cuisine} food. Suggest a fancy name for this.",
    )
    name_chain = LLMChain(
        llm=llm, prompt=prompt_template_name, output_key="restaurant_name"
    )

    prompt_template_items = PromptTemplate(
        input_variables=["restaurant_name"],
        template="Suggest some menu items for {restaurant_name}. Return it as a comma separated list.",
    )
    food_items_chain = LLMChain(
        llm=llm, prompt=prompt_template_items, output_key="menu_items"
    )

    chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=["cuisine"],
        output_variables=["restaurant_name", "menu_items"],
    )
    response = chain.invoke({"cuisine": cuisine})
    return response

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate restaurant name and menu items.")
    parser.add_argument("-c", "--cuisine", help="Cuisine type (e.g., Italian, Chinese, Mexican, Indian)")
    args = parser.parse_args()

    cuisine = args.cuisine or input("Enter cuisine: ").strip()
    if not cuisine:
        raise SystemExit("Cuisine is required.")

    response = generate_restaurant_name_and_items(cuisine)
    print("Restaurant:", response.get("restaurant_name", "").strip())
    items = [i.strip() for i in response.get("menu_items", "").split(",") if i.strip()]
    print("Menu Items:")
    for item in items:
        print("-", item)
