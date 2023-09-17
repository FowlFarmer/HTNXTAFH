from keys import OPENAI_KEY
import requests
import openai

openai.api_key = OPENAI_KEY

def generate_recipes(ingredients, prompt):
    ingredients_str = ', '.join(ingredients)  # Convert the list of ingredients to a comma-separated string
    prompt = f" {prompt}:{ingredients_str}"
    response = openai.Completion.create(
        engine="davinci",  # Choose the GPT-3 engine you want to use
        prompt=prompt,
        max_tokens=150  # Adjust based on your requirements
    )
    return response.choices[0].text

ingredients = ["chicken", "rice", "broccoli"]
prompt = "What are some creative recipes I can make with these ingredients? Please also state the recipe name."
recipe = generate_recipes(ingredients, prompt)
print(recipe)
